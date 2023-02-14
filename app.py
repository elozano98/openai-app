import openai
import streamlit as st

from sections import load_files_section, load_fine_tunes_section, load_models_section


def run() -> None:
    st.title("OpenAI")

    section = st.sidebar.selectbox("", ["Fine-tunes", "Files", "Models"])

    if section == "Fine-tunes":
        load_fine_tunes_section()
    elif section == "Models":
        load_models_section()
    else:
        assert section == "Files"
        load_files_section()


if __name__ == "__main__":
    openai.api_key = st.secrets["OPENAI_API_KEY"]
    run()
