#!/usr/bin/env python3

### Load libraries
import logging
import io
import datetime
import pandas as pd
from snowflake.connector import DictCursor
from google.cloud import bigquery
from googleads import adwords


class SnowflakeToBigQuery:
    def __init__(self, sf_connex, bq_client, dataset_name):

        logging.info("Initializing module")

        self.query, self.dest_table_name = self.get_query()
        self.sf_report_data = self.get_snowflake_data(sf_connex, self.query)
        self.load_report_to_bq(
            bq_client, dataset_name, self.dest_table_name, self.sf_report_data
        )

    def get_query(self):

        start_date = '2018-01-01'
        query = """
        SELECT
            TO_TIMESTAMP_NTZ(REGEXP_SUBSTR(TRACKING_UTMZ, '^[0-9]+\.([0-9]+)\.', 1, 1, 'e')) AS CLICK_TIMESTAMP,
            SALEDATE,
            TRACKING_GCLID,
            ORDERS,
            REVENUE,
            SALES_VALUE
        FROM ADWORDS_GCLID_AGGREGATION
        WHERE
            NB_ORDERS > 0 
            AND CLICK_TIMESTAMP >= '{0}'
        """.format(
            start_date
        )
        dest_table_name = 'snow_conversions'

        return query, dest_table_name

    def get_snowflake_data(self, sf_connex, query):

        logging.info("Firing Snowflake query")
        df = pd.DataFrame(sf_connex.cursor(DictCursor).execute(query).fetchall())
        report_data = io.StringIO()
        df.to_csv(report_data, index=False)

        logging.info("Snowflake query finished")
        return report_data

    def load_report_to_bq(self, bq_client, dataset_name, dest_table_name, report_data):

        dataset_ref = bq_client.dataset(dataset_name)
        job_config = bigquery.LoadJobConfig()
        job_config.write_disposition = 'WRITE_TRUNCATE'
        job_config.source_format = bigquery.SourceFormat.CSV
        job_config.skip_leading_rows = 1
        job_config.autodetect = True

        report_data.seek(0)
        with report_data as source:
            load_job = bq_client.load_table_from_file(
                source, dataset_ref.table(dest_table_name), job_config=job_config
            )
            logging.info(
                "Loading report data to BigQuery table '{}.{}'".format(
                    dataset_name, dest_table_name
                )
            )

        load_job.result()
        logging.info(
            "Loading to table '{}.{}' done".format(dataset_name, dest_table_name)
        )


class AdwordsToBigQuery:
    def __init__(
        self, account, adw_client, bq_client, dataset_name, date_begin, date_end
    ):

        logging.info("Initializing module")

        ### Get list of accounts
        self.accounts = self.get_all_accounts(adw_client, account)
        logging.info("List of accounts: {}".format(self.accounts))

        ### Make Adwords API calls for each account
        for account_id in self.accounts:
            logging.info("Processing account {}".format(account_id))

            ### Ad Performance report
            self.kw_report_data = self.get_ad_performance_report(
                adw_client, account_id, date_begin, date_end
            )
            self.load_report_to_table(
                bq_client, dataset_name, 'adw_keywords', self.kw_report_data
            )

            ### Keywords names & IDs
            self.kw_names = self.get_keywords_names(adw_client, account_id)
            self.load_report_to_table(
                bq_client, dataset_name, 'adw_kw_names', self.kw_names
            )

            ### Gclid reports (one for each day)
            for date in self.get_period_dates(date_begin, date_end):
                self.gclid_report_data = self.get_gclid_report_oneday(
                    adw_client, account_id, date
                )
                self.load_report_to_table(
                    bq_client, dataset_name, 'adw_gclid_list', self.gclid_report_data
                )

    def get_all_accounts(self, adw_client, account):

        ### Initialize appropriate service.
        managed_customer_service = adw_client.GetService(
            'ManagedCustomerService', version='v201809'
        )

        ### Construct selector to get all accounts.
        page_size = 500
        offset = 0
        selector = {
            'fields': ['CustomerId', 'Name'],
            'paging': {'startIndex': str(offset), 'numberResults': str(page_size)},
        }
        more_pages = True
        child_links = {}

        ### Browse through accounts
        while more_pages:
            page = managed_customer_service.get(selector)
            if 'entries' in page and page['entries']:
                if 'links' in page:
                    for link in page['links']:
                        if link['managerCustomerId'] not in child_links:
                            child_links[link['managerCustomerId']] = []
                        child_links[link['managerCustomerId']].append(link)
            offset += page_size
            selector['paging']['startIndex'] = str(offset)
            more_pages = offset < int(page['totalNumEntries'])

        ### Check if account is an MCC, otherwise just return the provided account ID
        mcc = int(str(account).replace('-', ''))
        if int(mcc) in child_links:
            accounts_list = [i['clientCustomerId'] for i in child_links[int(mcc)]]
        else:
            accounts_list = [mcc]

        return accounts_list

    def load_report_to_table(self, bq_client, dataset_name, table_name, report_data):

        dataset_ref = bq_client.dataset(dataset_name)
        job_config = bigquery.LoadJobConfig()
        job_config.source_format = bigquery.SourceFormat.CSV

        report_data.seek(0)
        with report_data as source:
            load_job = bq_client.load_table_from_file(
                source, dataset_ref.table(table_name), job_config=job_config
            )

        load_job.result()
        logging.info("Data loaded to table '{}.{}'".format(dataset_name, table_name))

    def get_ad_performance_report(self, adw_client, account_id, date_begin, date_end):

        ### Initialize appropriate service
        adw_client.SetClientCustomerId(account_id)
        report_downloader = adw_client.GetReportDownloader(version='v201809')

        ### Construct query
        report = {
            'reportName': 'Last X days AD_PERFORMANCE_REPORT',
            'dateRangeType': 'CUSTOM_DATE',
            'reportType': 'AD_PERFORMANCE_REPORT',
            'downloadFormat': 'CSV',
            'selector': {
                'fields': [
                    'AccountDescriptiveName',
                    'CampaignName',
                    'CampaignId',
                    'AdGroupName',
                    'AdGroupId',
                    'AdGroupStatus',
                    'Id',  # Ad Id
                    'CriterionId',  # Keyword Id
                    'Device',
                    'Date',
                    'Cost',
                    'Impressions',
                    'Clicks',
                    'Conversions',
                    'AveragePosition',
                ],
                'dateRange': {'min': date_begin, 'max': date_end},
            },
        }

        ### Retrieve the report content and return it as StringIO object
        try:
            report_data = io.StringIO()
            report_downloader.DownloadReport(
                report,
                report_data,
                skip_report_header=True,
                skip_column_header=True,
                skip_report_summary=True,
                include_zero_impressions=False,
            )
            return report_data
        except:
            logging.error("Error: could not generate report")
            return

    def get_keywords_names(self, adw_client, account_id):

        ### Initialize appropriate service
        adw_client.SetClientCustomerId(account_id)
        report_downloader = adw_client.GetReportDownloader(version='v201809')

        ### Construct query
        report = {
            'reportName': 'Last X days KEYWORDS_PERFORMANCE_REPORT',
            'dateRangeType': 'CUSTOM_DATE',
            'reportType': 'KEYWORDS_PERFORMANCE_REPORT',
            'downloadFormat': 'CSV',
            'selector': {
                'fields': [
                    'AccountDescriptiveName',
                    'AdGroupId',
                    'Criteria',
                    'KeywordMatchType',
                    'Id',
                ],
                'dateRange': {'min': '2018-01-01'},
            },
        }

        ### Retrieve the report content and return it as StringIO object
        try:
            report_data = io.StringIO()
            report_downloader.DownloadReport(
                report,
                report_data,
                skip_report_header=True,
                skip_column_header=True,
                skip_report_summary=True,
                include_zero_impressions=False,
            )
            return report_data
        except:
            logging.error("Error: could not generate report")
            return

    def get_gclid_report_oneday(self, adw_client, account_id, date):

        ### Initialize appropriate service
        adw_client.SetClientCustomerId(account_id)
        report_downloader = adw_client.GetReportDownloader(version='v201809')

        ### Construct query
        report = {
            'reportName': 'CLICK_PERFORMANCE_REPORT',
            'dateRangeType': 'CUSTOM_DATE',
            'reportType': 'CLICK_PERFORMANCE_REPORT',
            'downloadFormat': 'CSV',
            'selector': {
                'fields': [
                    'AccountDescriptiveName',
                    'CampaignName',
                    'AdGroupId',
                    'CreativeId',
                    'CriteriaId',  # Keyword ID
                    'Date',
                    'Device',
                    'GclId',
                    'Clicks',
                ],
                'dateRange': {'min': date, 'max': date},
            },
        }

        ### Retrieve the report content and return it as StringIO object
        try:
            report_data = io.StringIO()
            report_downloader.DownloadReport(
                report,
                report_data,
                skip_report_header=True,
                skip_column_header=True,
                skip_report_summary=True,
                include_zero_impressions=False,
            )
            return report_data
        except:
            logging.error("Error: could not generate report")
            return

    def get_period_dates(self, date_begin, date_end):

        ### Convert to datetime types
        date_begin = datetime.datetime.strptime(date_begin, "%Y-%m-%d").date()
        date_end = datetime.datetime.strptime(date_end, "%Y-%m-%d").date()

        ### Gclid reports cannot be generated more than 90 days back.
        ### Check if period is not more than 90 days back.
        ### Otherwise, try to constraint the period; if not possible, throw an error.
        if (datetime.date.today() - date_begin).days > 90:
            if (datetime.date.today() - date_end).days > 90:
                raise Exception(
                    "Gclid report can not be retrieved for more than 90 days back."
                )
            else:
                date_begin = datetime.date.today() - datetime.timedelta(90)
                logging.info(
                    "Gclid report can not be retrieved for more than 90 days back.\n \
                    Report period reduced to: {} to {}".format(
                        date_begin, date_end
                    )
                )

        ### Calculate time delta
        delta = date_end - date_begin

        ### Returns a list with every date in the period
        dates_list = []
        for i in range(delta.days + 1):
            dates_list.append(str((date_begin + datetime.timedelta(days=i))))

        return dates_list


class JoinFinalTable:
    def __init__(self, bq_client, dataset_name, date_begin, date_end):

        logging.info("Initializing module")
        self.join_final_table(
            bq_client, dataset_name, 'final_report', date_begin, date_end
        )

    def join_final_table(
        self, bq_client, dataset_name, dest_table_name, date_begin, date_end
    ):

        dataset_ref = bq_client.dataset(dataset_name)
        table_ref = dataset_ref.table(dest_table_name)
        job_config = bigquery.QueryJobConfig()
        job_config.destination = table_ref
        job_config.write_disposition = 'WRITE_TRUNCATE'

        query = """
        WITH gclid AS (
            SELECT *
            FROM `{2}.adw_gclid_list` AS a
            INNER JOIN (
                SELECT *
                FROM `{2}.snow_conversions`
                WHERE
                    TRACKING_GCLID IS NOT NULL
                    AND NB_ORDERS > 0
            ) AS b
            ON a.GCLID = b.TRACKING_GCLID
        ),
        kwnames AS (
            SELECT DISTINCT
                AdGroupId, 
                KeywordId,
                Keyword
            FROM `{2}.adw_kw_names`
        )

        SELECT
            CASE
                WHEN kw.AccountDescriptiveName LIKE 'Site1%' THEN 'ST1'
                WHEN kw.AccountDescriptiveName LIKE 'Site2%' THEN 'ST2'
                ELSE 'Other'
            END AS Site,
            kw.AccountDescriptiveName AS AccountName,
            kw.CampaignName AS CampaignName,
            REGEXP_EXTRACT(kw.CampaignName, r"^([A-Z]{{2,6}})-") AS CampaignType,
            LOWER(REGEXP_EXTRACT(kw.CampaignName, r"^[A-Z]{{2,6}}-([A-Za-z'_\.]+)-")) AS Partner,
            kw.AdGroupName AS AdGroupName,
            kw.CreativeId AS CreativeId,
            kwnames.Keyword AS Keyword,
            kw.Device AS Device,
            FORMAT_DATE("%Y%m%d", kw.Date) AS Date,
            kw.Cost/1000000 AS Cost,
            kw.Impressions AS Impressions,
            kw.Clicks AS Clicks,
            kw.Conversions AS Conversions,
            SAFE_CAST(kw.AveragePosition AS FLOAT64) AS AveragePosition,
            SUM(gclid.ORDERS) AS Orders,
            ROUND(SUM(gclid.REVENUE), 4) AS Revenue,
            ROUND(SUM(gclid.SALES_VALUE), 4) AS SalesValue

        FROM `{2}.adw_keywords` AS kw

        LEFT JOIN gclid
        ON
            kw.AdGroupId = gclid.AdGroupId
            AND kw.CreativeId = gclid.CreativeId
            AND kw.KeywordId = gclid.KeywordId
            AND kw.Date = gclid.Date
            AND kw.Device = gclid.Device

        LEFT JOIN kwnames
        ON
            kw.AdGroupId = kwnames.AdGroupId
            AND kw.KeywordId = kwnames.KeywordId

        WHERE kw.Date BETWEEN '{0}' AND '{1}'

        GROUP BY 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15;
        """.format(
            date_begin, date_end, dataset_name
        )

        logging.info("Firing BigQuery query")
        query_job = bq_client.query(query, job_config=job_config)
        query_job.result()
        logging.info(
            "Query results loaded to table '{}.{}'".format(
                dataset_name, dest_table_name
            )
        )

