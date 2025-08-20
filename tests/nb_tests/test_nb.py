import pytest
from pathlib import Path
import logging
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor, CellExecutionError
from typing import List

logger = logging.getLogger(__name__)

NOTEBOOK_DIR = Path("./Notebooks")
SEARCH = "**/*.ipynb"
TIMEOUT = 600
SKIP_NOTEBOOKS = ["RAG_Agent.ipynb"]


def get_notebooks() -> List[Path]:
    """Get all notebooks to test"""
    return [
        f
        for f in NOTEBOOK_DIR.glob(SEARCH)
        if f.name not in SKIP_NOTEBOOKS
        and ".ipynb_checkpoints" not in str(f.absolute())
    ]


def run_notebook(notebook: Path) -> None:
    """Execute and validate notebook"""
    logger.info(f"Testing notebook: {notebook.name}")

    with notebook.open() as f:
        nb = nbformat.read(f, as_version=4)

    code_cells = len([c for c in nb.cells if c.cell_type == "code"])
    logger.info(f"- Total code cells: {code_cells}")

    ep = ExecutePreprocessor(timeout=TIMEOUT)
    ep.preprocess(nb, {"metadata": {"path": str(notebook.parent)}})

    assert code_cells > 0, f"No code cells found in {notebook.name}"
    logger.info(f"✓ {notebook.name} executed successfully")


# Dynamically create test functions for each notebook
for notebook in get_notebooks():

    def make_test(nb: Path):
        def test_func():
            run_notebook(nb)

        return test_func

    test_name = f"test_{notebook.stem.lower()}"
    # Add test to module namespace
    globals()[test_name] = make_test(notebook)
