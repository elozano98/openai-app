import streamlit as st

from utils import get_fine_tunes, get_all_files, start_training
from models import Model


def list_fine_tunes() -> None:
    with st.sidebar.expander("Options"):
        num_fine_tunes_to_show = st.number_input(
            "Number of fine-tunes to show:", min_value=1, max_value=10, value=2
        )
        fine_tunes = get_fine_tunes(n=num_fine_tunes_to_show)
    for f in fine_tunes:
        f.display()


def train() -> None:
    file_ids = [f.id for f in get_all_files()]
    model_suffix = st.text_input("Model suffix:")
    base_model = st.selectbox("Base model:", Model.BASE_MODELS)
    training_file_id = st.selectbox("Training file ID:", file_ids)

    if st.checkbox("Use validation file", value=True):
        validation_file_id = st.selectbox("Validation file ID:", file_ids)
        if (
            st.selectbox("Purpose", ["Completion", "Classification"])
            == "Classification"
        ):
            num_classes = st.number_input(
                "Number of classes:", min_value=1, step=1, value=2
            )
        else:
            num_classes = None
    else:
        validation_file_id = None
        num_classes = None

    num_epochs = st.number_input("Epochs:", min_value=1, step=1, value=4)
    if st.checkbox("Show advanced hyperparameters"):
        batch_size = st.number_input(
            "Batch Size", min_value=1, step=1, value=8, max_value=16
        )
        learning_rate_multiplier = st.number_input(
            "Learning rate multiplier:",
            min_value=0.02,
            max_value=0.2,
            step=0.01,
        )
    else:
        batch_size = None
        learning_rate_multiplier = None

    train_button = st.button("Train")

    if train_button:
        if model_suffix:
            fine_tune_id = start_training(
                model_suffix=model_suffix,
                base_model=base_model,
                training_file_id=training_file_id,
                validation_file_id=validation_file_id,
                num_classes=num_classes,
                num_epochs=num_epochs,
                batch_size=batch_size,
                learning_rate_multiplier=learning_rate_multiplier,
            )
            st.success(f"Fine-tune with id '{fine_tune_id}' has been created.")
        else:
            st.error("Please, define a valid model suffix.")
