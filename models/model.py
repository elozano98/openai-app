from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import streamlit as st
import openai


@dataclass
class Model:
    BASE_MODELS = ["ada", "babbage", "curie", "davinci"]

    id: str
    base_model: Optional[str]
    owner: str
    created_at: datetime

    @classmethod
    def from_openai_response(cls, response: dict) -> Model:
        return Model(
            id=response["id"],
            owner=response["owned_by"],
            base_model=response["parent"].split(":")[0] if response["parent"] else None,
            created_at=datetime.fromtimestamp(response["created"]),
        )

    def display(self) -> None:
        with st.expander(self.id):
            self._show_info()

    def _show_info(self) -> None:
        st.markdown("**Information:**")
        st.text_input("Base model:", value=self.base_model, key=f"{self.id}-base-model")
        st.text_input("Owner:", value=self.owner, key=f"{self.id}-owner")
        st.text_input("Created at:", value=self.created_at, key=f"{self.id}-created-at")
