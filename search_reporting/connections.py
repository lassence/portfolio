#!/usr/bin/env python3

### Import libraries
import logging
import googleads
from google.cloud import bigquery
from google.cloud import storage
import snowflake.connector
from snowflake.connector import DictCursor


def bigquery_connection():

    try:
        bq_client = bigquery.Client()
        logging.info("BigQuery client initialized")
    except:
        logging.error("Error initializing BigQuery client")
        return
    return bq_client


def adwords_api_connection(yaml_file):

    try:
        adwords_client = googleads.adwords.AdWordsClient.LoadFromStorage(yaml_file)
        logging.info("Connected to the Adwords API")
    except:
        logging.error("Error trying to connect to the Adwords API")
        return
    return adwords_client


def storage_connection():

    try:
        gs_client = storage.Client()
        logging.info("Google Storage client initialized")
    except:
        logging.error("Error initializing BigQuery client")
        return
    return gs_client


def snowflake_connection(sf_account, sf_user, sf_password):

    try:
        sf_connex = snowflake.connector.connect(
            account=sf_account, user=sf_user, password=sf_password
        )
        sf_connex.cursor(DictCursor).execute("USE WAREHOUSE WH1")
        sf_connex.cursor(DictCursor).execute("USE DATABASE DB1")
        sf_connex.cursor(DictCursor).execute("USE SCHEMA SCH1")
        logging.info("Snowflake connection established")
    except:
        logging.error("Error establishing Snowflake connection")
        return
    return sf_connex
