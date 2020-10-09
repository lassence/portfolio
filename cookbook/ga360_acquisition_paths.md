# [GA360] Conversion paths

## Initiate connection


```python
# Import libraries
import pandas as pd
from google.cloud import bigquery

# Launch BigQuery client from the JSON credentials file
bq_client = bigquery.Client.from_service_account_json('../bigquery_creds.json')

# Helper function for queries to be returned as a Dataframe
def bquery(sql):
    return bq_client.query(sql).to_dataframe()
```

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
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
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
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
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
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
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
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
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


