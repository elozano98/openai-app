import openai
from models.file import File
from typing import List


def get_all_files() -> List[File]:
    files = openai.File.list()["data"]
    files.sort(key=lambda x: x["created_at"], reverse=True)
    return [File.from_openai_response(f) for f in files]
