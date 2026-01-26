import sys
import shutil
import subprocess
import os
import time

def ensure_package_manager():
    """
    Checks if the OS has the right tools (Brew/APT/Winget).
    If missing, attempts to install them (Mac) or warns the user (Windows/Linux).
    """
    system_os = sys.platform

    # ==========================
    # 🍎 MAC OS LOGIC (Homebrew)
    # ==========================
    if system_os == "darwin":
        # 1. Check if brew is already available
        if shutil.which("brew"):
            print("✅ Homebrew is already installed.")
            return True
        
        # 2. If not, try to install it
        print("⚠️  Homebrew not found. Initiating Installation...")
        print("🛑 NOTE: You may be asked for your password.")
        time.sleep(2)

        install_cmd = '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
        
        try:
            # We use shell=True because we are piping curl into bash
            subprocess.check_call(install_cmd, shell=True)
            
            # 3. CRITICAL: Apple Silicon / Intel Path Fix
            # Homebrew isn't in PATH immediately after install. We must add it manually for this session.
            possible_paths = ["/opt/homebrew/bin/brew", "/usr/local/bin/brew"]
            for p in possible_paths:
                if os.path.exists(p):
                    print(f"🔗 Hooking into Homebrew at {p}...")
                    # Add to Python's environment for this run
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
        # Check for APT (Debian/Ubuntu)
        if shutil.which("apt-get"):
            print("✅ APT (Debian/Ubuntu) detected.")
            print("🔄 Updating package catalog...")
            try:
                # Update silently (-qq) to keep logs clean, but check=True to catch sudo failures
                subprocess.run(["sudo", "apt", "update", "-qq"], check=True)
                return True
            except subprocess.CalledProcessError:
                print("❌ Failed to update APT. Do you have sudo privileges?")
                return False
        
        # Check for DNF (Fedora/RHEL)
        elif shutil.which("dnf"):
            print("✅ DNF (Fedora/RHEL) detected.")
            return True
            
        else:
            print("❌ Unknown Linux distribution. This script currently supports apt (Ubuntu) and dnf (Fedora).")
            return False
    
    # ==========================
    # 🪟 WINDOWS LOGIC (Winget)
    # ==========================
    elif system_os == "win32":
        if shutil.which("winget"):
            print("✅ Winget is detected.")
            return True
        else:
            print("❌ Winget is missing.")
            print("   On Windows 10/11, this is rare. Please update 'App Installer' from the Microsoft Store.")
            return False

    return False