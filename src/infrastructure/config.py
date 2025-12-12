import os
from typing import Dict, Tuple


class Settings:
    DATABASE_PATH: str = os.getenv("DB_PATH", "logs.db")
    EXCEL_OUTPUT_DIR: str = os.getenv("EXCEL_DIR", ".")

    SUPPORTED_CITIES: Dict[str, Tuple[float, float]] = {
        "москва": (55.7522, 37.6156),
        "киев": (50.4501, 30.5234),
        "минск": (53.9045, 27.5615),
        # ...
    }


settings = Settings()