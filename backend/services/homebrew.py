import subprocess
import sys
import shutil

def resolve_app_id(user_input):
    """
    Finds the correct package ID based on the OS.
    - Mac: brew
    - Windows: winget
    - Linux: apt
    """
    cleaned_input = user_input.lower().strip()
    system_os = sys.platform
    print(f"🔍 [{system_os}] Resolving: '{cleaned_input}'...")

    # ==========================
    # 🍎 MAC OS (Homebrew)
    # ==========================
    if system_os == "darwin":
        # 1. Exact Check
        try:
            subprocess.run(["brew", "info", "--cask", cleaned_input], 
                           check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return cleaned_input
        except subprocess.CalledProcessError:
            pass

        # 2. Search
        try:
            res = subprocess.run(["brew", "search", "--cask", cleaned_input], capture_output=True, text=True)
            candidates = res.stdout.strip().split()
            filtered = [c for c in candidates if "font-" not in c]
            return min(filtered, key=len) if filtered else None
        except:
            return None

    # ==========================
    # 🪟 WINDOWS (Winget)
    # ==========================
    elif system_os == "win32":
        # Winget doesn't have a simple "info" command that returns exit code 0/1 cleanly.
        # We rely on search.
        try:
            # We limit to 1 result (-n 1) to get the best match quickly
            cmd = ["winget", "search", cleaned_input, "--source", "winget", "-n", "1"]
            res = subprocess.run(cmd, capture_output=True, text=True)
            
            # Winget output is a table. This is a simplified parser.
            # Real-world parsing is harder, but this works for a portfolio demo.
            if "No package found" in res.stdout:
                return None
            
            # If successful, we assume the user input (like 'Firefox') 
            # maps close enough to an ID, or we return the input itself to let winget try its best.
            # Ideally, you parse the 'Id' column, but that's complex text processing.
            # For this level: Return the input. Winget is smart enough to handle "firefox".
            return cleaned_input 
        except:
            return None

    # ==========================
    # 🐧 LINUX (APT)
    # ==========================
    elif system_os == "linux":
        # 1. Exact Check
        try:
            # apt-cache policy returns info if installed or available
            res = subprocess.run(["apt-cache", "policy", cleaned_input], capture_output=True, text=True)
            if "Candidate:" in res.stdout and "(none)" not in res.stdout:
                return cleaned_input
        except:
            pass

        # 2. Search
        try:
            # apt-cache search returns "name - description"
            cmd = ["apt-cache", "search", "--names-only", cleaned_input]
            res = subprocess.run(cmd, capture_output=True, text=True)
            
            lines = res.stdout.strip().split('\n')
            if not lines:
                return None
            
            # Get the first word of the first result (the package name)
            # Example: "vlc - multimedia player" -> "vlc"
            best_match = lines[0].split()[0]
            return best_match
        except:
            return None

    return None