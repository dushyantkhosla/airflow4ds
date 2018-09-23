## Airflow

- Initialize a new directory that contains a `dags/` folder
- Set the `AIRFLOW_HOME` to point to the directory that contains your `dags/` folder
  - `export AIRFLOW_HOME=$(pwd)`
- Run `airflow initdb`
  - This will create some new files `airflow.cfg, airflow.db, uniitests.cfg`
- Set `load_examples` in `airflow.cfg` to False
  - Run `airflow resetdb` to implement changes made to the config file
- Airflow uses `mysql` for the distributed scheduler
- Start the webserver with `airflow webserver`
- Start the scheduler with `airflow scheduler`
- Start a worker with `airflow worker`

## DAGs

- We define the `start_date` inside the `default_args` dict that is passed to the `DAG()` constructor along with the `schedule_interval`
  - NOTE: The `start_date` needs to be set at least one interval behind for the scheduler to run the DAG
  - Other important things we need to set are `depends_on_past`, `retries` and `retry_delay`
- Once constructed, DAGs are filled using the `.set_upstream` and `.set_downstream` methods of Tasks  
- `SubDag`s are essentially their own DAGs which are general and can be re-used as utilities
  - These are instantiated with the `SubDagOperator`
  - Need to be defined in their own `subdags/` folder so they're not automatically picked up and scheduled
  - We specify a `trigger_rule` to specify when or how the SubDag should run
- Check DAGs with
  - `airflow list_dags`
- DAGs can be tested as
  - `aiflow test <dag-name> <task-name> <parameters>`
- Manually trigger the DAG as
    - `airflow trigger_dag <dag-name>`  

## Operators and Tasks

- *Operators* categorised into 3 types
  - `Action`: perform a task with the data/pipeline
  - `Transfer`: move data in the pipeline
  - `Sensor`: test to determine if a particular state or requirement has been reached
- Tasks are created by instantiating an Operator
  - always specify a the `dag` and a `task_id`
  - Other parameters will depend on the type of Operator being used
    - For example, a `PythonOperator` will require a `python_callable` which is just a function defined either in the same module, or imported from another

## Branching

- The `BranchPythonOperator` returns a string, and that should match a `task_id`
- This is to ensure that there's a Task for every branch of the operator
- As a general rule, any Branching operator will work in this fashion


## Connections

- In the UI, go to Admin -> Connections
  - Use `Create` to make a connection to your data store
