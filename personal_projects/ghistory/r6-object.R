Historizr <- R6::R6Class (
    "Historizr",
    
    public = list (
        
        ### Public variables
        dataset = NULL,
        start.date = NULL,
        end.date = NULL,
        
        ### METHOD
        initialize = function (path = "./", 
                               itin.rm = FALSE,
                               all.queries = FALSE) {
            self$dataset <-
                sourceJSONFiles(path = path,
                                itin.rm = itin.rm,
                                all.queries = all.queries)
            self$start.date <- as.POSIXct(min(self$dataset$Date))
            self$end.date <- as.POSIXct(max(self$dataset$Date))
            message("JSON loaded")
        },
        
        ### METHOD
        getData = function () {
            self$dataset
        },
        
        ### METHOD
        setPeriod = function (start, end) {
            if (!missing(start) && as.POSIXct(start) >= self$start.date) {
                self$start.date <- as.POSIXct(start)
                self$dataset <- 
                    dplyr::filter(self$dataset, 
                                  Date >= as.POSIXct(start))
            }
            if (!missing(end) && as.POSIXct(end) <= self$end.date) {
                self$end.date <- as.POSIXct(end)
                self$dataset <- 
                    dplyr::filter(self$dataset, 
                                  Date <= as.POSIXct(end) + 3600 * 24)
            }
            self$getPeriod()
        },
        
        ### METHOD
        getPeriod = function () {
            print(paste("Start date:", self$start.date))
            print(paste("End date:", self$end.date))
        },
        
        ### METHOD
        findQuery = function (word, full.query = FALSE) {
            findKeyword(data = self$dataset, 
                        word = word, 
                        full.query = full.query)
        },
        
        ### METHOD
        plotCount = function (breakdown = "day") {
            if (breakdown == "day") plotDay(self$dataset)
            else if (breakdown == "week") plotWeek(self$dataset)
            else if (breakdown == "month") plotMonth(self$dataset)
            else warning("Invalid argument. Must be 'day', 'week' or 'month'.")
        },
        
        ### METHOD
        topQueries = function (n = 20) {
            topRequests(data = self$dataset, n = n)
        },
        
        ### METHOD
        termsFreq = function (language = "english") {
            private$corpus <- termsCorpus(self$dataset$Query, 
                                          language = language)
            termsFrequency(private$corpus)
        }
        
    ),
    
    private = list (
        
        ### Private variables
        corpus = NULL
        
    )
)