import logging

from cassandra.cluster import Cluster
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType

def create_spark_connection():
    s_conn = None

    try:
        # s_conn represents the driver node

        # Cassandra typically listens on port 9042 for client connections (including CQL clients like your cas_session object). 
        # If the port is not explicitly specified in the connection settings, Cassandra defaults to this port.
        s_conn = SparkSession.builder \
            .appName('SparkDataStreaming') \
            .config('spark.jars.packages', "com.datastax.spark:spark-cassandra-connector_2.13:3.4.1," # downloads the corresponding packages needed in java
                                           "org.apache.spark:spark-sql-kafka-0-10_2.13:3.4.1") \
            .config('spark.cassandra.connection.host', 'localhost') \
            .getOrCreate()
        
        # sparkContext is used to configure and interact with the Spark application
        # "ERROR" only shows errors, suppressing info and warnings.
        s_conn.sparkContext.setLogLevel("ERROR")

        # logs that spark connection with cassandra and kafka is done 
        logging.info("Spark connection created successfully!")
    except Exception as e:
        logging.error(
            f"Couldn't create the spark session due to exception {e}")

    return s_conn

def create_cassandra_connection():
    try:
        # connecting to the cassandra cluster
        cluster = Cluster(['localhost'])

        cas_session = cluster.connect()

        return cas_session
    except Exception as e:
        logging.error(f"Could not create cassandra connection due to {e}")
        return None

if __name__ == "__main__": 
    # create spark connection
    spark_conn = create_spark_connection()

    if spark_conn:
        session = create_cassandra_connection()

        if session: 
            # create keyspace 

            # create table

