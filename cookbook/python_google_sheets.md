# Read and write to Google Sheets with Python

## Setup

Install the necessary Google Python libraries:

```sh
pip install — upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

```python
# Import standard libraries
import pandas as pd
import numpy as np
import pickle
import os

# Import Google API libraries
from googleapiclient import discovery
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
```

## Connection

Enable the Google Sheets API for your account and download credentials as a JSON file, by following [these steps](https://developers.google.com/sheets/api/quickstart/python#step_1_turn_on_the).

```python
# Function to generate user token
def gsheet_api_check(SCOPES, TOKEN, CREDENTIALS):
    creds = None
    if os.path.exists(TOKEN):
        with open(TOKEN, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS, SCOPES)
            creds = flow.run_console()
        with open(TOKEN, 'wb') as token:
            pickle.dump(creds, token)
    return creds

# Connect to Google Sheets API v4
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']   # Allow read and write to Google Sheets
TOKEN = 'data/gsheet_token.pickle'
CREDENTIALS = 'data/gsheet_credentials.json'
CREDS = gsheet_api_check(SCOPES, TOKEN, CREDENTIALS)
```

```python
# Connect to the service
service = discovery.build('sheets', 'v4', credentials=CREDS)
SPREADSHEET_ID = '1c0HS6Wc09bri6vvQQds3zVMGvXNbYJ3gKY5wtyaAYxI'   # Found in the Google Sheet URL
RANGE = 'Sheet1!A:Z'   # Tab and cells range to be read and/or written
```

## Read from a Google Sheet

```python
# Read from a Google Sheet
request = service.spreadsheets().values().get(
    spreadsheetId=SPREADSHEET_ID, 
    range=RANGE
)
response = request.execute()

# Convert data to a pandas DataFrame
pd.DataFrame(response.get('values', []))
```

<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>0</th>
      <th>1</th>
      <th>2</th>
      <th>3</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>A</td>
      <td>B</td>
      <td>C</td>
      <td>D</td>
    </tr>
    <tr>
      <th>1</th>
      <td>0,206</td>
      <td>0,661</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0,144</td>
      <td>0,157</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>3</th>
      <td>0,733</td>
      <td>0,094</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0,18</td>
      <td>0,607</td>
      <td>None</td>
      <td>None</td>
    </tr>
    <tr>
      <th>5</th>
      <td>0,321</td>
      <td>0,541</td>
      <td>None</td>
      <td>None</td>
    </tr>
  </tbody>
</table>
</div>

## Write a pandas DataFrame to a Google Sheet

```python
# Optional: clear data on a Sheet range
request = service.spreadsheets().values().clear(
    spreadsheetId=SPREADSHEET_ID, 
    range=RANGE
)
response = request.execute()
```

```python
# Create DataFrame to be written to the Google Sheet
df = pd.DataFrame(np.random.random(size=(5, 4)), columns=list('ABCD')).round(3)

# Convert DataFrame to a list of rows, with the columns names as first row
value_range_body = {
  "values": [list(df.columns)] + df.values.tolist()
}

# Write data to the Google Sheet
request = service.spreadsheets().values().update(
    spreadsheetId=SPREADSHEET_ID, 
    range=RANGE, 
    valueInputOption='RAW', 
    body=value_range_body)
response = request.execute()
```
