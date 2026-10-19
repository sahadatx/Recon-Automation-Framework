import re
import time
from pathlib import Path


def create_directory(directory: str) -> None:


    Path(directory).mkdir(parents=True, exist_ok=True)


def read_file(file_path: str) -> list[str]:


    path = Path(file_path)

    if not path.exists():
        return []

    with path.open("r", encoding="utf-8") as file:

        return [line.strip() for line in file if line.strip()]


def write_file(file_path: str, data: list[str]) -> None:


    path = Path(file_path)

    create_directory(path.parent)

    with path.open("w", encoding="utf-8") as file:

        for item in data:
            file.write(f"{item}\n")


def timer(start_time: float) -> float:


    return round(time.time() - start_time, 2)


def validate_domain(domain: str) -> bool:


    pattern = (
        r"^(?:[a-zA-Z0-9]"
        r"(?:[a-zA-Z0-9-]{0,61}"
        r"[a-zA-Z0-9])?\.)+"
        r"[A-Za-z]{2,}$"
    )

    return bool(re.fullmatch(pattern, domain.strip()))
