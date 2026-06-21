import streamlit as st

st.set_page_config(
    page_title="AI Smart Waste Collection System",
    page_icon="♻️",
    layout="wide"
)

st.title("♻️ AI Smart Waste Collection System")
st.subheader("Transforming Waste Management with AI and Data Analytics")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    st.header("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username and password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.rerun()
        else:
            st.error("Enter username and password")

else:

    st.success(f"Welcome {st.session_state.username}")

    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()
