# Authenticate to BigQuery in a Jupyter notebook

If you are working on a [cloud-based Jupyter notebook](gcp_ai_notebooks.md) in AI Platform, the instance automatically has access to BigQuery in your GCP project, so you won't need to set up anything in most cases. Otherwise, run the following steps.

## Method 1: with a service account

### Create a service account

Follow [these steps](https://cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=en#before-you-begin):  
1. Enable the BigQuery API.  
2. In the GCP console, go to the **Create service account key** page.  
3. From the **Service account** list, select **New service account.**  
4. In the **Service account name** field, enter a name.  
5. From the **Role** list, select **Project > Owner.**  
6. Click **Create**. A JSON file that contains your key downloads to your computer.

### Option A: set the environment variable

Set the environment variable `GOOGLE_APPLICATION_CREDENTIALS` to the file you downloaded. You can do it in the Terminal, or directly on your Notebook by prefixing `!` to the command.

```python
# Set environment variable
!export GOOGLE_APPLICATION_CREDENTIALS="ignore/bigquery_creds.json"
```

```python
# Start BigQuery client
from google.cloud import bigquery
bqclient = bigquery.Client()
```

### Option B: specify file location to the BigQuery client

Instead of setting the environment variable, you can directly specify the credentials JSON file when starting BigQuery client, with `from_service_account_json()`. 

```python
# Start BigQuery client and specify a credentials file
bqclient = bigquery.Client.from_service_account_json('ignore/bigquery_creds.json')
```

## Method 2: as final user

While the service account method is preferable for most situations, you might need to identify as a final user in some cases, for example to work with datasets that have been granted access to your own account.

### Set up

1. In the GCP console, enable the BigQuery API.  
2. Install the *google-cloud-bigquery* and *google-auth-oauthlib* Python libraries:  
`pip install --upgrade google-cloud-bigquery google-auth-oauthlib`

### Create your client credentials

1. In the GCP console, go to the [OAuth consent screen](https://console.cloud.google.com/apis/credentials/consent) page.  
2. On the Credentials page, click **Create credentials**, then select **OAuth client ID**.  
3. Select **Other** > **Create** > **OK**.  
4. Download the credentials by clicking the **Download JSON** button for the client ID.  
5. Save the file as `client_secrets.json`

### Authenticate and call the API

```python
# Import library and start authentication flow
from google_auth_oauthlib import flow

appflow = flow.InstalledAppFlow.from_client_secrets_file(
    '/Users/home/Downloads/client_secrets.json',
    scopes=['https://www.googleapis.com/auth/bigquery'])

# Authentication flow
# If running a remote server, use `appflow.run_local_server()` instead
appflow.run_console()   
credentials = appflow.credentials

# Start BigQuery client
bqclient = bigquery.Client(project='my-project-id', credentials=credentials)
```
