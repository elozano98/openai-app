import streamlit as st

from actions import list_files, list_fine_tunes, list_models, run_inference


def load_fine_tunes_section() -> None:
    st.subheader("Fine-tunes")
    action = st.sidebar.selectbox("", ["List"])

    if action == "List":
        list_fine_tunes()


def load_models_section() -> None:
    st.subheader("Models")
    action = st.sidebar.selectbox("", ["List", "Inference"])

    if action == "List":
        list_models()
    elif action == "Inference":
        run_inference()


def load_files_section() -> None:
    st.subheader("Files")
    action = st.sidebar.selectbox("", ["List"])

    if action == "List":
        list_files()
