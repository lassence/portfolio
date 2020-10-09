#!/usr/bin/env python3

### Load libraries
import logging
import argparse
from google.cloud import bigquery
from google.api_core import exceptions


def create_bq_table(client, dataset_ref, table_name, schema):

    ### Table reference
    table_ref = dataset_ref.table(table_name)

    ### Delete table if exists
    try:
        client.get_table(table_ref)
        client.delete_table(table_ref)
        logging.info("Table '{}' supprimée".format(table_ref.table_id))
    except exceptions.NotFound:
        pass

    ### Create new table with specified schema
    table = bigquery.Table(table_ref, schema=schema)
    try:
        table = client.create_table(table)
        logging.info("Table '{}' créée".format(table.full_table_id))
    except:
        logging.error("La table n'a pas pu être créée")


def create_table_gclid(client, dataset_ref):

    schema = [
        bigquery.SchemaField('AccountName', 'STRING'),
        bigquery.SchemaField('CampaignName', 'STRING'),
        bigquery.SchemaField('AdGroupId', 'STRING'),
        bigquery.SchemaField('CreativeId', 'STRING'),
        bigquery.SchemaField('KeywordId', 'STRING'),
        bigquery.SchemaField('Date', 'DATE'),
        bigquery.SchemaField('Device', 'STRING'),
        bigquery.SchemaField('GclId', 'STRING'),
        bigquery.SchemaField('Clicks', 'INTEGER'),
    ]
    return create_bq_table(client, dataset_ref, 'adw_gclid_list', schema)


def create_table_adperf(client, dataset_ref):

    schema = [
        bigquery.SchemaField('AccountDescriptiveName', 'STRING'),
        bigquery.SchemaField('CampaignName', 'STRING'),
        bigquery.SchemaField('CampaignId', 'STRING'),
        bigquery.SchemaField('AdGroupName', 'STRING'),
        bigquery.SchemaField('AdGroupId', 'STRING'),
        bigquery.SchemaField('AdGroupStatus', 'STRING'),
        bigquery.SchemaField('CreativeId', 'STRING'),
        bigquery.SchemaField('KeywordId', 'STRING'),
        bigquery.SchemaField('Device', 'STRING'),
        bigquery.SchemaField('Date', 'DATE'),
        bigquery.SchemaField('Cost', 'FLOAT'),
        bigquery.SchemaField('Impressions', 'INTEGER'),
        bigquery.SchemaField('Clicks', 'INTEGER'),
        bigquery.SchemaField('Conversions', 'FLOAT'),
        bigquery.SchemaField('AveragePosition', 'STRING'),
    ]
    return create_bq_table(client, dataset_ref, 'adw_keywords', schema)


def create_table_kwnames(client, dataset_ref):

    schema = [
        bigquery.SchemaField('AccountDescriptiveName', 'STRING'),
        bigquery.SchemaField('AdGroupId', 'STRING'),
        bigquery.SchemaField('Keyword', 'STRING'),
        bigquery.SchemaField('MatchType', 'STRING'),
        bigquery.SchemaField('KeywordId', 'STRING'),
    ]
    return create_bq_table(client, dataset_ref, 'adw_kw_names', schema)


def create_table_final(client, dataset_ref):

    schema = [
        bigquery.SchemaField('Site', 'STRING'),
        bigquery.SchemaField('AccountName', 'STRING'),
        bigquery.SchemaField('CampaignName', 'STRING'),
        bigquery.SchemaField('CampaignType', 'STRING'),
        bigquery.SchemaField('Partner', 'STRING'),
        bigquery.SchemaField('AdGroupName', 'STRING'),
        bigquery.SchemaField('CreativeId', 'STRING'),
        bigquery.SchemaField('Keyword', 'STRING'),
        bigquery.SchemaField('Device', 'STRING'),
        bigquery.SchemaField('Date', 'DATE'),
        bigquery.SchemaField('Cost', 'FLOAT'),
        bigquery.SchemaField('Impressions', 'INTEGER'),
        bigquery.SchemaField('Clicks', 'INTEGER'),
        bigquery.SchemaField('ConversionsAdw', 'FLOAT'),
        bigquery.SchemaField('AveragePosition', 'FLOAT'),
        bigquery.SchemaField('Orders', 'INTEGER'),
        bigquery.SchemaField('Revenue', 'FLOAT'),
        bigquery.SchemaField('SalesValue', 'FLOAT'),
    ]
    return create_bq_table(client, dataset_ref, 'final_report', schema)


def main(dataset, gclid, adperf, kwnames, final, snow):

    ### Initializes BigQuery object
    client = bigquery.Client()
    dataset_ref = client.dataset(dataset)

    ### Creates specified tables
    if gclid == True:
        create_table_gclid(client, dataset_ref)
    if adperf == True:
        create_table_adperf(client, dataset_ref)
    if kwnames == True:
        create_table_kwnames(client, dataset_ref)
    if final == True:
        create_table_final(client, dataset_ref)


if __name__ == '__main__':

    ### Initialize logging
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(filename)s - %(message)s',
        level=logging.INFO,
    )

    ### Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('dataset', help="Dataset name")
    parser.add_argument(
        '--gclid', action='store_true', help="Create table for GCLID list"
    )
    parser.add_argument(
        '--adperf', action='store_true', help="Create table for AD PERFORMANCE stats"
    )
    parser.add_argument(
        '--kwnames', action='store_true', help="Create table for KEYWORDS NAMES"
    )
    parser.add_argument(
        '--final', action='store_true', help="Create table for FINAL report"
    )
    args = parser.parse_args()

    ### Call to main function
    main(args.dataset, args.gclid, args.adperf, args.kwnames, args.final)
