# Setup instructions for Google Cloud

This document describes how to implement the Adwords API to BigQuery scripts 
using a Google Compute Engine (GCE) instance and the GCP scheduling process.

## Set up the GCE instance

A Google Compute Engine (GCE) instance must be deployed with Debian 9.

First, install `pip3` and the necessary Google [Python libraries](https://cloud.google.com/python/docs/reference/):

```sh
sudo apt update
sudo apt install python3-pip
pip3 install google
pip3 install google-cloud
pip3 install google-cloud-bigquery
pip3 install googleads
```

To deploy the scripts, we will pull the latest version from Git. 
On a new GCE instance, `git` needs to be installed:

```sh
sudo apt install git
```

## Import the scripts on the GCE instance

1. Clone the Git repository to the GCE instance. 

```sh
git clone https://github.com/alecness/search_reporting.git
cd search-reporting
```

2. Create a `googleads.yaml` file with the Adwords API credentials 
and a `snowflake.yaml` with Snowflake credentials.

3. Verify that the scripts run as expected, on a test dataset.

## Configure cron job on the GCE instance

1. Edit the crontab file:

```sh
crontab -e
```

2. Schedule the `launcher.py` script to run every day at a specific time (05:35 GMT in this example).

```sh
35 05 * * * python3 /home/report/search-reporting/launcher.py 12345678 --google /home/report/googleads.yaml --snow /home/report/snowflake.yaml >> /home/user/cron.log 2>&1
```

See [unix-cron format](https://cloud.google.com/scheduler/docs/configuring/cron-job-schedules#defining_the_job_schedule)
for more info on scheduling cron tasks.

3. Verify that the cronjob has been saved with: `crontab -l`


## Schedule GCE start and shutdown

To avoid having a GCE instance running all the time - and being charged for it - 
we can configure Google Cloud to start the GCE instance a few minute before 
the cronjob are executed, and to power it off afterwards.

We will use the following architecture:

![](https://cloud.google.com/scheduler/docs/images/scheduling-instances-architecture-pubsub.png)

All instructions for this architecture come from this [GCP support page](https://cloud.google.com/scheduler/docs/scheduling-instances-with-cloud-scheduler).

### Set up the Cloud Functions

Create the **Start** function:

1. Create a new [function](https://console.cloud.google.com/functions) 
and name it `startInstancePubSub`
2. For **Trigger**, select `Cloud Pub/Sub`
3. For **Topic**, create a new topic and call it `start-vm`
4. For **Runtime**, select `Node.js 6`
5. On the `index.js` tab, copy and paste the [following code](https://github.com/GoogleCloudPlatform/nodejs-docs-samples/blob/master/functions/scheduleinstance/index.js)
6. On the `package.json` tab, copy and paste the [following code](https://github.com/GoogleCloudPlatform/nodejs-docs-samples/blob/master/functions/scheduleinstance/package.json)
7. For **Function to execute**, enter `startInstancePubSub`.
8. Click **Create**

Create the **Stop** function:

1. Create a new [function](https://console.cloud.google.com/functions) 
and name it `stopInstancePubSub`
2. For **Trigger**, select `Cloud Pub/Sub`
3. For **Topic**, create a new topic and call it `stop-vm`
4. For **Runtime**, select `Node.js 6`
5. On the `index.js` tab, copy and paste the [following code](https://github.com/GoogleCloudPlatform/nodejs-docs-samples/blob/master/functions/scheduleinstance/index.js)
6. On the `package.json` tab, copy and paste the [following code](https://github.com/GoogleCloudPlatform/nodejs-docs-samples/blob/master/functions/scheduleinstance/package.json)
7. For **Function to execute**, enter `stopInstancePubSub`.
8. Click **Create**

Verify that the functions work with [these instructions](https://cloud.google.com/scheduler/docs/scheduling-instances-with-cloud-scheduler#optional_verify_the_functions_work)

### Set up the Cloud Scheduler jobs

Create the **Start** job

1. Create a new [**Job**](https://console.cloud.google.com/cloudscheduler) 
and name it `start-vm`
2. For **Frequency**, enter a time 5 minutes before the cronjob time on the GCE instance
For example, if the cronjob is defined at 06:35, enter `30 6 * * *`
3. For **Target** select `Pub/Sub`, and for Topic enter `start-vm`
4. For **Payload**, enter the following: `{"zone":"europe-west1-d","instance":"vm1"}`
5. Click **Create**

Create the **Stop** job

1. Create a new [**Job**](https://console.cloud.google.com/cloudscheduler) 
and name it `stop-vm`
2. For **Frequency**, enter a time ~30 minutes after the cronjob time on the GCE instance
For example, if the cronjob is defined at 06:35, enter `0 7 * * *`
3. For **Target** select `Pub/Sub`, and for Topic enter `stop-vm`
4. For **Payload**, enter the following: `{"zone":"europe-west1-d","instance":"vm1"}`
5. Click **Create**

Verify that the events work correctly with [these instructions](https://cloud.google.com/scheduler/docs/scheduling-instances-with-cloud-scheduler#optional_verify_the_jobs_work)
