import os

import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv
from sqlalchemy.sql import text

from database import create_table_insert_data

# Define Your Prompt
templet = """
You are an expert in converting questions to SQL query!
The SQL database has the name student
and has the following columns - NAME, CLASS, SECTION, SCORE

For example:
Example 1 - How many entries of records are present?
the SQL command will be something like this SELECT COUNT(*) FROM student;

Example 2 - Tell me all the students studying in Data Science class? 
the SQL command will be something like this SELECT * FROM student where CLASS="Data Science";

Create a SQL query snippet using the below text:
```
{prompt}
```
also the sql code should not have ``` in beginning or end and sql word in output
"""


def get_gemini_response(api_key, prompt):
    # Configure Genai Key
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(templet.format(prompt=prompt))
    return response.text


# Function To retrieve query from the database
def read_sql_query(sql, db):
    # Create the SQL connection to student_db as specified in your secrets file.
    conn = st.connection(db, type='sql')
    session = conn.session
    try:
        create_table_insert_data(session, text)
        if sql.startswith("INSERT ") or sql.startswith("UPDATE ") or sql.startswith("DELETE "):
            session.execute(text(sql))
            sql = 'SELECT * FROM student'

    finally:
        session.commit()

    return session.execute(text(sql))


def get_api_key():
    try:
        return st.secrets["GOOGLE_API_KEY"]
    except KeyError:
        load_dotenv()
        return os.getenv("GOOGLE_API_KEY")


def main(api_key):
    # Streamlit App
    st.set_page_config(page_title="I can Retrieve Any SQL query", page_icon=":robot:")
    st.header("Gemini App To Retrieve SQL Data")

    if not api_key:
        st.markdown("[Get API key | Google AI Studio](%s)" % "https://makersuite.google.com/app/apikey")
        api_key = st.text_input("Entering your own Google API key", type="password")

    prompt = st.text_input("Ask the question: ", key="input")
    submit = st.button("Submit")
    # if submit is clicked
    if submit:
        sql = get_gemini_response(api_key, prompt)
        st.success("SQL query generated successfully:")
        st.code(sql, language="sql")
        df = read_sql_query(sql, 'student_db')
        st.subheader("The response is")
        st.dataframe(df)
    else:
        df = read_sql_query('SELECT * FROM student', 'student_db')
        st.dataframe(df)


if __name__ == '__main__':
    main(get_api_key())
