



## Desired Features of Data Pipelines

1. Explicit documentation of Data Lineage: 
   *Where are my derived datasets coming from?*
2. Defined dependencies between tasks and pipelines
3. Centralised Scheduling
   *Automatic retries*
   *Configure sources once and re-use/share*
4. Alerting and Monitoring
   *Did something fail?*
   *Is there a bottleneck in my pipeline?*
5. Dealing with Complexity Intelligently

## Airflow 

> A platform to programmatically author, schedule and monitor workflows

![image-20180820121904575](/var/folders/kv/l02c_chn7tqd9cmrvyms7vy4bfc09j/T/abnerworks.Typora/image-20180820121904575.png)



## Difference from `Luigi` 

- No dynamic pipeline creation
- No built-in scheduler
- Slow for large DAGs
- Not so many features
- Output oriented (vs task-oriented)

### Architecture

- Scheduler - orchestrates the execution of tasks
  - persists information about the status of tasks in a metadata DB
  - DAGs are identified by their IDs
  - Has different mode
    - Sequential - tasks scheduled on the same machine where Airflow is running
    - Celery - tasks scheduled on different worker nodes. 
      This allows Airflow to scale.
- UI



## Airflow Terms

- Operators - "do [this]"
- Sensors - "is [this] available now"
- Variables - "provide value at runtime in admin console"
- Pools - "ensure that only one process pushes data to DB"
- Also
  - Database Integrations
  - Error monitoring
  - Retry policy
  - Timeouts - "fail if hanged for x mins"

## Scheduler

- Each DAG has a
  - **schedule** defined with a cron notation 
  - **start date**
- DAGs process the data generated in the previous period. So a DAGRun is triggered when the period it covered has ended. 
- A DAG run is scheduled for each scheduled period between the start date and now
  - If the start date is in the past, Airflow will schedule a bunch of runs. See the `catchup` property.
  -  If you clear DAG runs from the past, Airflow will re-run them
    See `airflow clear <dag-id>`
  - If the `depends_on_past` is set to True, the subsequent tasks will run iff previous were successful
- Data should be immutable and all transformations should be reproducible 
- It's a good idea to have two similar DAGs parameterized differently
  - one DAG for backfilling history that is scheduled to run `@once` and 
  - another DAG that runs periodicaly, ex. `weekly`

## XCom

- Recommended: No pipeline between tasks. All tasks should read/write to systems.
- for sharing small bits of information between tasks

## Trying out Airflow

- Using Docker [github.com/puckel/docker-airflow](github.com/puckel/docker-airflow)
- Using Ansible [github.com/LREN-CHUV/ansible-airflow](github.com/LREN-CHUV/ansible-airflow)



# Airflow x Spark

- Airflow installed on a Hadoop Gateway node that can submit a Spark job 
  - use a `BashOperator` with a `spark-submit --master yarn ...`
  - use a `HTTPOperator` to submit the job and poll the cluster through API requests to check if it is done
  - Client Mode - logs available
  - Cluster Mode - will have to use a `FileSensor`
- Alternatively, use Airflow to 
  - spin-up a Spark cluster
  - perform jobs
  - spin-down
  - see [agari.com/automated-model-building-emr-spark-airflow](agari.com/automated-model-building-emr-spark-airflow)

