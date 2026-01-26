# --- 2. MODELS ---
from pydantic import BaseModel
from typing import List

class InstallRequest(BaseModel):
    apps: List[str]
