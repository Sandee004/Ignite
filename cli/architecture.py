import platform
import sys
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
    elif system_os == "windows":
        info["os"] = "windows"
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

# --- Quick Test ---
if __name__ == "__main__":
    details = get_system_info()
    print("🖥️  System Detected:")
    print(f"   • OS: {details['os'].upper()}")
    print(f"   • Arch: {details['arch'].upper()}")
    if details['is_rosetta']:
        print("   • Note: Running under Rosetta Translation")