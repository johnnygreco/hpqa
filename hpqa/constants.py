from pathlib import Path

__all__ = ["REPO_PATH", "DATA_PATH", "LOCAL_DATA_PATH"]


REPO_PATH = Path(__file__).parent.parent
DATA_PATH = REPO_PATH / "corpus"
LOCAL_DATA_PATH = REPO_PATH / "local_data"
