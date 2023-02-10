from typing import List

import streamlit as st

from models import Model
from utils import generate_completion, get_models


def list_models() -> None:
    models = _filter_models(models=get_models())
    for m in models:
        m.display()


def run_inference() -> None:
    models = _filter_models(models=get_models())
    with st.form("inference"):
        model_id = st.selectbox("Model", [m.id for m in models])
        max_tokens = st.number_input("Maximum tokens:", min_value=1, step=1)
        temperature = st.slider(
            "Temperature", min_value=0.0, max_value=1.0, value=0.0, step=0.01
        )
        text = st.text_area("Text:", height=250)
        run_inference_button = st.form_submit_button("Run")
        if run_inference_button:
            if text:
                completion = generate_completion(
                    text=text,
                    model_id=model_id,
                    max_tokens=max_tokens,
                    temperature=temperature,
                )
                st.markdown("**Result:**")
                st.text(completion)
            else:
                st.error("Error: No text provided.")


def _filter_models(models: List[Model]) -> List[Model]:
    with st.sidebar.expander("Filters"):
        owner = st.selectbox(
            "Owner:",
            ["All"] + list(set(m.owner for m in models)),
        )
    return [m for m in models if owner == "All" or m.owner == owner]
