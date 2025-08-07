import pytest
from pathlib import Path
import os
import logging
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import coverage
from coverage.files import PathAliases

logger = logging.getLogger(__name__)

NOTEBOOK_DIR = Path("./Notebooks")
SKIP_NOTEBOOKS = ["RAG_Agent.ipynb"]
TIMEOUT = 600


def setup_coverage():
    """Setup coverage with proper configuration"""
    aliases = PathAliases()
    aliases.add(pattern="*/Agents/", result="Agents")

    return coverage.Coverage(
        source=["Agents"],
        branch=True,
        data_file=".coverage.nb",
        config_file=True,
        source_pkgs=["Agents"],
        include=["*/Agents/*"],
    )


@pytest.mark.parametrize(
    "notebook",
    [f for f in NOTEBOOK_DIR.glob("**/*.ipynb") if f.name not in SKIP_NOTEBOOKS],
)
def test_notebook_execution(notebook: Path, covr: bool = True):
    cov = None
    try:
        cov = setup_coverage() if covr else None
        if cov:
            cov.start()

        with open(notebook) as f:
            nb = nbformat.read(f, as_version=4)

        logger.debug("Executing notebook: %s", notebook)

        ep = ExecutePreprocessor(timeout=TIMEOUT)
        ep.preprocess(nb)

        # Stop and save coverage data
    finally:
        # Ensure coverage is stopped and saved
        if cov:
            cov.stop()
            cov.save()
