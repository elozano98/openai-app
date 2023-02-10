import openai
import streamlit as st

from sections import load_files_section, load_fine_tunes_section


def run() -> None:
    st.title("OpenAI")

    section = st.sidebar.selectbox("", ["Fine-tunes", "Files"])

    if section == "Fine-tunes":
        load_fine_tunes_section()
    else:
        assert section == "Files"
        load_files_section()


if __name__ == "__main__":
    openai.api_key = st.secrets["OPENAI_API_KEY"]
    run()
