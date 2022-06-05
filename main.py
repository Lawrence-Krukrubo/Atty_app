import streamlit as st
from datetime import date, datetime
import mysql
from mysql.connector import Error
import pandas as pd
import time


# @st.experimental_singleton
# def init_connection():
#     return mysql.connector.connect(**st.secrets["mysql"])
#
# connection = init_connection()
# cursor = connection.cursor()
# cursor.execute("select database();")
# record = cursor.fetchone()
# print("You're connected to database: ", record)


# db_name = 'dand'
connection = mysql.connector.connect(database=st.secrets["db"],
                                     user=st.secrets["db_username"],
                                     password=st.secrets["db_password"])


cursor = connection.cursor()
cursor.execute("select database();")
record = cursor.fetchone()
print("You're connected to database: ", record)


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


st.title('DAND Connect Session Attendance')
st.subheader('Session Lead: Lawrence Krukrubo')

# Load the data and receive email input
data = query_to_df('SELECT * FROM students;')
today = str(date.today())[-1]
new_table = f'stud_{today}'

# Get students email
mail = st.text_input("Write Your Udacity Email").lower().strip()


def create_new_table(table=new_table):
    q1 = f'CREATE TABLE IF NOT EXISTS {table} SELECT * FROM students;'

    try:
        cursor.execute(q1)
    except Exception as e:
        st.write(e)


def get_names():
    if len(mail) > 3:
        try:
            ind = data['email'].to_list().index(mail)
            first, last = data.iat[ind, 0], data.iat[ind, 1]
            return first, last
        except ValueError:
            return None, None


def confirm_name():
    x, y = get_names()
    if not x:
        st.write('Your Email is Incorrect! Try again carefully...')
    else:
        st.write(f'Your Udacity Name Is: {x} {y}')


def submit():
    first, last = get_names()

    if first:
        create_new_table()
        q2 = f'UPDATE {new_table} SET status = 1 WHERE email = "{mail}";'
        cursor.execute(q2)
        connection.commit()
        now = datetime.now()
        now = now.strftime("%H:%M:%S")
        st.write(f'Attendance Submitted! UK-Time: {now}')
    else:
        st.write('No Submission!: Confirm Udacity Email or Contact Session Lead.')

# if st.checkbox('Show Main Data'):
#     st.subheader('Main Data')
#     st.write(data)


if st.button('Submit Attendance'):
    confirm_name()
    submit()