# Analysis of Google Analytics 360 raw logs

With Google Analytics 360, you can access raw logs stored on BigQuery, with detail at hit level. This allows for much more thorough and finer analyses. Here are some examples of audience insights that can be generated with SQL queries only.

## Setup and connection

```python
# Import libraries
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from google.cloud import bigquery

sns.set()
```

```python
# Launch BigQuery client from the JSON credentials file
bq_client = bigquery.Client.from_service_account_json('../../bigquery_creds.json')

# Helper function for queries to be returned as a Dataframe
def bquery(sql):
    return bq_client.query(sql).to_dataframe()
```

## Users, sessions and pageviews

```python
# Sessions and page views for 10 days
sql = """
SELECT
    PARSE_DATE("%Y%m%d", date) AS date,
    COUNT(DISTINCT fullVisitorId) AS visitors,
    SUM(totals.visits) AS sessions,
    SUM(totals.pageviews) AS pageviews,
FROM `bigquery-public-data.google_analytics_sample.ga_sessions_*`
WHERE
    _TABLE_SUFFIX BETWEEN '20170701' AND '20170710'
GROUP BY 1
ORDER BY 1
"""
bquery(sql)
```

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>date</th>
      <th>visitors</th>
      <th>sessions</th>
      <th>pageviews</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2017-07-01</td>
      <td>1946</td>
      <td>2048</td>
      <td>6562</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2017-07-02</td>
      <td>1791</td>
      <td>1895</td>
      <td>5637</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2017-07-03</td>
      <td>1904</td>
      <td>2046</td>
      <td>6492</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2017-07-04</td>
      <td>1799</td>
      <td>1938</td>
      <td>5740</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2017-07-05</td>
      <td>2683</td>
      <td>2885</td>
      <td>9927</td>
    </tr>
    <tr>
      <th>5</th>
      <td>2017-07-06</td>
      <td>2478</td>
      <td>2658</td>
      <td>8924</td>
    </tr>
    <tr>
      <th>6</th>
      <td>2017-07-07</td>
      <td>2213</td>
      <td>2450</td>
      <td>9266</td>
    </tr>
    <tr>
      <th>7</th>
      <td>2017-07-08</td>
      <td>1732</td>
      <td>1859</td>
      <td>6087</td>
    </tr>
    <tr>
      <th>8</th>
      <td>2017-07-09</td>
      <td>1761</td>
      <td>1921</td>
      <td>6523</td>
    </tr>
    <tr>
      <th>9</th>
      <td>2017-07-10</td>
      <td>2512</td>
      <td>2769</td>
      <td>10183</td>
    </tr>
  </tbody>
</table>
</div>

## Breakdown by devices and channels

```python
# Traffic KPIs broken down by device and acquisition channel
sql = """
SELECT
    device.deviceCategory AS device,
    channelGrouping AS channel_grouping,
    SUM(totals.visits) AS sessions,
    SUM(totals.pageviews) AS pageviews
FROM `bigquery-public-data.google_analytics_sample.ga_sessions_*`
WHERE
    _TABLE_SUFFIX BETWEEN '20170701' AND '20170710'
GROUP BY 1,2
ORDER BY 1,2
"""
bquery(sql)
```

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>device</th>
      <th>channel_grouping</th>
      <th>sessions</th>
      <th>pageviews</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>desktop</td>
      <td>Affiliates</td>
      <td>557</td>
      <td>1543</td>
    </tr>
    <tr>
      <th>1</th>
      <td>desktop</td>
      <td>Direct</td>
      <td>1800</td>
      <td>6611</td>
    </tr>
    <tr>
      <th>2</th>
      <td>desktop</td>
      <td>Display</td>
      <td>74</td>
      <td>317</td>
    </tr>
    <tr>
      <th>3</th>
      <td>desktop</td>
      <td>Organic Search</td>
      <td>6504</td>
      <td>22545</td>
    </tr>
    <tr>
      <th>4</th>
      <td>desktop</td>
      <td>Paid Search</td>
      <td>333</td>
      <td>1630</td>
    </tr>
    <tr>
      <th>5</th>
      <td>desktop</td>
      <td>Referral</td>
      <td>2172</td>
      <td>12220</td>
    </tr>
    <tr>
      <th>6</th>
      <td>desktop</td>
      <td>Social</td>
      <td>1893</td>
      <td>4186</td>
    </tr>
    <tr>
      <th>7</th>
      <td>mobile</td>
      <td>Affiliates</td>
      <td>119</td>
      <td>451</td>
    </tr>
    <tr>
      <th>8</th>
      <td>mobile</td>
      <td>Direct</td>
      <td>2016</td>
      <td>5235</td>
    </tr>
    <tr>
      <th>9</th>
      <td>mobile</td>
      <td>Display</td>
      <td>32</td>
      <td>134</td>
    </tr>
    <tr>
      <th>10</th>
      <td>mobile</td>
      <td>Organic Search</td>
      <td>4224</td>
      <td>12096</td>
    </tr>
    <tr>
      <th>11</th>
      <td>mobile</td>
      <td>Paid Search</td>
      <td>338</td>
      <td>1361</td>
    </tr>
    <tr>
      <th>12</th>
      <td>mobile</td>
      <td>Referral</td>
      <td>89</td>
      <td>281</td>
    </tr>
    <tr>
      <th>13</th>
      <td>mobile</td>
      <td>Social</td>
      <td>1219</td>
      <td>3100</td>
    </tr>
    <tr>
      <th>14</th>
      <td>tablet</td>
      <td>Affiliates</td>
      <td>17</td>
      <td>85</td>
    </tr>
    <tr>
      <th>15</th>
      <td>tablet</td>
      <td>Direct</td>
      <td>223</td>
      <td>777</td>
    </tr>
    <tr>
      <th>16</th>
      <td>tablet</td>
      <td>Display</td>
      <td>4</td>
      <td>8</td>
    </tr>
    <tr>
      <th>17</th>
      <td>tablet</td>
      <td>Organic Search</td>
      <td>613</td>
      <td>2071</td>
    </tr>
    <tr>
      <th>18</th>
      <td>tablet</td>
      <td>Paid Search</td>
      <td>100</td>
      <td>257</td>
    </tr>
    <tr>
      <th>19</th>
      <td>tablet</td>
      <td>Referral</td>
      <td>13</td>
      <td>34</td>
    </tr>
    <tr>
      <th>20</th>
      <td>tablet</td>
      <td>Social</td>
      <td>129</td>
      <td>399</td>
    </tr>
  </tbody>
</table>
</div>

## Traffic stickiness indicators

```python
# Pages per session, average sessions duration (in seconds) and bounce rate
sql = """
SELECT
    PARSE_DATE("%Y%m%d", date) AS date,
    SUM(totals.visits) AS sessions,
    SUM(totals.pageviews)/SUM(totals.visits) AS page_per_session,
    SUM(totals.timeOnSite)/SUM(totals.visits) AS avg_session_duration,
    SUM(totals.bounces)/SUM(totals.visits) AS bounce_rate
FROM `bigquery-public-data.google_analytics_sample.ga_sessions_*`
WHERE
    _TABLE_SUFFIX BETWEEN '20170701' AND '20170710'
GROUP BY 1
ORDER BY 1
"""
bquery(sql)
```

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>date</th>
      <th>sessions</th>
      <th>page_per_session</th>
      <th>avg_session_duration</th>
      <th>bounce_rate</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2017-07-01</td>
      <td>2048</td>
      <td>3.204102</td>
      <td>103.764160</td>
      <td>0.581055</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2017-07-02</td>
      <td>1895</td>
      <td>2.974670</td>
      <td>101.568338</td>
      <td>0.568865</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2017-07-03</td>
      <td>2046</td>
      <td>3.173021</td>
      <td>119.063050</td>
      <td>0.558162</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2017-07-04</td>
      <td>1938</td>
      <td>2.961816</td>
      <td>107.820433</td>
      <td>0.567079</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2017-07-05</td>
      <td>2885</td>
      <td>3.440901</td>
      <td>119.314038</td>
      <td>0.515425</td>
    </tr>
    <tr>
      <th>5</th>
      <td>2017-07-06</td>
      <td>2658</td>
      <td>3.357412</td>
      <td>115.759970</td>
      <td>0.504515</td>
    </tr>
    <tr>
      <th>6</th>
      <td>2017-07-07</td>
      <td>2450</td>
      <td>3.782041</td>
      <td>146.904082</td>
      <td>0.489796</td>
    </tr>
    <tr>
      <th>7</th>
      <td>2017-07-08</td>
      <td>1859</td>
      <td>3.274341</td>
      <td>114.330285</td>
      <td>0.536310</td>
    </tr>
    <tr>
      <th>8</th>
      <td>2017-07-09</td>
      <td>1921</td>
      <td>3.395627</td>
      <td>114.941176</td>
      <td>0.546590</td>
    </tr>
    <tr>
      <th>9</th>
      <td>2017-07-10</td>
      <td>2769</td>
      <td>3.677501</td>
      <td>142.385338</td>
      <td>0.514265</td>
    </tr>
  </tbody>
</table>
</div>

## Transactions

```python
# Transactions and revenue
sql = """
SELECT
    PARSE_DATE("%Y%m%d", date) AS date,
    SUM(totals.visits) AS sessions,
    SUM(totals.transactions) AS transactions,
    SUM(totals.transactions)/SUM(totals.visits) AS conversion_rate,
    SUM(totals.transactionRevenue)/1e6 AS revenue,
    SUM(totals.transactionRevenue)/1e6/SUM(totals.transactions) AS avg_purchase_value
FROM `bigquery-public-data.google_analytics_sample.ga_sessions_*`
WHERE
    _TABLE_SUFFIX BETWEEN '20170701' AND '20170710'
GROUP BY 1
ORDER BY 1
"""
bquery(sql)
```

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>date</th>
      <th>sessions</th>
      <th>transactions</th>
      <th>conversion_rate</th>
      <th>revenue</th>
      <th>avg_purchase_value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2017-07-01</td>
      <td>2048</td>
      <td>3</td>
      <td>0.001465</td>
      <td>84.54</td>
      <td>28.180000</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2017-07-02</td>
      <td>1895</td>
      <td>8</td>
      <td>0.004222</td>
      <td>634.99</td>
      <td>79.373750</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2017-07-03</td>
      <td>2046</td>
      <td>15</td>
      <td>0.007331</td>
      <td>1225.81</td>
      <td>81.720667</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2017-07-04</td>
      <td>1938</td>
      <td>7</td>
      <td>0.003612</td>
      <td>379.98</td>
      <td>54.282857</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2017-07-05</td>
      <td>2885</td>
      <td>42</td>
      <td>0.014558</td>
      <td>8029.36</td>
      <td>191.175238</td>
    </tr>
    <tr>
      <th>5</th>
      <td>2017-07-06</td>
      <td>2658</td>
      <td>31</td>
      <td>0.011663</td>
      <td>3883.85</td>
      <td>125.285484</td>
    </tr>
    <tr>
      <th>6</th>
      <td>2017-07-07</td>
      <td>2450</td>
      <td>40</td>
      <td>0.016327</td>
      <td>4339.02</td>
      <td>108.475500</td>
    </tr>
    <tr>
      <th>7</th>
      <td>2017-07-08</td>
      <td>1859</td>
      <td>14</td>
      <td>0.007531</td>
      <td>454.96</td>
      <td>32.497143</td>
    </tr>
    <tr>
      <th>8</th>
      <td>2017-07-09</td>
      <td>1921</td>
      <td>19</td>
      <td>0.009891</td>
      <td>751.10</td>
      <td>39.531579</td>
    </tr>
    <tr>
      <th>9</th>
      <td>2017-07-10</td>
      <td>2769</td>
      <td>47</td>
      <td>0.016974</td>
      <td>4718.07</td>
      <td>100.384468</td>
    </tr>
  </tbody>
</table>
</div>

## Goals

Several types of **Goals** can be [defined](https://support.google.com/analytics/answer/1012040)  in Google Analytics:
* Destination page: e.g. */registersuccess.html*
* Duration: e.g. mininum 5 minutes per session
* Pages per session: e.g. >10 pages per session
* Event: e.g. click on a video

Goals are not computed in BigQuery raw logs, they have to be extracted with a query. Unlike queries above, that made use of the pre-aggregated metrics in the `totals` field, we now need to unnest the `hits` nested field to extract pages paths, so we compute sessions differently, by counting the number of distinct sessions IDs.

```python
# Compute if a goal has been reached in each session
sql = """
WITH sub1 AS (
    SELECT
        PARSE_DATE("%Y%m%d", date) AS date,
        CONCAT(fullVisitorId, CAST(visitId AS STRING)) AS session_id,
        -- Goal: browsed to page /registersuccess.html
        MAX(IF(hits.page.pagePath = '/registersuccess.html', 1, 0)) AS goal_destination,
        -- Goal: session duration >= 5 min
        MAX(IF(totals.timeOnSite >= 300, 1, 0)) AS goal_duration,
        -- Goal: pages per session > 10
        MAX(IF(totals.pageviews > 10, 1, 0)) AS goal_pageviews
    FROM
        `bigquery-public-data.google_analytics_sample.ga_sessions_*`,
        UNNEST(hits) AS hits
    WHERE
        _TABLE_SUFFIX BETWEEN '20170701' AND '20170710'
        AND totals.visits > 0
    GROUP BY date, session_id
)

SELECT
    date,
    COUNT(session_id) AS sessions,
    SUM(goal_destination) AS goals_destination,
    SUM(goal_duration) AS goals_duration,
    SUM(goal_pageviews) AS goals_pageviews
FROM sub1
GROUP BY date
ORDER BY date
"""
bquery(sql)
```

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>date</th>
      <th>sessions</th>
      <th>goals_destination</th>
      <th>goals_duration</th>
      <th>goals_pageviews</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2017-07-01</td>
      <td>2048</td>
      <td>30</td>
      <td>181</td>
      <td>114</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2017-07-02</td>
      <td>1895</td>
      <td>32</td>
      <td>168</td>
      <td>104</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2017-07-03</td>
      <td>2046</td>
      <td>39</td>
      <td>214</td>
      <td>116</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2017-07-04</td>
      <td>1938</td>
      <td>31</td>
      <td>194</td>
      <td>94</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2017-07-05</td>
      <td>2885</td>
      <td>53</td>
      <td>312</td>
      <td>202</td>
    </tr>
    <tr>
      <th>5</th>
      <td>2017-07-06</td>
      <td>2658</td>
      <td>43</td>
      <td>280</td>
      <td>156</td>
    </tr>
    <tr>
      <th>6</th>
      <td>2017-07-07</td>
      <td>2450</td>
      <td>55</td>
      <td>298</td>
      <td>195</td>
    </tr>
    <tr>
      <th>7</th>
      <td>2017-07-08</td>
      <td>1859</td>
      <td>34</td>
      <td>208</td>
      <td>114</td>
    </tr>
    <tr>
      <th>8</th>
      <td>2017-07-09</td>
      <td>1921</td>
      <td>39</td>
      <td>186</td>
      <td>129</td>
    </tr>
    <tr>
      <th>9</th>
      <td>2017-07-10</td>
      <td>2769</td>
      <td>72</td>
      <td>338</td>
      <td>220</td>
    </tr>
  </tbody>
</table>
</div>

## Path length: how many sessions before converting

```python
# Get number of session before a transaction, and conversion rates by session position
sql = """
WITH sub1 AS (
    SELECT
        fullVisitorId,
        CONCAT(fullVisitorId, CAST(visitId AS STRING)) AS session_id,
        visitStartTime,
        MAX(IF(totals.transactions > 0, 1, 0)) AS transaction_session,
        RANK() OVER (PARTITION BY fullVisitorId ORDER BY visitStartTime) AS session_number
    FROM `bigquery-public-data.google_analytics_sample.ga_sessions_*`
    WHERE
        _TABLE_SUFFIX BETWEEN '20170701' AND '20170710'
    GROUP BY fullVisitorId, session_id, visitStartTime
)

SELECT
    session_number,
    COUNT(session_id) AS sessions,
    SUM(transaction_session) AS transactions,
    SUM(transaction_session)/COUNT(session_id) AS conversion_rate
FROM sub1
GROUP BY session_number
HAVING transactions > 0
ORDER BY session_number
"""
bquery(sql)
```

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>session_number</th>
      <th>sessions</th>
      <th>transactions</th>
      <th>conversion_rate</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>19671</td>
      <td>141</td>
      <td>0.007168</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>1859</td>
      <td>43</td>
      <td>0.023131</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>520</td>
      <td>17</td>
      <td>0.032692</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>195</td>
      <td>7</td>
      <td>0.035897</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>99</td>
      <td>6</td>
      <td>0.060606</td>
    </tr>
    <tr>
      <th>5</th>
      <td>6</td>
      <td>41</td>
      <td>2</td>
      <td>0.048780</td>
    </tr>
    <tr>
      <th>6</th>
      <td>10</td>
      <td>10</td>
      <td>1</td>
      <td>0.100000</td>
    </tr>
  </tbody>
</table>
</div>

## Time lag: how much time before converting

```python
# Get time lag (in days) between first session of a user and a converting session
sql = """
WITH sub1 AS (
    SELECT
        fullVisitorId,
        MIN(visitStartTime) OVER (PARTITION BY fullVisitorId ORDER BY visitStartTime) AS first_session_time,
        MAX(IF(totals.transactions > 0, visitStartTime, 0)) AS transaction_session_time
    FROM `bigquery-public-data.google_analytics_sample.ga_sessions_*`
    WHERE
        _TABLE_SUFFIX BETWEEN '20170701' AND '20170710'
    GROUP BY fullVisitorId, visitStartTime
)

SELECT
    FLOOR((transaction_session_time - first_session_time)/3600/24) AS lag_days,
    COUNT(*) AS transactions
FROM sub1
WHERE transaction_session_time > 0
GROUP BY lag_days
ORDER BY lag_days
"""
bquery(sql)
```

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>lag_days</th>
      <th>transactions</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0.0</td>
      <td>187</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1.0</td>
      <td>12</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2.0</td>
      <td>5</td>
    </tr>
    <tr>
      <th>3</th>
      <td>3.0</td>
      <td>4</td>
    </tr>
    <tr>
      <th>4</th>
      <td>4.0</td>
      <td>5</td>
    </tr>
    <tr>
      <th>5</th>
      <td>5.0</td>
      <td>2</td>
    </tr>
    <tr>
      <th>6</th>
      <td>6.0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>7</th>
      <td>7.0</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>

## Differentiate brand vs non-brand keywords

```python
# Differentiate between SEA keywords containing 'google' vs others
sql = """
SELECT
    CASE
        WHEN REGEXP_CONTAINS(LOWER(trafficSource.keyword), r"google") AND channelGrouping = 'Paid Search' THEN 'Paid Search Brand'
        WHEN channelGrouping = 'Paid Search' THEN 'Paid Search Non Brand'
        ELSE 'Other channels'
    END AS channel,
    SUM(totals.visits) AS sessions,
    SUM(totals.transactions) AS transactions,
    SUM(totals.transactions)/SUM(totals.visits) AS conversion_rate,
FROM `bigquery-public-data.google_analytics_sample.ga_sessions_*`
WHERE
    _TABLE_SUFFIX BETWEEN '20170701' AND '20170710'
GROUP BY 1
ORDER BY 1
"""
bquery(sql)
```

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>channel</th>
      <th>sessions</th>
      <th>transactions</th>
      <th>conversion_rate</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Other channels</td>
      <td>21698</td>
      <td>217</td>
      <td>0.010001</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Paid Search Brand</td>
      <td>376</td>
      <td>1</td>
      <td>0.002660</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Paid Search Non Brand</td>
      <td>395</td>
      <td>8</td>
      <td>0.020253</td>
    </tr>
  </tbody>
</table>
</div>

## True Direct vs Last Non Direct Click

Definition of "Direct" channel in Google Analytics is rather narrow. A user will only be considered coming through "Direct" if he/she did *not* previously came via *any* other channel. Hence, acquisition channels in GA are attributed to the Last Non-Direct click.

With the BigQuery raw data, you can know if a user *actually* came directly to your site, even if he/she previously arrived via another channel, with the `trafficSource.isTrueDirect` field. Note how conversion rates are much higher when considering this parameter.

```python
# Differentiate True Direct in channels
sql = """
SELECT
    channelGrouping AS channel,
    trafficSource.isTrueDirect IS NOT NULL AS true_direct,
    SUM(totals.visits) AS sessions,
    SUM(totals.transactions) AS transactions,
    ROUND(100*SUM(totals.transactions)/SUM(totals.visits), 2) AS conversion_rate,
FROM `bigquery-public-data.google_analytics_sample.ga_sessions_*`
WHERE
    _TABLE_SUFFIX BETWEEN '20170701' AND '20170731'
GROUP BY 1,2
ORDER BY 1,2
"""
bquery(sql)
```

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>channel</th>
      <th>true_direct</th>
      <th>sessions</th>
      <th>transactions</th>
      <th>conversion_rate</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>(Other)</td>
      <td>False</td>
      <td>1</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Affiliates</td>
      <td>False</td>
      <td>1460</td>
      <td>2.0</td>
      <td>0.14</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Affiliates</td>
      <td>True</td>
      <td>328</td>
      <td>2.0</td>
      <td>0.61</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Direct</td>
      <td>True</td>
      <td>12306</td>
      <td>131.0</td>
      <td>1.06</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Display</td>
      <td>False</td>
      <td>548</td>
      <td>14.0</td>
      <td>2.55</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Display</td>
      <td>True</td>
      <td>142</td>
      <td>7.0</td>
      <td>4.93</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Organic Search</td>
      <td>False</td>
      <td>31468</td>
      <td>168.0</td>
      <td>0.53</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Organic Search</td>
      <td>True</td>
      <td>6187</td>
      <td>145.0</td>
      <td>2.34</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Paid Search</td>
      <td>False</td>
      <td>1684</td>
      <td>37.0</td>
      <td>2.20</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Paid Search</td>
      <td>True</td>
      <td>421</td>
      <td>16.0</td>
      <td>3.80</td>
    </tr>
    <tr>
      <th>10</th>
      <td>Referral</td>
      <td>False</td>
      <td>5508</td>
      <td>206.0</td>
      <td>3.74</td>
    </tr>
    <tr>
      <th>11</th>
      <td>Referral</td>
      <td>True</td>
      <td>4010</td>
      <td>342.0</td>
      <td>8.53</td>
    </tr>
    <tr>
      <th>12</th>
      <td>Social</td>
      <td>False</td>
      <td>7319</td>
      <td>1.0</td>
      <td>0.01</td>
    </tr>
    <tr>
      <th>13</th>
      <td>Social</td>
      <td>True</td>
      <td>430</td>
      <td>1.0</td>
      <td>0.23</td>
    </tr>
  </tbody>
</table>
</div>

## Conversion rate by weekday and hour

```python
# Conversion rate by weekday and hour
sql = """
SELECT
    EXTRACT(DAYOFWEEK FROM PARSE_DATE("%Y%m%d", date)) AS weekday,
    EXTRACT(HOUR FROM PARSE_TIMESTAMP("%s", CAST(visitStartTime AS STRING))) AS hour,
    100*SUM(totals.transactions)/SUM(totals.visits) AS conv_rate
FROM `bigquery-public-data.google_analytics_sample.ga_sessions_*`
WHERE
    _TABLE_SUFFIX BETWEEN '20170701' AND '20170731'
GROUP BY 1,2
"""
slots = bquery(sql)

# Plot as a heatmap
fig, ax = plt.subplots(1, 1, figsize=(8,8))
sns.heatmap(
    slots.pivot(index='hour', columns='weekday', values='conv_rate').fillna(0),
    cmap="YlGnBu", annot=True, fmt='.2f', cbar=False);
```

![png](ga360_analysis_files/ga360_analysis_26_0.png)


## How many pageviews before reaching a Destination Goal

```python
# Number of pages viewed in a session before reaching a Goal (destination page)
sql = """
WITH sub1 AS (
    SELECT
        CONCAT(fullVisitorId, CAST(visitId AS STRING)) AS session_id,
        -- Window function to compute rank of each Page viewed in a session
        RANK() OVER (PARTITION BY fullVisitorId, visitId ORDER BY hits.hitNumber) AS page_number,
        hits.page.pagePath AS page
    FROM `bigquery-public-data.google_analytics_sample.ga_sessions_*`,
    UNNEST(hits) AS hits
    WHERE
        _TABLE_SUFFIX BETWEEN '20170701' AND '20170710'
        -- Filter on Pages only, we don't want all Hits types
        AND hits.type = 'PAGE'
    GROUP BY fullVisitorId, visitId, hits.hitNumber, page
)

SELECT
    page_number,
    COUNT(*) AS goals
FROM sub1
-- Filter on the destination page associated with a Goal
WHERE page = '/registersuccess.html'
GROUP BY 1
ORDER BY 1
"""
goals_pages = bquery(sql)

# Plot distribution
(
    goals_pages
    .set_index('page_number')
    .reindex(list(range(0, max(goals_pages['page_number'])+1)))
    .plot(kind='bar', figsize=(10,6))
);
```

![png](ga360_analysis_files/ga360_analysis_28_0.png)
