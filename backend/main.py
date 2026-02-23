import os
import sys
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# Import DIST_DIR, but REMOVE build_frontend
from backend.config import DIST_DIR 
from backend.routers import install

app = FastAPI(title="Ignite API")

# 1. CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Include Routers
app.include_router(install.router)

# 3. Serve Frontend (Static Files)
# We check for 'assets' folder specifically for Vite builds
assets_path = os.path.join(DIST_DIR, "assets")

if os.path.exists(assets_path):
    app.mount("/assets", StaticFiles(directory=assets_path), name="assets")

@app.get("/{full_path:path}")
async def serve_react(full_path: str):
    # This ensures that even if the user refreshes a sub-route, 
    # FastAPI serves the index.html (Standard SPA behavior)
    index_path = os.path.join(DIST_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"error": f"Frontend build not found at {index_path}"}



import webbrowser
from threading import Timer

def open_browser():
    webbrowser.open("http://localhost:8000")

Timer(1.5, open_browser).start()

if __name__ == "__main__":
    print("🚀 Ignite is firing up...")
    print("🌍 Open your browser at http://localhost:8000")
    
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")