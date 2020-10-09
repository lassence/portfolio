library('jsonlite')
library('tidyr')
library('dplyr')
library('ggplot2')
library('tm')

### FUNCTION
# Get JSON files, concatenate and outputs a tbl_df
sourceJSONFiles <- function(path = "./", 
                            itin.rm = FALSE,
                            all.queries = FALSE) {

    # List JSON files in the folder
    json.list <- list.files(path = path, 
                            pattern = "\\.json$", 
                            ignore.case = TRUE)
    
    # Create empty tbl_df
    clean.df <- tbl_df(data.frame(Query = character(0), 
                                  Timestamp = character(0), 
                                  Date = character(0)))
    
    # Convert each JSON to tbl_df, and append them
    for (file in json.list) {
        extract <- fromJSON(paste(path, file, sep =""))

        # If close.queries == TRUE, unnest all timestamps
        if (all.queries == TRUE) {
            extract <- 
                extract$event$query %>% 
                tidyr::unnest() %>%
                dplyr::select(Timestamp = timestamp_usec, Query = query_text)

        # Otherwise, keep only 1st timestamp for queries very close in time
        } else {
            extract <- 
                extract$event$query %>% 
                dplyr::as.tbl() %>%
                dplyr::select(Timestamp = id, Query = query_text)
            extract$Timestamp <- sapply(extract$Timestamp, function(x) x[[1]][1])
        }
        
        # Append
        clean.df <- rbind(clean.df, extract)
    }
    
    # Convert dates
    clean.df <-
        clean.df %>%
        dplyr::mutate(Date = as.POSIXct(as.numeric(substr(Timestamp, 0, 10)), 
                             origin = "1970-01-01")) %>%
        dplyr::arrange(Date)
    
    # If 'init.rm = TRUE', remove all Google Maps itineraries queries
    if(itin.rm == TRUE) {
        clean.df <- filter(clean.df, !grepl(" -> ", Query))
    }
    
    # Output as tbl_df
    clean.df
}


### FUNCTION
# Find keyword within queries, and retrieve times of searches
findKeyword <- function(data, word, full.query = FALSE) {
    
    # If 'word' should be searched as the full query
    if (full.query == TRUE) {
        output <- dplyr::filter(data, Query == word)
    
    # If 'word' should be searched as a subset of the query
    } else {
        output <- 
            dplyr::filter(data, grepl(word, Query, fixed = TRUE) == TRUE)
    }
    
    # Output queries and dates of search
    output <- dplyr:: select(output, Query, Date)
    output
}

### FUNCTION
# Plot by Day
plotDay <- function(data) {
    
    # Mutate, group and summarize data
    data <- data %>%
        dplyr::mutate(Year = as.factor(substr(Date, 0, 4)),
               Month = as.factor(substr(Date, 6, 7)),
               Day = as.integer(substr(Date, 9, 10))) %>%        
        dplyr::group_by(Year, Month, Day) %>%
        dplyr::summarize(QueriesCount = n())
    
    # Plot by day, with facets by month and year
    graph <- 
        ggplot(data = data, aes(x = Day, y = QueriesCount)) +
        geom_bar(aes(fill = Year, color = Year), 
                 alpha = 0.3, 
                 stat = "identity", 
                 position = "identity") +
        facet_grid(Month ~ Year) +
        # Display parameters
        coord_cartesian(expand = 0) +
        guides(fill = FALSE, color = FALSE) +
        labs(title = "Queries Count by Day", 
             x = "", y = "Number of queries")
    plot(graph)
    
}


### FUNCTION
# Plot by Week
plotWeek <- function(data) {
    
    # Mutate, group and summarize data
    data <- data %>%
        dplyr::mutate(Year = as.factor(substr(Date, 0, 4)),
               Week = as.numeric(format(Date, "%U"))) %>%        
        dplyr::group_by(Year, Week) %>%
        dplyr::summarize(QueriesCount = n())
    
    # Plot weeks with facet by year
    graph <- 
        ggplot(data = data, aes(
            x = Week, 
            y = QueriesCount)) +
        geom_bar(aes(fill = Year, color = Year), 
                 alpha = 0.3, 
                 stat = "identity", 
                 position = "identity") +
        facet_grid(Year ~ .) +
        geom_smooth(color = "gray50", se = FALSE) +
        # Display parameters
        coord_cartesian(expand = 0) +
        guides(fill = FALSE, color = FALSE) +
        labs(title = "Queries Count by Week", 
             x = "", y = "Number of queries")
    plot(graph)

}

### FUNCTION
# Plot by month
plotMonth <- function(data) {
    
    # Mutate, group and summarize data
    data <- 
        data %>%
        dplyr::mutate(Year = as.factor(substr(Date, 0, 4)),
               YearMonth = substr(Date, 0, 7)) %>%        
        dplyr::group_by(Year, YearMonth) %>%
        dplyr::summarize(QueriesCount = n())
    
    # Plot summarized data
    graph <- 
        ggplot(data = data, aes(
            x = as.integer(row.names(data)), 
            y = QueriesCount)) +
        geom_bar(aes(fill = Year, color = Year), 
                 alpha = 0.3, 
                 stat = "identity", 
                 position = "identity") + 
        geom_smooth(color = "gray50", se = FALSE) +
        # Display parameters
        coord_cartesian(expand = 0) +
        guides(fill = FALSE, color = FALSE) +
        scale_x_discrete(labels = data$YearMonth, 
                         breaks = as.integer(row.names(data))) +
        labs(title = "Queries Count by Month", 
             x = "", y = "Number of queries") +
        theme(axis.text.x = element_text(angle = 90))
    plot(graph)
    
}

### FUNCTION
# Return top queries and plot the first n
topRequests <- function(data, n = 20) {
    
    # Get top n queries
    output <- 
        data %>% 
        dplyr::group_by(Query) %>% 
        dplyr::summarise(QueriesCount = n()) %>% 
        dplyr::arrange(desc(QueriesCount)) %>%
        dplyr::top_n(n)

    # Get top 10 queries in descending order
    gdata <- output[1:10, ]
    
    # Plot top 10 queries
    graph <-
        ggplot(data = gdata, 
               aes(x = Query, 
                   y = QueriesCount)) +
        geom_bar(fill = "navyblue",
                 stat = "identity", 
                 position = "identity") +
        coord_flip(expand = 0) +
        # scale_x_discrete(labels = substr(gdata$Query, 0, 20)) +
        guides(fill = FALSE, color = FALSE) +
        labs(title = "Top Queries Over the Period", 
             x = "", y = "")
    plot(graph)
    
    # Output top queries as tbl_df
    output
    
}

### FUNCTION
# Create 'Corpus' of terms, for further analysis
termsCorpus <- function(data, language = "english") {
    
    # Load data as corpus
    corpus <- tm::Corpus(tm::VectorSource(data))
    
    # Clean up data
    corpus <-
        corpus %>%
        tm::tm_map(tm::content_transformer(tolower)) %>%
        tm::tm_map(tm::content_transformer(function (x) gsub("/|-|\\.|@|'|\\?|!|:|,|;|\\+|\\$|€|%|>|<", " ", x))) %>%
        tm::tm_map(tm::removeWords, tm::stopwords(language)) %>%
        tm::tm_map(tm::stripWhitespace) %>%
        tm::tm_map(tm::content_transformer(trimws))

    # Output
    corpus
    
}

### FUNCTION
# Return a dataframe of terms frequency
termsFrequency <- function(corpus) {
    
    # Transform Corpus to sorted matrix
    terms.freq <- 
        corpus %>%
        tm::TermDocumentMatrix() %>%
        as.matrix() %>%
        rowSums() %>%
        sort(decreasing = TRUE)
    
    # Transform matrix to dataframe
    terms.freq <-
        data.frame(Term = names(terms.freq), 
                   Count = terms.freq, 
                   row.names = NULL)
    
    # Output
    terms.freq
    
}

### FUNCTION
# Give a summary of the queries
queriesSummary <- function(data) {
    
    print(paste('Number of queries:', nrow(data)))
    print(paste('Start date:', min(data$Date)))
    print(paste('End date:', max(data$Date)))
    print('Top 5 queries:')
    print(topRequests(data, n = 5))
    
}

