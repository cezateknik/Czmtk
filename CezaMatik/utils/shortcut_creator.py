import os
import sys
import platform
import subprocess
import winreg

def get_desktop_path():
    """Get the correct desktop path for the current user"""
    try:
        if platform.system() == "Windows":
            try:
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders") as key:
                    desktop_path = winreg.QueryValueEx(key, "Desktop")[0]
                    if os.path.exists(desktop_path):
                        return desktop_path
            except Exception:
                pass

            possible_paths = [
                os.path.join(os.environ.get('USERPROFILE', ''), 'Desktop'),
                os.path.join(os.environ.get('USERPROFILE', ''), 'Masaüstü'),
                os.path.join(os.environ.get('HOME', ''), 'Desktop'),
                os.path.join(os.path.expanduser("~"), 'Desktop'),
                os.path.join(os.path.expanduser("~"), 'Masaüstü')
            ]

            for path in possible_paths:
                if path and os.path.exists(path):
                    return path

            user_profile = os.environ.get('USERPROFILE')
            if user_profile:
                desktop_path = os.path.join(user_profile, 'Desktop')
                os.makedirs(desktop_path, exist_ok=True)
                return desktop_path

        elif platform.system() == "Darwin":
            return os.path.join(os.path.expanduser("~"), "Desktop")
        elif platform.system() == "Linux":
            return os.path.join(os.path.expanduser("~"), "Desktop")
            
        return None
    except Exception:
        return None

def create_desktop_shortcut(target_path):
    """
    Creates a desktop shortcut to the application.
    
    Args:
        target_path (str): Path to the executable or Python script
    """
    try:
        system = platform.system()
        app_name = "CezaMatik"
        
        # Eğer frozen (exe) ise, sys.executable kullan
        if getattr(sys, 'frozen', False):
            target_path = sys.executable
        
        desktop_path = get_desktop_path()
        if not desktop_path:
            return False
            
        if system == "Windows":
            create_windows_shortcut(target_path, desktop_path, app_name)
        elif system == "Darwin":
            create_macos_shortcut(target_path, desktop_path, app_name)
        elif system == "Linux":
            create_linux_shortcut(target_path, desktop_path, app_name)
            
    except Exception:
        pass

def create_windows_shortcut(target_path, desktop_path, app_name):
    """Create a shortcut on Windows using PowerShell"""
    try:
        shortcut_path = os.path.join(desktop_path, f"{app_name}.lnk")
        
        if os.path.exists(shortcut_path):
            return
            
        os.makedirs(os.path.dirname(shortcut_path), exist_ok=True)
        
        # Yolları düzelt ve kaçış karakterlerini ekle
        target_path = os.path.normpath(target_path).replace('\\', '\\\\')
        working_dir = os.path.normpath(os.path.dirname(target_path)).replace('\\', '\\\\')
        shortcut_path = os.path.normpath(shortcut_path).replace('\\', '\\\\')
        
        # Eğer exe dosyası ise, doğrudan hedef olarak kullan
        if getattr(sys, 'frozen', False):
            ps_command = f"""
            $WshShell = New-Object -comObject WScript.Shell
            $Shortcut = $WshShell.CreateShortcut('{shortcut_path}')
            $Shortcut.TargetPath = '{target_path}'
            $Shortcut.WorkingDirectory = '{working_dir}'
            $Shortcut.Description = '{app_name}'
            $Shortcut.IconLocation = '{target_path},0'
            $Shortcut.Save()
            """
        else:
            # Python script için pythonw.exe kullan
            ps_command = f"""
            $WshShell = New-Object -comObject WScript.Shell
            $Shortcut = $WshShell.CreateShortcut('{shortcut_path}')
            $Shortcut.TargetPath = 'pythonw.exe'
            $Shortcut.Arguments = '"{target_path}"'
            $Shortcut.WorkingDirectory = '{working_dir}'
            $Shortcut.Description = '{app_name}'
            $Shortcut.Save()
            """
        
        subprocess.run(["powershell", "-Command", ps_command], 
                      capture_output=True, text=True, check=False)
            
    except Exception:
        pass

def create_macos_shortcut(target_path, desktop_path, app_name):
    """Create an alias on macOS"""
    try:
        shortcut_path = os.path.join(desktop_path, f"{app_name}.command")
        
        if os.path.exists(shortcut_path):
            return
        
        os.makedirs(os.path.dirname(shortcut_path), exist_ok=True)
            
        with open(shortcut_path, 'w') as f:
            f.write(f"""#!/bin/bash
cd "{os.path.dirname(target_path)}"
python "{target_path}"
""")
        
        os.chmod(shortcut_path, 0o755)
        
    except Exception:
        pass

def create_linux_shortcut(target_path, desktop_path, app_name):
    """Create a .desktop file on Linux"""
    try:
        shortcut_path = os.path.join(desktop_path, f"{app_name}.desktop")
        
        if os.path.exists(shortcut_path):
            return
        
        os.makedirs(os.path.dirname(shortcut_path), exist_ok=True)
            
        with open(shortcut_path, 'w') as f:
            f.write(f"""[Desktop Entry]
Version=1.0
Type=Application
Name={app_name}
Exec=python "{target_path}"
Path={os.path.dirname(target_path)}
Terminal=false
StartupNotify=true
""")
        
        os.chmod(shortcut_path, 0o755)
        
    except Exception:
        pass