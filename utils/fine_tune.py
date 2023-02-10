from typing import List, Optional

import openai
from models import FineTune


def get_fine_tunes(n: Optional[int] = None) -> List[FineTune]:
    all_fine_tunes = openai.FineTune.list()["data"]
    all_fine_tunes.sort(key=lambda x: x["created_at"], reverse=True)
    return [FineTune.with_id(ft["id"]) for ft in all_fine_tunes[:n]]
