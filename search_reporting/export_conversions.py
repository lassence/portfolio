#!/usr/bin/env python3

### Load libraries
import logging
import io
import pandas as pd
from google.cloud import bigquery
from google.cloud import storage


class ExportConversionsAdwords:
    def __init__(self, gs_client, bq_client, dataset_name):

        logging.info("Initializing module")
        self.bucket_name = 'client_bucket'
        self.blob_name = 'adwords_conversions.csv'

        self.bq_results = self.get_conversions_from_bq(bq_client, dataset_name)
        self.io_object = self.transform_results(self.bq_results)
        self.upload_to_gs(gs_client, self.io_object, self.bucket_name, self.blob_name)

    def get_conversions_from_bq(self, bq_client, dataset_name):

        ### Build the query to export conversions list
        sql = """
            SELECT
                TRACKING_GCLID AS GclId,
                DATETIME_ADD(DATETIME(SALEDATE), INTERVAL 86399 SECOND) AS ConversionTime,
                REVENUE AS ConversionValue
            FROM `{0}.snow_conversions`
            WHERE
                REVENUE > 0
                AND SALEDATE < CURRENT_DATE()
            ORDER BY SALEDATE DESC
            LIMIT 2000
        """.format(
            dataset_name
        )

        ### Fire query to BigQuery
        logging.info("Firing BigQuery query")
        query_job = bq_client.query(sql)
        query_results = query_job.result()

        ### Load query results into a list
        bq_list = []
        for row in query_results:
            bq_list.append(list(row))
        logging.info("Query results saved")
        return bq_list

    def transform_results(self, bq_list):

        logging.info("Transforming query results")

        ### Create DataFrame from list
        df = pd.DataFrame(
            bq_list, columns=['Google Click ID', 'Conversion Time', 'Conversion Value']
        )
        df['Conversion Name'] = 'Commissions'
        df['Conversion Currency'] = 'EUR'

        ### Create IO object and add header row
        io_object = io.StringIO()
        header_row = ["Parameters:TimeZone=Europe/Paris,,,,\n"]
        io_object.writelines(header_row)

        ### Write DataFrame to IO object
        df.to_csv(
            io_object,
            index=False,
            columns=[
                'Google Click ID',
                'Conversion Name',
                'Conversion Time',
                'Conversion Value',
                'Conversion Currency',
            ],
        )
        return io_object

    def upload_to_gs(self, gs_client, io_object, bucket_name, blob_name):

        ### Define variables
        bucket = gs_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)

        ### Upload blob
        io_object.seek(0)
        blob.upload_from_file(io_object)

        ### Make public
        blob.make_public()
        logging.info("Blob modified and accessible at '{}'".format(blob.public_url))
        return blob.public_url
