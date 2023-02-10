import streamlit as st
from utils import get_models
from models import Model


def list_models() -> None:
    models = get_models()
    owner = st.selectbox(
        "Owner:",
        ["All"] + list(set(m.owner for m in models)),
    )
    base_model = st.selectbox("Base model:", ["All"] + Model.BASE_MODELS)
    for model in models:
        if (owner == "All" or model.owner == owner) and (
            base_model == "All" or model.base_model == base_model
        ):
            model.display()
