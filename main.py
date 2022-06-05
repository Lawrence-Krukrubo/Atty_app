from connect import connection, cursor, query_to_df
import streamlit as st
from datetime import date, datetime

st.title('DAND Connect Session Attendance')
st.subheader('Session Lead: Lawrence Krukrubo')

# Load the data and receive email input
data = query_to_df('SELECT * FROM students;')
today = str(date.today())[-1]
new_table = f'stud_{today}'

q1 = f'CREATE TABLE IF NOT EXISTS {new_table} SELECT * FROM students;'

try:
    cursor.execute(q1)
except Exception as e:
    st.write(e)

# Get students email
mail = st.text_input("Write Your Udacity Email").lower().strip()


def get_names():
    if len(mail) > 3:
        try:
            ind = data['email'].to_list().index(mail)
            first, last = data.iat[ind, 0], data.iat[ind, 1]
            return first, last
        except ValueError:
            pass


def confirm_name():
    try:
        x, y = get_names()
        st.write(f'Your Udacity Name Is: {x} {y}')
    except:
        st.write('Your Email is Incorrect! Try again carefully...')


def submit():
    try:
        q2 = f'UPDATE {new_table} SET status = 1 WHERE email = "{mail}";'
        cursor.execute(q2)
        connection.commit()
        now = datetime.now()
        now = now.strftime("%H:%M:%S")
        st.write(f'Attendance Submitted! UK-Time: {now}')
    except Exception as e:
        st.write('No Submission!: Confirm Udacity Email or Contact Session Lead.')

# if st.checkbox('Show Main Data'):
#     st.subheader('Main Data')
#     st.write(data)


if st.button('Submit Attendance'):
    confirm_name()
    submit()
