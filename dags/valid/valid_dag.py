from datetime import datetime
from airflow import models
from airflow.contrib.operators.bigquery_operator import BigQueryOperator


with models.DAG('bigquery_example',
        schedule_interval='0 12 * * *',
        start_date=datetime(2021, 8, 20),
        default_args={
            'params': {
                'project': 'bigquery-public-data'
            }
        },
        catchup=True) as dag:


    example_query = BigQueryOperator(
                        task_id='example_query',
                        sql='select count(*) from `{{ params.project }}.iowa_liquor_sales.sales`'
                    )

    example_query_from_file = BigQueryOperator(
                        task_id='example_query_from_file',
                        sql='select count(*) from `{{ params.project }}.iowa_liquor_sales.sales`'
                    )

    example_query

    example_query_from_file
