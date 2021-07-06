# Authenticate to Google API on a cloud-based notebook

When working with Google APIs on a **AI Platform Notebook**, you cannot access `localhost` like on a local machine. 
To generate credentials, the Google Auth library gives you the option to generate a callback URL on a *remote* address. For more details, refer to this [support page](https://cloud.google.com/bigquery/docs/authentication/end-user-installed).

```python
# Import library and start authentication flow
from google_auth_oauthlib import flow

appflow = flow.InstalledAppFlow.from_client_secrets_file(
    './client_secrets.json',
    scopes=['https://www.googleapis.com/auth/bigquery'])
```

## Running a local server

Visit the URL, authorize your app when prompted, and the autentication process will automatically complete.

```python
# If running a local server:
appflow.run_local_server()
```

    Please visit this URL to authorize this application: https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=707506262186-8li17b8ftmtls5t1da3tbqjcl6.apps.googleusercontent.com&redirect_uri=http%3A%2F%2Flocalhost%3A8080%2F&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fbigquery&state=X9l4xFtJDu1R7ykeGfkFNke0S0X&access_type=offline

## Running a remote server

In this case, for example when running code on an AI Platform Notebook, you cannot use `localhost` as callback URL. Use `run_console()` instead, and after visiting the URL and authorizing your app, you will be given an authorization code to be pasted in the prompt.

```python
# If running a remote server:
appflow.run_console()
```

    Please visit this URL to authorize this application: https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=707506262186-8li17b8ftmtls5t1da3tbqjcl6.apps.googleusercontent.com&redirect_uri=urn%3Aietf%3Awg%3Aoauth%3A2.0%3Aoob&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fbigquery&state=TgyqXhRch1u2vtxhfypmhEUQcuF&prompt=consent&access_type=offline

    Enter the authorization code:  4/ywF6LRH5rJoC6f0531aNgoapZqepKtJRBOPAPMzHdF0ToBk4k

