## Data Modeling

>  a design process where one carefully defines table schemas and data relations to capture business metrics and dimensions

When a user interacts with a product, their usage information such as clicks, views, likes, saves, upvotes are all captured by the system in an Events stream. These are stored in tables with simple schemas and an ERD (Entity Relationship Diagram) is built to remember how the tables are related. This process, called Normalization, attempts to 

- reduce data duplication 
- reduce the storage size 
- improve maintainability

The architect needs to decide between OLTP databases (optimized for transactional processing) and OLAP databases (optimized for analytical processing). A popular choice, `star schema`, builds normalized *fact* and *dimension* tables. 

- *Fact tables* typically contain point-in-time transactional data. 
  The column structure is simple and often represented as a unit of transaction and widely used as source-of-truth tables from which business metrics are derived. Examples from Airbnb - bookings, reservations, cancellations, alterations
- *Dimension Tables* contain slowly changing attributes of specific entities like users, listings, markets that help us slice-and-dice our data.

Users are encouraged to write `JOIN` statements as needed to create *de-normalized* Views as and when needed to answer specific questions. 

## Data Partitioning

- a practice that enables more efficient querying and data backfilling
- instead of storing all the data in one chunk, we break it up into independent, self-contained chunks each with its own *partition key*
- one common partition key to use is *datestamp*

### Backfilling

- sometimes we wish to compute new metrics on historical data and compare them with existing metrics

## Airflow 

- use sensors, operators, and transfers to operationalize the concepts of extraction, transformation, and loading

- any ETL job is built on top of three building blocks: **E**xtract, **T**ransform, and **L**oad, combined in complex ways

- it is often useful to visualize complex data flows using a graph.

- a *node* in a graph represents a task, and an *edge* represents the dependency of one task on another

- In Airflow, these graphs are built programmatically and known as DAGs

- *DAGs* describe what needs to be done, and in what order

- *Operators* describe how work is actually done. 

  - *Sensors*: wait for a condition to become `True`
    Example - `NamedHivePartitionSensors` can be used to check whether the most recent partition of a Hive table is available for downstream processing.

  - *Operators*: trigger the execution of a task 

    Examples - `HiveOperator` (to execute hive queries), `PythonOperator` (to run a Python module) and `BashOperator` (to run a bash script, or even a Spark job)

  - *Transfers*: move data from A to B
    `MySqlToHiveTransfer` or `S3ToHiveTransfer` can move data between sources and sinks depending on your infrastructure

  Below is an example of a sample DAG file (these are stored under `/dags` in the `AIRFLOW_HOME` directory)

  ```python
  """
  The DAG docstring
  Describe the goal of the DAG
  Provide links to documents 
  """
  from datetime import datetime, timedelta
  from airflow.models import DAG
  from airflow.operators.sensors import ...
  from airflow.operators.<xyz> import ...
  
  # set default args for the DAG
  default_args_ = {
      'start_date': datetime(2018, 1, 1),
  }
  
  # Instantiate the DAG
  dag_01 = DAG(
      dag_id='dag_extract_twitter',
      default_args=default_args_,
      schedule_interval='@daily'
  )
  
  # Define Tasks
  task_1 = BashOperator(
  	task_id='connect-to-db',
      bash_command='connect.sh',
      dag='dag_extract_twitter'
  )
  
  task_2 = PythonOperator(
      task_id='clean-data',
      python_executable='clean_data',
      dag='dag_extract_twitter'
  )
  
  # Define Dependencies
  task_1 >> task_2
  ```


## ETL Best Practices

- *Partition Data Tables*

  - especially useful when dealing with large-size tables with a long history. 
  - can leverage dynamic partitions to parallelize backfilling

- *Load Data Incrementally*

  - useful when building dimension tables from the fact tables
  - we only neeed to append the new transactions from the previous load date

- *Enforce Idempotency*

  - the same query, when run against the data sources and over the same time range, should always return the same result

- *Parameterize Workflows*

  - Jinja can be used in conjunction with SQL

- *Add data tests early and often*

  - Push data to a staging table, check for quality issues and then push to production
  - Tests can be macro (such as overall counts) or micro (such as detecting outliers)

- *Altering and monitoring*

  - ETL jobs take a long time to run, so adding alerts and monitoring them helps
  - Use Emails or Slack notifications with Airflow to alert devs when an SLA is missed, or when the `r-squared` of a Regression model falls below acceptable levels.


