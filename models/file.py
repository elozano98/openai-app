from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

import streamlit as st
import openai


@dataclass
class File:
    id: str
    bytes: int
    filename: Optional[float]
    purpose: str
    created_at: datetime

    @classmethod
    def from_openai_response(cls, response: dict) -> File:
        return File(
            id=response["id"],
            bytes=response["bytes"],
            filename=response["filename"],
            purpose=response["purpose"],
            created_at=datetime.fromtimestamp(response["created_at"]),
        )

    def display(self) -> None:
        with st.expander(self.id):
            self._show_info()
            self._show_actions()

    def delete(self) -> None:
        openai.File.delete(self.id)

    def _show_info(self) -> None:
        st.markdown("**Information:**")
        st.text_input("Filename:", value=self.filename, key=f"{self.id}-filename")
        st.text_input("Bytes:", value=self.bytes, key=f"{self.id}-bytes")
        st.text_input("Purpose:", value=self.purpose, key=f"{self.id}-purpose")
        st.text_input("Created at:", value=self.created_at, key=f"{self.id}-created-at")

    def _show_actions(self) -> None:
        st.markdown("**Actions:**")
        st.button("Delete", on_click=self.delete, key=f"{self.id}-delete")
