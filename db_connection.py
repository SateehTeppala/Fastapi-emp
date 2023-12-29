import psycopg2
from psycopg2 import pool
import pandas as pd
import logging
import os
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Replace these variables with your actual database connection details


# Create a connection pool
connection_pool = psycopg2.pool.SimpleConnectionPool(
    minconn=1,
    maxconn=5,
    dbname=os.environ['_dbname'],
    user=os.environ['_user'],
    password=os.environ['_password'],
    host=os.environ['_host'],
    port=os.environ['_port']
)


# Function to execute a query using a connection from the pool
def execute_query(query, param_value):
    connection = connection_pool.getconn()
    try:
        cursor = connection.cursor()
        cursor.execute(query, (param_value,))
        result = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        logger.info("executed successfully")
        return pd.DataFrame(result, columns=columns)
    except:
        logger.error("not executed successfully")
    finally:
        connection_pool.putconn(connection)

# # Example query
# query = "select * from employee where employee_id = %s;"
#
# a = 'E02003'
# # Try executing the query using the connection pool
# try:
#     version_result = execute_query(query,a)
#     print("Connected to the database. PostgreSQL version:", version_result[0])
#
# except (Exception, psycopg2.Error) as error:
#     print("Error while connecting to PostgreSQL:", error)
#
# finally:
#     # Close all connections in the pool
#     if connection_pool:
#         connection_pool.closeall()
#         print("Connection pool closed.")
