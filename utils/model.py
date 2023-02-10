from typing import List

import openai

from models import Model


def get_models() -> List[Model]:
    models_info = openai.Model.list()["data"]
    models_info.sort(key=lambda x: x["created"], reverse=True)
    return [Model.from_openai_response(info) for info in models_info]


def generate_completion(
    *, text: str, model_id: str, max_tokens: int, temperature: float
) -> str:
    response = openai.Completion.create(
        model=model_id,
        max_tokens=max_tokens,
        temperature=temperature,
        n=1,
        prompt=text,
    )
    return response["choices"][0]["text"]
