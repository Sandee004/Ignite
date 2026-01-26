import subprocess
import shutil
import platform
import os


def get_system_info():
    """
    Detects the operating system, architecture, and whether
    the machine is running under Rosetta (Mac specific).
    """
    system_os = platform.system().lower()  # 'darwin', 'linux', 'windows'
    machine_arch = platform.machine().lower() # 'x86_64', 'arm64', 'aarch64'
    print(system_os)
    print(machine_arch)
    info = {
        "os": "unknown",
        "arch": "unknown",
        "is_rosetta": False,
        "package_manager": None
    }

    # 1. Detect OS
    if system_os == "darwin":
        info["os"] = "macos"
        if shutil.which("brew"):
            print("Homebrew is installed")
        else:
            print("Homebrew is not installed. Proceed?")
    elif system_os == "windows":
        info["os"] = "windows"
        if shutil.which("winget"):
            print("Winget exists. Proceeding")
        else:
            print("Winget not found")
    elif system_os == "linux":
        info["os"] = "linux"

    # 2. Detect Architecture (Crucial for Apple Silicon)
    if "arm" in machine_arch or "aarch64" in machine_arch:
        info["arch"] = "arm64"
    else:
        info["arch"] = "x86"

    # 3. Detect Rosetta (Mac Specific)
    # If Python thinks it's x86 but the sysctl command says translated, we are in Rosetta.
    if info["os"] == "macos" and info["arch"] == "x86":
        try:
            # sysctl -n sysctl.proc_translated returns '1' if translated, '0' if native
            result = os.popen('sysctl -n sysctl.proc_translated 2>/dev/null').read().strip()
            if result == '1':
                info["is_rosetta"] = True
                info["arch"] = "arm64" # Correcting the arch because hardware is actually ARM
        except Exception:
            pass

    return info


if shutil.which("brew"):
    print("✅ Homebrew is already installed.")
    
else:
    print("Homebrew doesn't exist on this machine")



"""
import requests

HOMEBREW_CACHE = []

def refresh_cache():
    global HOMEBREW_CACHE
    print("🌍 Fetching Homebrew Data...")
    try:
        # We fetch both Casks (Apps) and Formulae (CLI tools) if you want, 
        # but for now let's stick to Casks since you want .apps
        res = requests.get("https://formulae.brew.sh/api/cask.json")
        if res.status_code == 200:
            raw = res.json()
            HOMEBREW_CACHE = [{"id": a.get("token"), "names": a.get("name", [])} for a in raw]
            print(f"✅ Loaded {len(HOMEBREW_CACHE)} apps.")
        else:
            print("❌ Failed to fetch Homebrew data.")
    except Exception as e:
        print(f"❌ Cache Error: {e}")

# Load on start
refresh_cache()

def resolve_app_id(user_input):
    ""
    Smart Resolver:
    1. Exact Match (Best)
    2. Name Match
    3. Partial Match (Fallback)
    ""
    cleaned = user_input.lower().strip()
    
    # ----------------------------------------
    # 🕵️‍♂️ PRIORITY 1: EXACT ID MATCH
    # ----------------------------------------
    # If user types "slack", we look for ID "slack".
    # This skips "font-slackey" because "font-slackey" != "slack"
    for app in HOMEBREW_CACHE:
        if app['id'] == cleaned:
            return app['id']

    # ----------------------------------------
    # 🕵️‍♂️ PRIORITY 2: EXACT NAME MATCH
    # ----------------------------------------
    # If user types "Chrome", we find the app named "Google Chrome"
    for app in HOMEBREW_CACHE:
        # Check if the user input matches one of the known names exactly
        if any(cleaned == name.lower() for name in app['names']):
            return app['id']

    # ----------------------------------------
    # 🕵️‍♂️ PRIORITY 3: PARTIAL MATCH (The "Guess")
    # ----------------------------------------
    # Only if we found NOTHING above, do we guess.
    # We pick the SHORTEST match to avoid weird long packages.
    best_match = None
    shortest_len = float('inf')

    for app in HOMEBREW_CACHE:
        # Check ID contains input
        if cleaned in app['id']:
            if len(app['id']) < shortest_len:
                best_match = app['id']
                shortest_len = len(app['id'])
        
        # Check Names contain input
        for name in app['names']:
            if cleaned in name.lower():
                # We prefer the ID as the return value
                if len(app['id']) < shortest_len:
                    best_match = app['id']
                    shortest_len = len(app['id'])
    
    return best_match
"""