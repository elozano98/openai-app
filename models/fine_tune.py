from __future__ import annotations

import os
import re
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Optional

import openai
import requests
import streamlit as st
from humanfriendly import format_timespan


@dataclass
class FineTune:
    STATUS_PENDING = "pending"
    STATUS_RUNNING = "running"
    STATUS_FAILED = "failed"
    STATUS_SUCCEEDED = "succeeded"

    id: str
    status: str
    cost: Optional[float]
    base_model: str
    model_name: Optional[str]
    hyperparameters: dict
    training_file_id: str
    validation_file_id: Optional[str]
    result_file_id: Optional[str]
    created_at: datetime
    events: List[dict]
    duration: Optional[timedelta]

    @classmethod
    def with_id(cls, fine_tune_id: str) -> FineTune:
        response = openai.FineTune.retrieve(fine_tune_id)
        return FineTune(
            id=response["id"],
            status=response["status"],
            cost=cls._extract_cost_from_events(response["events"]),
            base_model=response["model"],
            model_name=response["fine_tuned_model"],
            hyperparameters=response["hyperparams"],
            training_file_id=response["training_files"][0]["id"],
            validation_file_id=response["validation_files"][0]["id"]
            if response["validation_files"]
            else None,
            result_file_id=response["result_files"][0]["id"]
            if response["result_files"]
            else None,
            events=response["events"],
            created_at=datetime.fromtimestamp(response["created_at"]),
            duration=cls._extract_duration_from_events(response["events"])
            if len(response["events"]) > 1
            else None,
        )

    def display(self) -> None:
        with st.expander(self.id):
            self._show_information()
            if self.result_file_id:
                self._show_result_metrics()
            self._show_actions()

    def cancel(self) -> None:
        openai.FineTune.cancel(self.id)

    def delete(self) -> None:
        openai.FineTune.delete(self.id)

    @classmethod
    def _extract_cost_from_events(cls, events: List[dict]) -> Optional[float]:
        if len(events) == 1:
            return None
        match = re.search("costs \$(\d*.\d*)", events[1]["message"])
        if match:
            return float(match.group(1))
        return None

    @classmethod
    def _extract_duration_from_events(cls, events: List[dict]) -> timedelta:
        first_event_date = datetime.fromtimestamp(events[0]["created_at"])
        last_event_date = datetime.fromtimestamp(events[-1]["created_at"])
        return last_event_date - first_event_date

    def _show_information(self) -> None:
        st.markdown("**Information:**")
        col1, col2 = st.columns(2)
        if self.status == self.STATUS_SUCCEEDED:
            col1.success(self.status)
        elif self.status == self.STATUS_FAILED:
            col1.error(self.status)
        else:
            col1.warning(self.status)
        if self.cost:
            col2.info(f"Cost: ${self.cost}")
        st.text_input("Created at:", self.created_at, key=f"{self.id}-created-at")
        if self.duration:
            st.text_input(
                "Duration:", format_timespan(self.duration), key=f"{self.id}-duration"
            )
        if self.model_name:
            st.text_input("Model name:", self.model_name, key=f"{self.id}-model-name")
        st.text_input("Base model:", self.base_model, key=f"{self.id}-base-model")
        st.text_input(
            "Training File ID:",
            self.training_file_id,
            key=f"{self.id}-training-file-id",
        )
        if self.validation_file_id:
            st.text_input(
                "Validation File ID:",
                self.validation_file_id,
                key=f"{self.id}-validation-file-id",
            )
        if self.result_file_id:
            st.text_input(
                "Result File ID:",
                self.result_file_id,
                key=f"{self.id}-result-file-id",
            )
        st.text("Hyperparameters:")
        st.json(self.hyperparameters, expanded=False)
        st.text("Last event:")
        st.info(self.events[-1]["message"])

    def _show_result_metrics(self) -> None:
        response = requests.get(
            f"https://api.openai.com/v1/files/{self.result_file_id}/content",
            headers={"Authorization": f"Bearer {openai.api_key}"},
        )
        assert response.status_code == 200
        accuracy, f1_score = response.content.decode().split("\n")[-2].split(",")[-2:]
        accuracy = round(float(accuracy), 4)
        f1_score = round(float(f1_score), 4)

        st.markdown("**Results:**")

        st.text(f"Accuracy: {accuracy*100}")
        st.progress(accuracy)

        st.text(f"F1 Score: {f1_score}")
        st.progress(f1_score)

    def _show_actions(self) -> None:
        st.markdown("**Actions:**")
        if self.status in [self.STATUS_PENDING, self.STATUS_RUNNING]:
            st.button("Cancel", on_click=self.cancel, key=f"{self.id}-cancel")
        st.button("Delete", on_click=self.delete, key=f"{self.id}-delete")
