#!/usr/bin/env python3

### Import Python libraries
import argparse
import logging
import datetime
import yaml

### Load project modules
import connections
import export_conversions
import report_gen


def main(adwords_mcc, date_from, date_until, bq_dataset, google_yaml, snow_yaml):

    logging.info("Start Google connections")
    bq_client = connections.bigquery_connection()
    gs_client = connections.storage_connection()
    adw_client = connections.adwords_api_connection(google_yaml)

    logging.info("Parsing Snowflake credentials")
    snow_creds = yaml.load(open(snow_yaml))

    logging.info("Starting DataStudio report")
    with connections.snowflake_connection(
        snow_creds['sf_account'], 
        snow_creds['sf_user'], 
        snow_creds['sf_password']
    ) as sf_client:
        report_gen.SnowflakeToBigQuery(sf_client, bq_client, bq_dataset)
        
    report_gen.AdwordsToBigQuery(
        adwords_mcc, adw_client, bq_client, bq_dataset, date_from, date_until
    )
    report_gen.JoinFinalTable(bq_client, bq_dataset, '2000-01-01', date_until)

    logging.info("Starting conversions export for Adwords")
    export_conversions.ExportConversionsAdwords(gs_client, bq_client, bq_dataset)

    logging.info("All tasks done. Have a good day!")


if __name__ == "__main__":

    ### Define logging level
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(filename)s - %(message)s',
        level=logging.INFO,
    )

    ### Get yesterday date
    yesterday = (datetime.datetime.today() - datetime.timedelta(1)).strftime("%Y-%m-%d")

    ### Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('mcc', type=str, help=("Adwords MCC or single account"))
    parser.add_argument(
        '--from',
        dest='date_begin',
        default=yesterday,
        type=str,
        help=("Beginning of period with format YYYY-MM-DD"),
    )
    parser.add_argument(
        '--to',
        dest='date_end',
        default=yesterday,
        type=str,
        help=("End of period with format YYYY-MM-DD"),
    )
    parser.add_argument(
        '--dataset', dest='bq_dataset', default='adwords', help="BigQuery dataset name"
    )
    parser.add_argument(
        '--google',
        dest='google_yaml',
        default='../googleads.yaml',
        help=("Path to YAML file for Google API credentials"),
    )
    parser.add_argument(
        '--snow',
        dest='snow_yaml',
        default='../snowflake.yaml',
        help=("Path to YAML file for Snowflake API credentials"),
    )
    args = parser.parse_args()

    logging.info("Lauching report with parameters: {}".format(args))

    ### Call to main function
    main(
        args.mcc,
        args.date_begin,
        args.date_end,
        args.bq_dataset,
        args.google_yaml,
        args.snow_yaml,
    )
