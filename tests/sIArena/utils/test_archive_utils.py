from pathlib import Path
import tempfile
import unittest
import zipfile

from sIArena.utils.archive_utils import extract_zip_archive, iter_files_with_suffix


class TestArchiveUtils(unittest.TestCase):
    def test_extract_zip_archive_and_iter_files_with_suffix(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            source_dir = tmp_path / "source"
            source_dir.mkdir()
            (source_dir / "a.ipynb").write_text("{}", encoding="utf-8")
            (source_dir / "b.txt").write_text("x", encoding="utf-8")

            zip_path = tmp_path / "sample.zip"
            with zipfile.ZipFile(zip_path, "w") as archive:
                archive.write(source_dir / "a.ipynb", arcname="nested/a.ipynb")
                archive.write(source_dir / "b.txt", arcname="nested/b.txt")

            extracted_dir = tmp_path / "extracted"
            extract_zip_archive(zip_path, extracted_dir)
            notebook_paths = list(iter_files_with_suffix(extracted_dir, ".ipynb"))

        self.assertEqual(len(notebook_paths), 1)
        self.assertEqual(notebook_paths[0].name, "a.ipynb")
