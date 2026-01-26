from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel
from typing import List
from backend.services.installer import run_installation_task
from backend.database import get_state, reset_state

router = APIRouter()

class InstallRequest(BaseModel):
    apps: List[str]

@router.post("/install")
async def trigger_install(payload: InstallRequest, background_tasks: BackgroundTasks):
    if not payload.apps:
        raise HTTPException(status_code=400, detail="List cannot be empty")
    
    reset_state()
    background_tasks.add_task(run_installation_task, payload.apps)
    return {"status": "Accepted"}

@router.get("/progress")
def read_progress():
    return get_state()