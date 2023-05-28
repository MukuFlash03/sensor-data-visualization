'''
This file contains functions for fetching data from the database.
'''

import os
import psycopg2
from datetime import datetime
import pandas as pd
from io import StringIO


# This function is used to test and establish the connection to the database.
def test_db() -> psycopg2.extensions.connection: 
    print("Connecting to " + os.environ['POSTGRES_HOST'])
    
    # Establish the connection to the database
    connection: psycopg2.extensions.connection = psycopg2.connect(
        host=os.environ['POSTGRES_HOST'],
        port=os.environ['POSTGRES_PORT'],
        database=os.environ['POSTGRES_DB'],
        user=os.environ['POSTGRES_USER'],
        password=os.environ['POSTGRES_PASSWORD']
    )

    return connection

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# This function is used to fetch the minimum and maximum timestamps from database
def fetchStartEndTimes(start_time: str, end_time: str) -> tuple[str, str]:
    
    # Establish the connection to the database
    connection: psycopg2.extensions.connection = test_db()
    
    # Create a cursor object to execute SQL queries
    cursor: psycopg2.extensions.cursor = connection.cursor()
    
    # Execute the SQL query to retrieve the minimum timestamp
    cursor.execute('''SELECT MIN(time) as minT, MAX(time) as maxT 
        FROM (
                SELECT time FROM "CM_HAM_DO_AI1/Temp_value"
                UNION
                SELECT time FROM "CM_HAM_PH_AI1/pH_value"
                UNION
                SELECT time FROM "CM_PID_DO/Process_DO"
                UNION
                SELECT time FROM "CM_PRESSURE/Output"
        ) AS all_times;
    ''')

    # Fetch the minimum and maximum timestamps from all four tables
    time_window: tuple = cursor.fetchone()
    min_timestamp: str = time_window[0]
    max_timestamp: str = time_window[1]

    # If the start_time or end_time is not provided, 
    # set it to the minimum and maximum timestamps
    if start_time is None or start_time == '' or end_time is None or end_time == '':
        start_time = min_timestamp
        end_time = max_timestamp
    else:
        # If the start_time or end_time is provided, 
        # convert it to the datetime format
        start_time = datetime.strptime(start_time, '%Y-%m-%dT%H:%M')
        end_time = datetime.strptime(end_time, '%Y-%m-%dT%H:%M')

        # Convert the datetime format to string format
        start_time = start_time.strftime('%Y-%m-%d %H:%M:%S.%f')
        end_time = end_time.strftime('%Y-%m-%d %H:%M:%S.%f')

    return start_time, end_time

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# This function is used to create the queries to fetch data from the database
def createQuery(start_time: str, end_time: str) -> list[str]:
    query: list[str] = [
        f"SELECT time, value FROM \"CM_HAM_DO_AI1/Temp_value\" WHERE time BETWEEN '{start_time}' AND '{end_time}' ORDER BY time ASC",
        f"SELECT time, value FROM \"CM_HAM_PH_AI1/pH_value\" WHERE time BETWEEN '{start_time}' AND '{end_time}' ORDER BY time ASC",
        f"SELECT time, value FROM \"CM_PID_DO/Process_DO\" WHERE time BETWEEN '{start_time}' AND '{end_time}' ORDER BY time ASC",
        f"SELECT time, value FROM \"CM_PRESSURE/Output\" WHERE time BETWEEN '{start_time}' AND '{end_time}' ORDER BY time ASC"
    ]
    return query

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# This function is used to fetch data from the database
def fetch_data(start_time: str, end_time: str) -> list[list[tuple]]:

    # Establish the connection to the database
    connection: psycopg2.extensions.connection = test_db()
    
    # Create a cursor object to execute SQL queries
    cursor: psycopg2.extensions.cursor = connection.cursor()

    # Fetch the minimum and maximum timestamps
    start_time, end_time = fetchStartEndTimes(start_time, end_time)

    # Create the queries to fetch data from the database
    query: list[str] = createQuery(start_time, end_time)

    # Fetch data from the four tables
    cursor.execute(query[0])
    temperatureData: tuple = cursor.fetchall()
    cursor.execute(query[1])
    pHData: tuple = cursor.fetchall()
    cursor.execute(query[2])
    distilledO2Data: tuple = cursor.fetchall()
    cursor.execute(query[3])
    pressureData: tuple = cursor.fetchall()

    # Combine the data into a single list
    allData: list[tuple] = [temperatureData, pHData, distilledO2Data, pressureData]
    return allData

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# This function is used to fetch data from the database and return it as a DataFrame
def fetch_data_DF(start_time: str, end_time: str) -> str:

    # Establish the connection to the database
    connection: psycopg2.extensions.connection = test_db()

    # Fetch the minimum and maximum timestamps
    start_time, end_time = fetchStartEndTimes(start_time, end_time)

    # Create the queries to fetch data from the database
    query: list[str] = createQuery(start_time, end_time)

    # Fetch data from the four tables
    temperatureData: pd.DataFrame  = pd.read_sql(query[0], connection)
    pHData: pd.DataFrame  = pd.read_sql(query[1], connection)
    distilledO2Data: pd.DataFrame  = pd.read_sql(query[2], connection)
    pressureData: pd.DataFrame  = pd.read_sql(query[3], connection)

    # Combine the data into a single DataFrame
    df: pd.DataFrame  = pd.concat([temperatureData, pHData, distilledO2Data, pressureData], axis=1)

    # Write the DataFrame to a CSV string
    csv_string: StringIO = StringIO()
    df.to_csv(csv_string, index=False)

    # Return the CSV string
    return csv_string.getvalue()
