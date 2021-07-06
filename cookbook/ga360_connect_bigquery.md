# Connect to Google Analytics 360 raw logs

## Setup

Google Analytics 360 allows access to raw logs stored on BigQuery. Google provides a public sample BigQuery dataset for GA 360, that can be queried either directly in the BigQuery interface, or via a client. For this tutorial series, we will use Jupyter Notebooks.

**Step 1:** enable connection to the BigQuery API from your notebook. In your GCP project, [follow these steps](https://cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=en#before-you-begin) to create a service account with access to BigQuery, and download a JSON file containing credentials.

**Step 2:** install the [*google-cloud-bigquery*](https://pypi.org/project/google-cloud-bigquery/) library with pip: `pip install google-cloud-bigquery`

## Initiate connection

```python
# Import libraries
import pandas as pd
from google.cloud import bigquery
```

```python
# Launch BigQuery client from the JSON credentials file
bq_client = bigquery.Client.from_service_account_json('../bigquery_creds.json')

# Helper function for queries to be returned as a Dataframe
def bquery(sql):
    return bq_client.query(sql).to_dataframe()
```

## Query

```python
# Query the public Google Analytics 360 dataset
sql = """
SELECT *
FROM `bigquery-public-data.google_analytics_sample.ga_sessions_*`
WHERE _TABLE_SUFFIX = '20170801'
LIMIT 10
"""
bquery(sql)
```

<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>visitorId</th>
      <th>visitNumber</th>
      <th>visitId</th>
      <th>visitStartTime</th>
      <th>date</th>
      <th>totals</th>
      <th>trafficSource</th>
      <th>device</th>
      <th>geoNetwork</th>
      <th>customDimensions</th>
      <th>hits</th>
      <th>fullVisitorId</th>
      <th>userId</th>
      <th>clientId</th>
      <th>channelGrouping</th>
      <th>socialEngagementType</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>NaN</td>
      <td>1</td>
      <td>1501583974</td>
      <td>1501583974</td>
      <td>20170801</td>
      <td>{'visits': 1, 'hits': 1, 'pageviews': 1, 'time...</td>
      <td>{'referralPath': None, 'campaign': '(not set)'...</td>
      <td>{'browser': 'Chrome', 'browserVersion': 'not a...</td>
      <td>{'continent': 'Americas', 'subContinent': 'Car...</td>
      <td>[]</td>
      <td>[{'hitNumber': 1, 'time': 0, 'hour': 3, 'minut...</td>
      <td>2248281639583218707</td>
      <td>None</td>
      <td>None</td>
      <td>Organic Search</td>
      <td>Not Socially Engaged</td>
    </tr>
    <tr>
      <th>1</th>
      <td>NaN</td>
      <td>1</td>
      <td>1501616585</td>
      <td>1501616585</td>
      <td>20170801</td>
      <td>{'visits': 1, 'hits': 1, 'pageviews': 1, 'time...</td>
      <td>{'referralPath': None, 'campaign': '(not set)'...</td>
      <td>{'browser': 'Chrome', 'browserVersion': 'not a...</td>
      <td>{'continent': 'Americas', 'subContinent': 'Nor...</td>
      <td>[{'index': 4, 'value': 'North America'}]</td>
      <td>[{'hitNumber': 1, 'time': 0, 'hour': 12, 'minu...</td>
      <td>8647436381089107732</td>
      <td>None</td>
      <td>None</td>
      <td>Organic Search</td>
      <td>Not Socially Engaged</td>
    </tr>
    <tr>
      <th>2</th>
      <td>NaN</td>
      <td>1</td>
      <td>1501583344</td>
      <td>1501583344</td>
      <td>20170801</td>
      <td>{'visits': 1, 'hits': 1, 'pageviews': 1, 'time...</td>
      <td>{'referralPath': None, 'campaign': '(not set)'...</td>
      <td>{'browser': 'Chrome', 'browserVersion': 'not a...</td>
      <td>{'continent': 'Asia', 'subContinent': 'Souther...</td>
      <td>[{'index': 4, 'value': 'APAC'}]</td>
      <td>[{'hitNumber': 1, 'time': 0, 'hour': 3, 'minut...</td>
      <td>2055839700856389632</td>
      <td>None</td>
      <td>None</td>
      <td>Organic Search</td>
      <td>Not Socially Engaged</td>
    </tr>
    <tr>
      <th>3</th>
      <td>NaN</td>
      <td>1</td>
      <td>1501573386</td>
      <td>1501573386</td>
      <td>20170801</td>
      <td>{'visits': 1, 'hits': 1, 'pageviews': 1, 'time...</td>
      <td>{'referralPath': None, 'campaign': '(not set)'...</td>
      <td>{'browser': 'Chrome', 'browserVersion': 'not a...</td>
      <td>{'continent': 'Europe', 'subContinent': 'Weste...</td>
      <td>[{'index': 4, 'value': 'EMEA'}]</td>
      <td>[{'hitNumber': 1, 'time': 0, 'hour': 0, 'minut...</td>
      <td>0750846065342433129</td>
      <td>None</td>
      <td>None</td>
      <td>Direct</td>
      <td>Not Socially Engaged</td>
    </tr>
    <tr>
      <th>4</th>
      <td>NaN</td>
      <td>8</td>
      <td>1501651467</td>
      <td>1501651467</td>
      <td>20170801</td>
      <td>{'visits': 1, 'hits': 1, 'pageviews': 1, 'time...</td>
      <td>{'referralPath': None, 'campaign': '(not set)'...</td>
      <td>{'browser': 'Chrome', 'browserVersion': 'not a...</td>
      <td>{'continent': 'Americas', 'subContinent': 'Nor...</td>
      <td>[{'index': 4, 'value': 'North America'}]</td>
      <td>[{'hitNumber': 1, 'time': 0, 'hour': 22, 'minu...</td>
      <td>0573427169410921198</td>
      <td>None</td>
      <td>None</td>
      <td>Organic Search</td>
      <td>Not Socially Engaged</td>
    </tr>
    <tr>
      <th>5</th>
      <td>NaN</td>
      <td>1</td>
      <td>1501611552</td>
      <td>1501611552</td>
      <td>20170801</td>
      <td>{'visits': 1, 'hits': 1, 'pageviews': 1, 'time...</td>
      <td>{'referralPath': '/imgres', 'campaign': '(not ...</td>
      <td>{'browser': 'Chrome', 'browserVersion': 'not a...</td>
      <td>{'continent': 'Asia', 'subContinent': 'Southea...</td>
      <td>[]</td>
      <td>[{'hitNumber': 1, 'time': 0, 'hour': 11, 'minu...</td>
      <td>8313021323030224050</td>
      <td>None</td>
      <td>None</td>
      <td>Referral</td>
      <td>Not Socially Engaged</td>
    </tr>
    <tr>
      <th>6</th>
      <td>NaN</td>
      <td>2</td>
      <td>1501600400</td>
      <td>1501600400</td>
      <td>20170801</td>
      <td>{'visits': 1, 'hits': 1, 'pageviews': 1, 'time...</td>
      <td>{'referralPath': None, 'campaign': '(not set)'...</td>
      <td>{'browser': 'Chrome', 'browserVersion': 'not a...</td>
      <td>{'continent': 'Americas', 'subContinent': 'Nor...</td>
      <td>[{'index': 4, 'value': 'North America'}]</td>
      <td>[{'hitNumber': 1, 'time': 0, 'hour': 8, 'minut...</td>
      <td>9161549067325106850</td>
      <td>None</td>
      <td>None</td>
      <td>Organic Search</td>
      <td>Not Socially Engaged</td>
    </tr>
    <tr>
      <th>7</th>
      <td>NaN</td>
      <td>1</td>
      <td>1501640178</td>
      <td>1501640178</td>
      <td>20170801</td>
      <td>{'visits': 1, 'hits': 1, 'pageviews': 1, 'time...</td>
      <td>{'referralPath': None, 'campaign': '(not set)'...</td>
      <td>{'browser': 'Chrome', 'browserVersion': 'not a...</td>
      <td>{'continent': 'Asia', 'subContinent': 'Southea...</td>
      <td>[{'index': 4, 'value': 'APAC'}]</td>
      <td>[{'hitNumber': 1, 'time': 0, 'hour': 19, 'minu...</td>
      <td>7712738124831804349</td>
      <td>None</td>
      <td>None</td>
      <td>Organic Search</td>
      <td>Not Socially Engaged</td>
    </tr>
    <tr>
      <th>8</th>
      <td>NaN</td>
      <td>3</td>
      <td>1501585492</td>
      <td>1501585492</td>
      <td>20170801</td>
      <td>{'visits': 1, 'hits': 1, 'pageviews': 1, 'time...</td>
      <td>{'referralPath': '/', 'campaign': '(not set)',...</td>
      <td>{'browser': 'Chrome', 'browserVersion': 'not a...</td>
      <td>{'continent': 'Americas', 'subContinent': 'Nor...</td>
      <td>[{'index': 4, 'value': 'North America'}]</td>
      <td>[{'hitNumber': 1, 'time': 0, 'hour': 4, 'minut...</td>
      <td>6644155147493409979</td>
      <td>None</td>
      <td>None</td>
      <td>Referral</td>
      <td>Not Socially Engaged</td>
    </tr>
    <tr>
      <th>9</th>
      <td>NaN</td>
      <td>1</td>
      <td>1501635646</td>
      <td>1501635646</td>
      <td>20170801</td>
      <td>{'visits': 1, 'hits': 1, 'pageviews': 1, 'time...</td>
      <td>{'referralPath': None, 'campaign': '(not set)'...</td>
      <td>{'browser': 'Chrome', 'browserVersion': 'not a...</td>
      <td>{'continent': 'Americas', 'subContinent': 'Nor...</td>
      <td>[{'index': 4, 'value': 'North America'}]</td>
      <td>[{'hitNumber': 1, 'time': 0, 'hour': 18, 'minu...</td>
      <td>2485028951030553624</td>
      <td>None</td>
      <td>None</td>
      <td>Organic Search</td>
      <td>Not Socially Engaged</td>
    </tr>
  </tbody>
</table>
</div>
