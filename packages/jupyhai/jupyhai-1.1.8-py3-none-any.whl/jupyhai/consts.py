# WARNING: This module may not import anything from within jupyhai
#          as it is being imported by `setup.py` – not all requirements
#          required are necessarily available during that import time.
import os
from typing import List, Optional

HOST: str = os.environ.get("VALOHAI_HOST", "https://app.valohai.com")
ROOT_DIRECTORY: str = os.getcwd()
NOTEBOOK_INSTANCE_ID: Optional[str] = os.environ.get("VALOHAI_NOTEBOOK_INSTANCE_ID")
PROJECT_ID: Optional[str] = os.environ.get("VALOHAI_PROJECT_ID")
DEFAULT_IMAGE: str = "valohai/pypermill"
DEFAULT_TITLE: str = "Notebook execution"
PAPERMILL_VERSION: str = "8445fb0d984af248d6946b6672b3e42633f21e51"
DEFAULT_IGNORE: List[str] = ["*.ipynb"]
JUPYTER_VERSION: str = "1.0.0"
SEABORN_VERSION: str = "0.9.0"
NBCONVERT_VERSION: str = "5.5.0"
JUPYTER_EXECUTION_STEP_NAME: str = "jupyter_execution"

# These patterns are always prepended to any user ignore patterns.
ALWAYS_IGNORE: List[str] = [
    pat for pat in os.environ.get('ALWAYS_IGNORE', '').split(',') if pat
]
