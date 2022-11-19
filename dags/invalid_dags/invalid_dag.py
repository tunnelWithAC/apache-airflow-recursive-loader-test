# from datetime import datetime
# from airflow import models
# from airflow.operators.dummy_operator import DummyOperator
# from airflow.operators.python_operator import PythonOperator


# with models.DAG('hello_world',
#         description='Hello World DAG',
#         schedule_interval='0 12 * * *',
#         start_date=datetime(2021, 8, 20),
#         catchup=False) as dag:


#     hello_operator = PythonOperator(task_id='hello_task',
#                                     # this function doesn't exist so the DAG is not valid
#                                     python_callable=print_hello
#                                     )

#     hello_operator
