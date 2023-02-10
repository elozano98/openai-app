import openai
from typing import List
from models import Model


def get_models() -> List[Model]:
    models_info = openai.Model.list()["data"]
    models_info.sort(key=lambda x: x["created"], reverse=True)
    return [Model.from_openai_response(info) for info in models_info]
