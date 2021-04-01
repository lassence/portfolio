# Schedule start and stop for a Google Compute Engine instance

**March 2021 update:** you can now easily schedule VM instances start and/or stop with the **Instances Schedule** feature (see [documentation](https://cloud.google.com/compute/docs/instances/schedule-instance-start-stop)).

***

Cronjobs are a simple and reliable way to periodically execute scripts on a virtual machine. However, to avoid having your virtual instance running all the time - and being charged for it - we can configure Google Cloud to start the GCE instance a few minute before the cronjob are executed, and to power it off afterwards.

We will use the following architecture:

![](https://cloud.google.com/scheduler/docs/images/scheduling-instances-architecture-pubsub.png)

Instructions for this architecture come from the [GCP support website](https://cloud.google.com/scheduler/docs/scheduling-instances-with-cloud-scheduler).

## Configure cron jobs on the GCE instance

1. Edit the crontab file:

```sh
crontab -e
```

2. Schedule your script to run every day at a specific time (05:35 GMT in this example).
Be careful with possible timezone differences between the VM and the Google schedule job.

```sh
35 05 * * * python3 /home/sweethome/my_script.py
```

See [unix-cron format](https://cloud.google.com/scheduler/docs/configuring/cron-job-schedules#defining_the_job_schedule)
for more info on scheduling cron tasks.

3. Verify that the cronjob has been saved with: `crontab -l`

## Add label to the Google Compute Engine instance

In the **Google Cloud Console**, go to **Compute Engines > VM Instances**. Edit the VM instance that will be used for the scheduled reporting, and add the following label (for example):
- *key*: `update`
- *value*: `daily`

## Set up the Cloud Functions

In the Console, go to **Cloud Functions**.

Create the start function:

1. Create a new function and name it `startInstancePubSub`
2. For **Trigger**, select `Cloud Pub/Sub`
3. For **Topic**, create a new topic and call it `start-vm`
4. For **Runtime**, select `Node.js 8`
5. On the `index.js` tab, copy and paste [this code](https://github.com/GoogleCloudPlatform/nodejs-docs-samples/blob/master/functions/scheduleinstance/index.js)
6. On the `package.json` tab, copy and paste [this code](https://github.com/GoogleCloudPlatform/nodejs-docs-samples/blob/master/functions/scheduleinstance/package.json)
7. For **Function to execute**, enter `startInstancePubSub`.
8. Click **Create**

Create the stop function:

1. Create a new function and name it `stopInstancePubSub`
2. For **Trigger**, select `Cloud Pub/Sub`
3. For **Topic**, create a new topic and call it `stop-vm`
4. For **Runtime**, select `Node.js 8`
5. On the `index.js` tab, copy and paste [this code](https://github.com/GoogleCloudPlatform/nodejs-docs-samples/blob/master/functions/scheduleinstance/index.js)
6. On the `package.json` tab, copy and paste [this code](https://github.com/GoogleCloudPlatform/nodejs-docs-samples/blob/master/functions/scheduleinstance/package.json)
7. For **Function to execute**, enter `stopInstancePubSub`.
8. Click **Create**

Verify that the functions work with [these instructions](https://cloud.google.com/scheduler/docs/scheduling-instances-with-cloud-scheduler#optional_verify_the_functions_work)

## Set up the Cloud Scheduler jobs

In the Console, go to **Cloud Scheduler**.

Create the start job

1. Create a new **Job** and name it `start-rmn-vm`
2. For **Frequency**, enter a time ~5 minutes before the cronjob time on the GCE instance
For example, if the cronjob is defined at 06:35, enter `30 6 * * *`
3. For **Target** select `Pub/Sub`, and for Topic enter `start-vm`
4. For **Payload**, enter the following: `{"zone":"europe-west1-d","label":"update=daily"}`
5. Click **Create**

Create the stop job

1. Create a new **Job** and name it `stop-rmn-vm`
2. For **Frequency**, enter a time sufficiently after the cronjob time on the GCE instance.
For example, if the cronjob is defined at 06:35, enter `0 7 * * *` to schedule the shutdown 25 minutes afterwards.
3. For **Target** select `Pub/Sub`, and for Topic enter `stop-vm`
4. For **Payload**, enter the following: `{"zone":"europe-west1-d","label":"update=daily"}`
5. Click **Create**

Verify that the events work correctly with [these instructions](https://cloud.google.com/scheduler/docs/scheduling-instances-with-cloud-scheduler#optional_verify_the_jobs_work)
