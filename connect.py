import pandas as pd
import mysql
from mysql.connector import Error
import time

db_name = 'dand'
connection = mysql.connector.connect(host='localhost',
                                         database=db_name,
                                         user='danam',
                                         password= 'roots')

cursor = connection.cursor()
cursor.execute("select database();")
record = cursor.fetchone()
print("You're connected to database: ", record)

# Initialize connection.
# Uses st.experimental_singleton to only run once.


# @st.experimental_singleton
# def init_connection():
#     return mysql.connector.connect(**st.secrets["mysql"])
#
#
# connection = init_connection()
# cursor = connection.cursor()
# cursor.execute("select database();")
# record = cursor.fetchone()
# print("You're connected to database: ", record)

# try:
#     connection = mysql.connector.connect(host='localhost',
#                                          database=db_name,
#                                          user= 'danam',
#                                          password= 'roots')
#     if connection.is_connected():
#         db_Info = connection.get_server_info()
#         print("Connected to MySQL Server version ", db_Info)
#         cursor = connection.cursor()
#         cursor.execute("select database();")
#         record = cursor.fetchone()
#         print("You're connected to database: ", record)
#
# except Error as e:
#     print("Error while connecting to MySQL", e)
#

def query_to_df(query):
    """This method converts the result
        of a SQL query to a DataFrame.
    @param query: Is a string of valid SQL syntax
    """

    st = time.time()
    # Assert Every Query ends with a semi-colon
    try:
        assert query.endswith(';')
    except AssertionError:
        return 'ERROR: Query Must End with ;'

    # so we never have more than 50 rows displayed
    pd.set_option('display.max_rows', 30)
    df = None

    # Process the query
    cursor.execute(query)
    columns = cursor.description
    result = []
    for value in cursor.fetchall():
        tmp = {}
        for (index, column) in enumerate(value):
            tmp[columns[index][0]] = [column]
        result.append(tmp)

    # Create a DataFrame from all results
    for ind, data in enumerate(result):
        if ind >= 1:
            x = pd.DataFrame(data)
            df = pd.concat([df, x], ignore_index=True)
        else:
            df = pd.DataFrame(data)
    print(f'Query ran for {time.time() - st} secs!')
    return df


print(query_to_df('SHOW TABLES;'))