from pathlib import Path
from typing import Iterable, Union
import zipfile


def extract_zip_archive(zip_path: Union[str, Path], destination: Union[str, Path]) -> Path:
    zip_path = Path(zip_path)
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(zip_path, "r") as archive:
        archive.extractall(destination)

    return destination


def iter_files_with_suffix(root: Union[str, Path], suffix: str) -> Iterable[Path]:
    root = Path(root)
    for path in sorted(root.rglob(f"*{suffix}")):
        if path.is_file():
            yield path
