[TOC]

# ETL with Airflow 1.8

When you work for a fairly large organization that has a large number of data sources, calculation processes, a bit of data science and maybe even big data, ad-hoc scheduling approaches with `cron` eventually create a tangled mess of data problems, inconsistencies and downstream problems that are hard to debug.

Airflow follows a meditated philosophy on how ETL jobs should be structured. This allows it to parallelize jobs, schedule them appropriately with dependencies and historically reprocess data when needed.

## Airflow Principles

1. **Idempotency**

   Write procedures that produce the same results when run with the same parameters every time, even  on different days. This reduces the possibility of unintended side effects.

2. **Determinism**
   Write functions that always produce the same output for a given input. Avoid using global variables, random values, hardware timers. Explicitly state the order (for ex. using `ORDER BY`) rather than relying on the implicit ordering (for ex. in Python Dictionaries)
3. **Execute Conditionally**
   Use features like `depends_on_past` when writing DAGs to ensure all upstream instances succeeded. Use the `LatestOnlyOperator` to conditionally skip some downstream steps if it's not the most recent execution of the workflow. The `BranchPythonOperator` allows you to choose which branch of the workflow is to be executed based on defined logic.
4. **Interim Data Availability**
   If some downstream tasks depend on an temporary dataset, ensure that it is rested on a service that is accessible to all workers. When using the `LocalExecutor` it might be possible to get away with persisting intermediate files locally, but when in cluster mode you should exercise caution.
5. **Understand SLAs and Alerts**
   Airflow uses SLAs to detect long-running (hanged) tasks and alerts you via Email or Slack. You can check the Web UI to inspect the missed SLAs further.
6. **Use Sensors**
   In addtion to triggering executions at scheduled intervals, Airflow can use Sensors like an HTTP Sensor or a File Sensor to wait for the appearance of a condition or data before continuing to run the DAG downstream.

## Points of Caution

- The `start_date` specifies the datetime at which data will be present in the database. The first job will run at `start_date + interval` because that's when all the data for the specified interval will have arrived.
- The `execution_date` specifies the lowest datetime of the interval under consideration.
- Don't forget to *start the scheduler* along with the webserver. Just run `airflow scheduler`
- If you rename tasks after the DAG has already run for a particular date, they might now show up in the UI. This is because a TaskInstance was recorded in the database against the old task name. In this case, you might want to run a backfill.
- When a DAG has been run, the database contains *instances* of that run. If you change the `start_date` or the `interval`, the scheduler may get confused. You should change the version of a DAG if you change its properties.

## Running Airflow with Docker Compose

- 



 

