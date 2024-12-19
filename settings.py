from pathlib import Path

BASE_PATH = Path(__file__).parent
LOGS_PATH = BASE_PATH / "logs"
LOCAL_STORE_PATH = BASE_PATH / "data"
DATASET_PATH = LOCAL_STORE_PATH / "dataset"
LOGS_PATH.mkdir(exist_ok=True)
LOCAL_STORE_PATH.mkdir(exist_ok=True)
DATASET_PATH.mkdir(exist_ok=True)
