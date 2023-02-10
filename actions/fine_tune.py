import streamlit as st
from utils import get_last_n_fine_tunes


def list_fine_tunes() -> None:
    num_fine_tunes_to_show = st.number_input(
        "Number of fine-tunes to show:", min_value=1, max_value=10, value=2
    )

    fine_tunes = get_last_n_fine_tunes(num_fine_tunes_to_show)
    for f in fine_tunes:
        f.display()