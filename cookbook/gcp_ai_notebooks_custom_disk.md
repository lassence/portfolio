# Create a GCP AI Notebook with custom disk size

**Google Cloud AI Platform Notebooks** are now created with two disks (*boot* and *data*) with a minimal size of 100GB each. This 200GB space adds a few dollars on your monthly bill just for persisent disks storage, even when the instances are stopped. 

Although this is not recommended by Google for I/O performance reasons, you can bypass this requirement and create notebooks with only one, smaller disk. Follow these steps:

1. In **AI Platform > Notebook**, create a notebook with adequate options (except for disks)
2. Go to **Compute Engine > VM Instances** and click on the notebook instance that was just created
3. Click **Create similar**
4. At the bottom of the page, click the **Equivalent in command line** link
5. Customize the command, especially the *instance name* and *disk size* (`boot-disk-size=`). You should have something similar to this:

```sh
gcloud beta compute --project=my_project instances create python-224550 \
    --zone=us-west1-b \
    --machine-type=n1-standard-1 \
    --subnet=default \
    --network-tier=PREMIUM \
    --metadata=framework=NumPy/SciPy/scikit-learn,proxy-mode=service_account,shutdown-script=/opt/deeplearning/bin/shutdown_script.sh,notebooks-api=PROD,enable-guest-attributes=TRUE,proxy-url=2435da420c9ca269-dot-us-west1.notebooks.googleusercontent.com,title=Base.CPU,version=65 \
    --maintenance-policy=MIGRATE \
    --service-account=843963512106-compute@developer.gserviceaccount.com \
    --scopes=https://www.googleapis.com/auth/cloud-platform,https://www.googleapis.com/auth/userinfo.email \
    --tags=deeplearning-vm,notebook-instance \
    --image=common-cpu-notebooks-v20210301-debian-10 \
    --image-project=deeplearning-platform-release \
    --boot-disk-size=50GB \
    --boot-disk-type=pd-standard \
    --boot-disk-device-name=python-224550 \
    --no-shielded-secure-boot \
    --shielded-vtpm \
    --shielded-integrity-monitoring \
    --labels=goog-caip-notebook= \
    --reservation-affinity=any
```

6. Run the command in **Cloud Shell**.

Your custom-but-fully-operational notebook should be listed in **AI Platform > Notebook**.
