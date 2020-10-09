## Fitcoach : Fitbit R API and Recommendation Engine for Fitbit

We are glad to submit the `fitcoach` package. As part of the project we have been able to accomplish the following:

1. Connect R to Fitbit API and expose an individual’s Fitbit data as a dataframe for further analysis.  
   + `DataLoader.R` does this. [Example 1](fitcoach/vignettes/examples/fitcoach-usage.pdf) shows how.
   + `DataLoader` enables getting both the *daily time-series* data and *intraday time-series* data at 15 min breaks for the individual.
   + Note: intraday data will require the user to create a new app on Fitbit website and is only available for app owner. i.e User A cannot access intraday data from User B. This is a Fitbit restriction.

2. Created [`FitAnalyzer`](fitcoach/R/FitAnalyzer.R) R6 class that provides an _opinionated_ but focused implementation for analyzing Fitbit data. It is likely that this workflow might not work for all. In this situation, the user can directly use Fitbit functions provided in [FitUtil.R](fitcoach/R/FitUtil.R) and create a customized analysis flow.

3. We were able to build the following:  
   + Ability to set goals and find the most significant variables that are enabling meeting the goals.
   + Ability to call a function and provide recommendations for the rest of the day. This is implemented for both daily and intraday scenarios.
   + Provide advanced charts in *ggplot2*.

4. Package Design Philosophy  
   + `DataLoader.R` is an R6 class because it encapsulates a unique OAuth2.0-based flow for accessing Fitbit API. The goal of this class is to orchestrate the Fitbit connection flow and download _daily_ or _intraday_ JSON files into a folder so that the JSON files can be analyzed further.
   + `FitAnalyzer.R` is an R6 class with a opinioned workflow for analysis. The class maintains state related to goal, analysis type among other things. It does not store the dataframe used for analysis to avoid memory issues. The user is expected to hold on to the dataframe.
   + `FitUtil.R` is a utility file that has functions for Fitbit analysis.
   + We are using [GLM](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/glm.html) for daily file and [GBM](https://cran.r-project.org/web/packages/gbm/gbm.pdf) for intraday file analysis. Intraday file analysis has a lot more data points and hence GBM works well here.For daily file, we have 1 datapoint per day. Hence, we decided to use GLM because we do not expect a lot of data in this file.

Please refer to the detailed [examples](fitcoach/vignettes/examples/fitcoach-usage.pdf) to understand the usage of the package.
