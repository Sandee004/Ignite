import subprocess
import shutil
import sys
import os
import time

# 🛑 STOP HOMEBREW AUTO-UPDATE (Speed Hack)
os.environ["HOMEBREW_NO_AUTO_UPDATE"] = "1"

# --- 1. The Bootstrapper ---
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
        # We only check for APT (Ubuntu/Debian) or DNF (Fedora)
        if shutil.which("apt-get"):
            print("✅ APT (Debian/Ubuntu) detected.")
            print("🔄 Updating package catalog...")
            try:
                # We update silently (-qq) to keep terminal clean
                subprocess.run(["sudo", "apt", "update", "-qq"], check=True)
                return True
            except subprocess.CalledProcessError:
                print("❌ Failed to update APT. Sudo required.")
                return False
        
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

# --- 2. The App Installer ---
def install_lightweight_app(mac_app, mac_path, win_id, linux_app):
    system_os = sys.platform

    # MAC LOGIC
    if system_os == "darwin":
        if os.path.exists(f"/Applications/{mac_path}"):
            print(f"✅ Found {mac_path} in Applications. Skipping.")
            return
        
        # Check Homebrew Database
        check_cmd = ["brew", "list", "--cask", mac_app]
        is_tracked = subprocess.run(check_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0
        
        if is_tracked:
            print(f"✅ Homebrew says {mac_app} is installed. Skipping.")
            return

        print(f"⬇️  Downloading {mac_app}...")
        cmd = ["brew", "install", "--cask", mac_app]

    # LINUX LOGIC
    elif system_os == "linux":
        if shutil.which(linux_app):
            print(f"✅ Found '{linux_app}' binary. Skipping.")
            return

        print(f"⬇️  Installing {linux_app} via APT...")
        cmd = ["sudo", "apt", "install", "-y", linux_app]

    # WINDOWS LOGIC
    elif system_os == "win32":
        # Check if installed via Winget
        check_cmd = f"winget list -e --id {win_id}"
        is_installed = subprocess.run(check_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0

        if is_installed:
            print(f"✅ {win_id} is already installed. Skipping.")
            return

        print(f"⬇️  Installing {win_id}...")
        cmd = ["winget", "install", "--id", win_id, "-e", "--source", "winget"]

    else:
        print("❌ Unsupported OS.")
        return

    # EXECUTE
    try:
        subprocess.run(cmd, check=True)
        print(f"✨ Success! {mac_app if system_os == 'darwin' else linux_app} installed.")
    except subprocess.CalledProcessError:
        print(f"❌ Failed to install.")

# --- RUN IT ---
if __name__ == "__main__":
    print("🔥 Ignite: Multi-OS Test")
    
    # STEP 1: Ensure the tools exist (Fixed: Added this call!)
    if ensure_package_manager():
        
        # STEP 2: Install the App
        install_lightweight_app(
            mac_app="rectangle",           # Verified Homebrew Name
            mac_path="Rectangle.app",      # Actual App Name
            win_id="Microsoft.PowerToys",  # Windows Equivalent (PowerToys)
            linux_app="htop"               # Linux (Simple monitor tool, safer test)
        )

        