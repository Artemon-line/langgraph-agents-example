import os
import asyncio
import pytest
import warnings
from jupyter_core.paths import jupyter_data_dir, jupyter_runtime_dir

# Set environment variable for Jupyter paths
os.environ["JUPYTER_PLATFORM_DIRS"] = "1"


# Configure Windows event loop policy
@pytest.fixture(scope="session", autouse=True)
def windows_event_loop_policy():
    """Configure Windows to use selector event loop policy"""
    if os.name == "nt":  # Windows only
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


# Filter warnings
@pytest.fixture(autouse=True)
def ignore_jupyter_warnings():
    """Filter known Jupyter warnings"""
    warnings.filterwarnings(
        "ignore", category=DeprecationWarning, module="jupyter_client.connect"
    )
    warnings.filterwarnings("ignore", category=RuntimeWarning, module="zmq._future")
