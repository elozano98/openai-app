from typing import List, Optional

import openai
from models import FineTune


def get_fine_tunes(n: Optional[int] = None) -> List[FineTune]:
    all_fine_tunes = openai.FineTune.list()["data"]
    all_fine_tunes.sort(key=lambda x: x["created_at"], reverse=True)
    return [FineTune.with_id(ft["id"]) for ft in all_fine_tunes[:n]]


def start_training(
    *,
    model_suffix: str,
    base_model: str,
    training_file_id: str,
    num_epochs: int,
    validation_file_id: Optional[str],
    num_classes: Optional[int],
    batch_size: Optional[int],
    learning_rate_multiplier: Optional[float],
) -> str:
    kwargs = {
        "suffix": model_suffix,
        "model": base_model,
        "training_file": training_file_id,
        "n_epochs": num_epochs,
    }
    if validation_file_id:
        kwargs["validation_file"] = validation_file_id
        if num_classes:
            kwargs["compute_classification_metrics"] = True
            kwargs["classification_n_classes"] = num_classes
    if batch_size:
        kwargs["batch_size"] = batch_size
    if learning_rate_multiplier:
        kwargs["learning_rate_multiplier"] = learning_rate_multiplier

    response = openai.FineTune.create(**kwargs)
    return response["id"]
