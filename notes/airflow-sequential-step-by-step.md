# Airflow Sequential

- `git clone` your project code and `cd` into it
- Create a Python environment and activate it
- Install Airflow
- Set the environment variable 
  `export AIRFLOW_HOME=$(pwd)/airflow`
- Run `airflow version` to confirm
- Check out `airflow.cfg` under `AIRFLOW_HOME`
  - Check `dags_folder` and create it if it doesn't exist
  - Set `load_examples = False`
- Move your local Python modules under `AIRFLOW_HOME`
  - Directories `dags/` and `src/` should be at the same level
- Create Python files under `dags/` to store your workflows. All DAG objects within these files will be discovered by the Airflow Scheduler and visible on the UI.
- DAG files should contain declarations for
  - `default_args` which will be inherited by all `Tasks`. 
    Read about the `BaseOperator` for more.
    At the very least, specify `start_date`
  - instantiating a `DAG` object
    - specify the `schedule_interval` here
  - importing Python modules, SQL scripts or Jinja templates that will be used
  - instantiating `Task` objects using `Operator` classes
    - Types of Operators - Action, Sensor
  - Workflow order using the `.set_upstream` or `.set_downstream` methods of `Task`s
- From the Terminal, run `airflow list_dags`
  - This will import all `DAG` declarations in `.py` files under the `/dags` directory into a `DagBag`
  - If there are errors or issues in the Python code, they will be raised here
- If the DAGs are successfully collected, run `airflow initdb`
- Then, start the scheduler with `airflow scheduler &> /dev/null &`
- Then, start the UI with `airflow webserver &> /dev/null &`
- Go to `localhost:8080` to access the UI
- Switch on the `DAG` and trigger a manual run to see the workflow in action!

## Gotchas

- If you run `airflow [subcommand]` from different terminals, ensure that your environment is active and the `AIRFLOW_HOME` variable is set.