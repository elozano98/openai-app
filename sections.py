import streamlit as st
from actions import list_fine_tunes, list_files


def load_fine_tunes_section() -> None:
    st.subheader("Fine-tunes")
    action = st.selectbox("Action:", ["List"])

    if action == "List":
        list_fine_tunes()


def load_files_section() -> None:
    st.subheader("Files")
    action = st.selectbox("Action:", ["List"])

    if action == "List":
        list_files()
