from typing import List

import openai
from models import FineTune


def get_last_n_fine_tunes(n: int) -> List[FineTune]:
    all_fine_tunes = openai.FineTune.list()["data"]
    all_fine_tunes.sort(key=lambda x: x["created_at"], reverse=True)
    return [FineTune.with_id(ft["id"]) for ft in all_fine_tunes[:n]]
