## Apache Airflow Recursive Loader Test

### About this repo

This repo contains code examples for a generic Python test script that loads all [DAGs](https://airflow.apache.org/docs/apache-airflow/stable/concepts/dags.html) from the `dags` directory in a repo and checks that pass [DAG Loader Tests](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html#dag-loader-test).

Two of the most time consuming issues I've seen with Airflow DAG in my current role are:
1. DAGs being deployed with incorrect imports
2. DAG tasks executing BigQuery SQL containing invalid code or returning unexpected values.

This repo is focused on solving the first issue. The second issue can be alleviated by using the [python-bigquery-validator package](https://github.com/tunnelWithAC/python-bigquery-validator).

### How it works

Apache Airflow DAG Loader tests ensure that your DAG does not contain a piece of code that raises error while loading. No additional code needs to be written by the user to run this test.
(Stolen directly from [here](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html#dag-loader-test))

This is a simple test to run on a single Python file when making changes but it can be made even easier by automatically loading all files containing DAG using Python and running these tests on every push to the `dags` directory.

This also helps in the case that multiple DAGs import functions or variables from a shared module and an engineer may only test the files that they have changed.


#### PyTest

The code block contains code to load all `DAG` objects with a directory and individually test that there are no issues when loading each DAG.

```python
# tests/recursive_integrity_test.py
 
# Get a list of all files in the dag directory
DAG_PATH = os.path.join(os.path.dirname(__file__), "..", "dags/**/*.py")
DAG_FILES = glob.glob(DAG_PATH, recursive=True)

@pytest.mark.parametrize("dag_file", DAG_FILES)
def test_dag_integrity(dag_file):
    module_name, _ = os.path.splitext(dag_file)
    module_path = os.path.join(DAG_PATH, dag_file)
    # Import all Python modules from the dag directory
    mod_spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(mod_spec)
    mod_spec.loader.exec_module(module)
    
    # Find all DAG objects in the loaded modules
    dag_objects = [var for var in vars(module).values() if isinstance(var, DAG)]
    
    # Individually test each DAG
    for dag in dag_objects:
        # This function will throw an error and fail the test if all packages cannot be loaded
        dag_test_cycle(dag)

```

You can run the test case above using PyTest with the following command

```
pytest tests/test_valid_dags.py
```

#### Github Actions

The `pytest` command above can be used as part of a Github Action to automatically test DAGs on each push to Github.

```
on:
  push:
jobs:
  test-valid-dags:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python 3.9
      uses: actions/setup-python@v1
      with:
        python-version: 3.9
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Run tests
      run: |
        pytest tests/test_valid_dags.py
```

![Screenshot from 2022-11-23 10-19-52](https://user-images.githubusercontent.com/10425225/203523970-e298cbba-0be6-4258-82a7-7563e6e95975.png)
