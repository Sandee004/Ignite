import sys
import subprocess
import time
from backend.database import set_state
from backend.services.system import ensure_package_manager
from backend.services.homebrew import resolve_app_id

def run_installation_task(app_names):
    # 1. Init State
    state = {
        "status": "running",
        "queue": app_names,
        "completed": [],
        "failed": [], # List of dicts: [{"name": "xyz", "reason": "..."}]
        "current_app": None
    }
    set_state(state)

    # 2. Pre-flight Check
    if not ensure_package_manager():
        state["status"] = "error"
        set_state(state)
        return

    # 3. Main Loop
    for app_name in app_names:
        state["current_app"] = app_name
        set_state(state)

        # A. Resolve ID (e.g., "Chrome" -> "google-chrome")
        target_id = resolve_app_id(app_name)
        
        if not target_id:
            print(f"⚠️ Not found: {app_name}")
            state["failed"].append({
                "name": app_name, 
                "reason": "App not found in Homebrew database"
            })
            set_state(state)
            continue

        # B. Prepare Command
        cmd = []
        
        # === MAC OS LOGIC ===
        if sys.platform == "darwin":
            # 1. Check if Homebrew thinks it is already installed
            check_receipt = subprocess.run(
                ["brew", "list", "--cask", target_id], 
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.DEVNULL
            )
            
            if check_receipt.returncode == 0:
                print(f"✅ {app_name} is already installed.")
                state["completed"].append(app_name)
                set_state(state)
                continue

            # 2. If not installed, Install it (using --force to fix broken links)
            print(f"⬇️  Installing {target_id}...")
            cmd = ["brew", "install", "--cask", "--force", target_id]
            
        # === WINDOWS LOGIC ===
        elif sys.platform == "win32":
            cmd = ["winget", "install", "--id", target_id, "-e"]
        
        # === LINUX LOGIC ===
        elif sys.platform == "linux":
            cmd = ["sudo", "apt", "install", "-y", target_id]

        # C. Execute Install
        try:
            # Run the command and capture any error messages
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            print(f"✨ Successfully installed {app_name}")
            state["completed"].append(app_name)
            
        except subprocess.CalledProcessError as e:
            # Extract the actual error message from the logs
            error_msg = e.stderr.strip().split('\n')[-1] if e.stderr else "Unknown error"
            print(f"❌ Failed: {app_name} -> {error_msg}")
            
            state["failed"].append({
                "name": app_name, 
                "reason": error_msg
            })
            
        except Exception as e:
            print(f"❌ Unexpected Error: {e}")
            state["failed"].append({
                "name": app_name, 
                "reason": str(e)
            })
        
        # Update DB after every step
        set_state(state)

    # 4. Finish
    state["status"] = "completed"
    state["current_app"] = None
    set_state(state)