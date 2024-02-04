import os
import sqlite3

import google.generativeai as genai
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from database import create_table_insert_data


# Function To Load Google Gemini Model and provide queries as response
def get_gemini_response(prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text


# Function To retrieve query from the database
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    try:
        cur = conn.cursor()
        create_table_insert_data(cur)
        cur.execute(sql)
        rows = cur.fetchall()
        df = pd.DataFrame(rows, columns=list(map(lambda x: x[0], cur.description)))
        conn.commit()
    finally:
        conn.close()

    return df


def main():
    # load all the environment variables
    load_dotenv()

    # Configure Genai Key
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    # Define Your Prompt
    prompt = """
    You are an expert in converting questions to SQL query!
    The SQL database has the name student
    and has the following columns - NAME, CLASS, SECTION, SCORE
    
    For example:
    Example 1 - How many entries of records are present?
    the SQL command will be something like this SELECT COUNT(*) FROM student;
    
    Example 2 - Tell me all the students studying in Data Science class? 
    the SQL command will be something like this SELECT * FROM student where CLASS="Data Science";
    
    also the sql code should not have ``` in beginning or end and sql word in output
    """

    # Streamlit App
    st.set_page_config(page_title="I can Retrieve Any SQL query", page_icon=":robot:")
    st.header("Gemini App To Retrieve SQL Data")

    question = st.text_input("Input: ", key="input")

    submit = st.button("Ask the question")
    # if submit is clicked
    if submit:
        sql = get_gemini_response([prompt, question])
        st.success("SQL query generated successfully:")
        st.code(sql, language="sql")

        df = read_sql_query(sql, "student.db")
        st.subheader("The response is")
        st.dataframe(df)


if __name__ == '__main__':
    main()
