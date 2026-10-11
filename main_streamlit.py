import streamlit as st
import psycopg2

from user_input_credentials import sign_in, sign_up
from recommander_system import recommanderSystem


st.set_page_config(page_title="StudyHub")

st.title("STUDYHUB")
st.write("I am here to help you!")


@st.cache_resource
def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="recommander_system",
        user="postgres",
        password="Sachin1130!",
        port=5432,
    )


conn = get_connection()


if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


user_choice = st.selectbox(
    "Choose an option",
    ["Select an option", "Sign in", "Sign up", "Guest"],
)


if user_choice == "Sign in":
    user_id = sign_in()

    if user_id is not None:
        st.session_state.user_id = user_id
        st.session_state.logged_in = True
        st.success("Signed in successfully.")


elif user_choice == "Sign up":
    sign_up()
    st.info("After signing up, select Sign in to log in.")


elif user_choice == "Guest":
    st.session_state.logged_in = True
    st.session_state.user_id = None
    st.success("You are using guest mode.")


if st.session_state.logged_in:
    st.divider()

    menu_choice = st.radio(
        "What would you like to do?",
        [
            "Recommendation system",
            "View search history",
            "View watch history",
            "View read history",
        ],
    )

    if menu_choice == "Recommendation system":
        result = recommanderSystem()

        if result:
            query, resource_type_used = result

            if st.session_state.user_id is not None:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO query_history
                        (user_id, query_text, resource_type_used)
                        VALUES (%s, %s, %s)
                        """,
                        (
                            st.session_state.user_id,
                            query,
                            resource_type_used,
                        ),
                    )

                conn.commit()
                st.success("Your query was saved.")