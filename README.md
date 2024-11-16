## Real-Time Data Streaming Project 

This guide provides a step-by-step approach to building a full-scale data engineering pipeline from scratch. It demonstrates how to handle data ingestion, processing, and storage using technologies such as Apache Airflow, Python, Apache Kafka, Apache Zookeeper, Apache Spark, and Cassandra. The entire setup is containerized using Docker for streamlined deployment and scalability.

## Key Learning Points 
As we systematically review the key concepts from this project, we will walk through the sequence in which data is processed within the system. Below is a rough diagram of the flow in which data is being processed: 

![system architrecture diagram](./system_architecture_diagram.png)

### Confluence

While not a part of this diagram, Confluence is important in keeping the Apache services together. 

**what is it**: It is a management and monitoring tool for Apache Kafka and related services in the Confluent ecosystem, provides a web based interface to observing and controlling kafka clusters, topics, streams, and connections. 

**what does it do**: It allows you to track and monitor the performance of Kafka brokers, topics, consumers, producers, schema registry, and connectors, among other Kafka-related components.

we can access this dashboard at `localhost:9021`.

**why do we use Confluence**: Simplifies the process of monitoring and managing Kafka. It does not control the orchestration or scheduling of workflows.

### Apache AirFlow

**what is it**: Apache Airflow provides the orchestration for the data pipeline, giving you a centralized interface to monitor and manage the flow of tasks (also known as DAGs). 

**what does it do**: It is used to schedule and monitor ETL pipelines, data workflows, and other batch or streaming tasks.

we can also access its own web-based UI via `localhost:8080` which allows users to manage tasks, monitor DAGs, view logs, and track status of individual tasks within the workflow. 

**why do we use AirFlow**: Helps in the automation and scheduling of complex workflows. It is often used to trigger tasks like data extraction, transformation, and loading (ETL processes).

**Components in Airflow**: 
* Tasks - individual pieces of work 
* Scheduler - schedules the workflows and submits tasks to the executor to run 
* Executor (part of the scheduler) - configuration property of the scheduler which specifies how the tasks should be runned. Here, we have used `SequentialExecutor`, which runs one task at a time and is ideal for development or small-scale environments
* webserver - presents a handy user interface to inspect, trigger and debug the behaviour of DAGs and tasks
* DAG files (`dags` file in this repository) - read by the scheduler to figure out what tasks to run and when to run them
* metadata database - Stores all the metadata for DAGs, task instances, logs, and configurations.

In a large distributed system, there can be other roles that can be played, such as `Deployment Manager`, `DAG Author`, and `Operations User`, which plays a part in managing a larger system of machines. 

In the case of a distributed deployment, it is important to consider the security aspects of the components. The `webserver` does not have access to the DAG files directly. The code in the Code tab of the UI is read from the metadata database. The webserver cannot execute any code submitted by the DAG author. It can only execute code that is installed as an installed package or plugin by the Deployment Manager. The Operations User only has access to the UI and can only trigger DAGs and tasks, but cannot author DAGs.

* Deployment Manager: Responsible for deploying and maintaining Airflow infrastructure, ensuring that necessary packages and plugins are installed, and managing system-level configurations and security policies.
* DAG Author: Develops and writes DAGs to define workflows, ensuring they are correctly structured and meet the requirements for execution within the Airflow system.
* Operations User: Manages the execution of DAGs, monitors task status, triggers runs, and resolves issues, but does not have permissions to modify or create DAGs.

Below is an outline of the architecture used in this project. More about Airflow's architecture can be found [here](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/overview.html). 

![airflow architectural diagram](./architecture_diagram_airflow.png)

