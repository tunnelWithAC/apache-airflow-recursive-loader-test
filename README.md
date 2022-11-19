## Apache Airflow Recursive Integrity Test

This repo contains code examples for a generic Python test script that loads all [DAGs](https://airflow.apache.org/docs/apache-airflow/stable/concepts/dags.html) from the `dags` directory in a repo and checks that pass [DAG Loader Tests](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html#dag-loader-test).

Two of the most time consuming issues I've seen with Airflow DAG in my current role are:
1. DAGs being deployed with incorrect imports
2.  

[DAG validation testing](https://docs.astronomer.io/learn/testing-airflow#dag-validation-testing)