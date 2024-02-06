import os

import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-pro')


def main():
    st.set_page_config(page_title="SQL Query Generator", page_icon=":robot:")
    st.markdown(
        """
        <div style="text-align:center;">
            <h1>SQL Query Generator</h1>
        </div>
        """,
        unsafe_allow_html=True
    )
    prompt = st.text_area("Enter your query here in Plain Language:")

    submit = st.button("Generate SQL Query")
    if submit:
        template = """
        Create a SQL query snippet using the below text:
        ```
        {prompt}
        ```
        I just want a SQL Query.
        """
        formatted_template = template.format(input=prompt)
        response = model.generate_content(formatted_template)
        sql_query = response.text
        sql_query = sql_query.strip().lstrip("```sql").rstrip("```")

        with st.container():
            st.success("SQL query generated successfully:")
            # st.markdown(sql_query)
            st.code(sql_query, language="sql")

            expected_output = """
            What would by the expected response of this SQL query snippet:
            ```sql
            {sql_query}
            ```
            Provide sample table Response:
            """
            expected_formatted = expected_output.format(sql_query=sql_query)
            expected_response = model.generate_content(expected_formatted)
            st.success("Expected Output of this SQL query will be:")
            st.markdown(expected_response.text)


if __name__ == '__main__':
    main()
