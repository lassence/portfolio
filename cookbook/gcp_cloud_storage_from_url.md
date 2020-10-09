# Copy files from URL to Google Cloud Storage

When you want to store large files but have a poor Internet connection, it is convenient to directly copy files from their distant URL to a cloud location, rather than having to download them on your computer and upload them again to their final storage location.

One simple solution is to use **[Google Cloud Storage](https://cloud.google.com/storagehttps://cloud.google.com/storage)**. This require that you have a GCP account and an active project.

Do the following:
1. Create a **Cloud Storage bucket**, or make sure you have one.
2. Start a **Cloud Shell** window.
3. Type the following:

```sh
curl https://www.example.com/largefile.txt | gsutil cp - gs://my_bucket/largefile.txt
```

The file will be copied from the source URL to the Cloud Storage bucket at the maximum speed that the source website can deliver. 
