# Cloud-based JupyterLab with Google Cloud AI Notebooks

Since 2019, I have been extensively using Google cloud-based JupyterLab instances, **AI Platform Notebooks**. While there are other solutions to host Jupyter notebooks on GCP, like installing Jupyter on a Compute Engine instance or [Colab](https://colab.research.google.com), I find AI Platform Notebooks very convenient. They are simple to create, powerful and reliable.

You can have multiple instances depending on your projects needs, with different machine configurations (CPU, Memory, Disk size, GPU, etc.) and pre-packaged environment (Python 3, Tensorflow...). If you need extra power for a computationally intensive task, you can beef up your machine config just for the time needed, and scale it down when finished.

You can install new Python packages for testing, without worrying about messing up with your local pip or conda environment. Just save your files, and create a new instance to start with a fresh environment.

## Create your AI Platform Notebook instance

* In the GCP Console, select **AI Platform > Notebooks**.
* Click **New Instance** and select an environment. I usually go with *Python*.
* On the configuration panel, click **Customize** to display more options. Some parameters to consider:
  * **Region** and **Zone**: closer to your location will be faster. 
  * **Machine Configuration**: this will impact the hourly price (you are only billed when instances are running), but you can change it afterwards.
  * **Boot disk**: a Standard Persistent Disk with 100GB is usually sufficient.
* Click **Create**

After a few moments, your instance will be ready. Click on **Open JupyterLab** to start using it. 

## Set up your environment

AI Platform Notebooks run standard JupyterLab instances, so you should be familiar with the environment.

Open a **Terminal** window to check the Python version: `python3 --version`. It may not be the latest available version, so be aware of potential compatibility issues with your previous work.

I use AI Notebooks as disposable instances, so I always save my work to Git. You can set up Git in the **Terminal**, and then use the **Git** tab in the left menu to sync your work.

When you are finished, do not forget to *turn off your instance* or you will be billed for useless hours: **AI Platform > Notebooks**, select your instance and click **Stop**.
