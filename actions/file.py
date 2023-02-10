import streamlit as st

from utils.file import get_all_files


def list_files() -> None:
    files = get_all_files()
    with st.sidebar.expander("Information"):
        st.info(f"**Number of files:** {len(files)}")
    for f in files:
        f.display()
