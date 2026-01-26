from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from typing import List
import subprocess
import requests
import sys
import shutil
import os
import time
from dotenv import load_dotenv
from .config import build_frontend, DIST_DIR
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

build_frontend()
load_dotenv()

app = FastAPI(
    title="1gnite API",
    description="API for 1gnite",
    version="1.0.0"
)

# 🛑 SPEED HACK (Mac Only)
os.environ["HOMEBREW_NO_AUTO_UPDATE"] = "1"

# --- 1. MEMORY CACHE ---
HOMEBREW_CACHE = []

def refresh_homebrew_cache():
    global HOMEBREW_CACHE
    print("🌍 Fetching latest apps from Homebrew API...")
    try:
        url = "https://formulae.brew.sh/api/cask.json"
        response = requests.get(url)
        if response.status_code == 200:
            raw_data = response.json()
            HOMEBREW_CACHE = [] 
            for app in raw_data:
                HOMEBREW_CACHE.append({
                    "id": app.get("token"),
                    "names": app.get("name", [])
                })
            print(f"✅ Loaded {len(HOMEBREW_CACHE)} apps into memory.")
        else:
            print("❌ Failed to fetch Homebrew data.")
    except Exception as e:
        print(f"❌ Error: {e}")

refresh_homebrew_cache()

# --- 2. MODELS (Fixed: Defined directly here) ---
class InstallRequest(BaseModel):
    apps: List[str]

# --- 3. SYSTEM CHECKS (The Bootstrapper) ---
def ensure_package_manager():
    """
    Checks if the OS has the right tools (Brew/APT/Winget).
    """
    system_os = sys.platform

    # ==========================
    # 🍎 MAC OS LOGIC (Homebrew)
    # ==========================
    if system_os == "darwin":
        if shutil.which("brew"):
            print("✅ Homebrew is already installed.")
            return True
        
        print("⚠️  Homebrew not found. Initiating Installation...")
        print("🛑 NOTE: You may be asked for your password.")
        time.sleep(2)

        install_cmd = '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
        
        try:
            subprocess.check_call(install_cmd, shell=True)
            
            # Post-Install PATH Fix for Apple Silicon
            possible_paths = ["/opt/homebrew/bin/brew", "/usr/local/bin/brew"]
            for p in possible_paths:
                if os.path.exists(p):
                    print(f"🔗 Hooking into Homebrew at {p}...")
                    os.environ["PATH"] += os.pathsep + os.path.dirname(p)
                    break
            return True
        except subprocess.CalledProcessError:
            print("❌ Critical Fail: Could not install Homebrew.")
            return False

    # ==========================
    # 🐧 LINUX LOGIC (APT/DNF)
    # ==========================
    elif system_os == "linux":
        if shutil.which("apt-get"):
            print("✅ APT (Debian/Ubuntu) detected.")
            # Only update if necessary (skipping for speed in this demo, but good for prod)
            return True
        elif shutil.which("dnf"):
            print("✅ DNF (Fedora/RHEL) detected.")
            return True
        else:
            print("❌ Unknown Linux distro. Only apt/dnf supported.")
            return False
    
    # ==========================
    # 🪟 WINDOWS LOGIC (Winget)
    # ==========================
    elif system_os == "win32":
        if shutil.which("winget"):
            print("✅ Winget is detected.")
            return True
        else:
            print("❌ Winget is missing. Please update 'App Installer' from Store.")
            return False


# --- 4. THE INSTALLER LOGIC ---
def run_installation_task(app_names: List[str]):
    print(f"🚀 [Background Task] Received order for: {app_names}")
    
    # A. PRE-FLIGHT CHECK
    if not ensure_package_manager():
        print("❌ [Background Task] Aborted: No package manager found.")
        return

    system_os = sys.platform
    
    # B. INSTALL LOOP
    for user_input in app_names:
        # 1. Resolve Name
        target_id = None
        cleaned_input = user_input.lower().strip()
        
        for app in HOMEBREW_CACHE:
            if app['id'] == cleaned_input:
                target_id = app['id']
                break
            if any(cleaned_input in name.lower() for name in app['names']):
                target_id = app['id']
                break
        
        if not target_id:
            print(f"⚠️  [Background Task] '{user_input}' not found in database.")
            continue

        # 2. Build Command
        cmd = []
        if system_os == "darwin":
            # Smart Check
            check = subprocess.run(["brew", "list", "--cask", target_id], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if check.returncode == 0:
                print(f"✅ [Background Task] {target_id} is already installed.")
                continue
            print(f"⬇️  [Background Task] Installing {target_id}...")
            cmd = ["brew", "install", "--cask", target_id]
        
        # 🐧 ADDED LINUX LOGIC HERE
        elif system_os == "linux":
             # Note: Using the Mac ID on Linux is a "Best Guess". 
             # Ideally, you'd map "google-chrome" (mac) -> "google-chrome-stable" (linux)
            print(f"🐧 [Background Task] Installing {target_id} via APT...")
            cmd = ["sudo", "apt", "install", "-y", target_id]

        elif system_os == "win32":
            print(f"🪟 [Background Task] Installing {target_id}...")
            cmd = ["winget", "install", "--id", target_id, "-e"]

        # 3. Execute
        try:
            # We use subprocess.run so we can catch errors without crashing the server
            result = subprocess.run(cmd, check=True, text=True, capture_output=True)
            print(f"✨ [Background Task] {target_id} installed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"❌ [Background Task] Failed to install {target_id}.")
            print(f"   Reason: {e.stderr}")

# --- 5. ENDPOINT ---
@app.post("/install")
async def trigger_install(payload: InstallRequest, background_tasks: BackgroundTasks):
    if not payload.apps:
        raise HTTPException(status_code=400, detail="List cannot be empty")

    background_tasks.add_task(run_installation_task, payload.apps)

    return {
        "status": "Accepted", 
        "message": "Installation started in background.",
        "monitor": "Check your server terminal for logs."
    }




# ------------------------------
# Static Files & React Routing
# ------------------------------
# Safety check: Ensure the folder exists before mounting, or Uvicorn crashes.
assets_path = os.path.join(DIST_DIR, "assets")
if os.path.exists(assets_path):
    app.mount("/assets", StaticFiles(directory=assets_path), name="assets")
else:
    print(f"⚠️ Warning: Assets folder not found at {assets_path}. Frontend might look broken.")

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    file_path = os.path.join(DIST_DIR, "favicon.ico")
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"error": "Favicon not found"}

@app.get("/{full_path:path}", include_in_schema=False)
async def serve_react(full_path: str):
    index_path = os.path.join(DIST_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {
        "error": "Frontend build not found.", 
        "detail": "Please check console logs to see if 'npm run build' failed."
    }
