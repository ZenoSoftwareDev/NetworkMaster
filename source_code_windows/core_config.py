import os
import sys
import subprocess

# --- 1. USTALANIE ŚCIEŻKI GŁÓWNEJ ---
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --- 2. GŁÓWNE FOLDERY ---
DB_DIR = os.path.join(BASE_DIR, "core_data")
REPORTS_DIR = os.path.join(BASE_DIR, "Reports")

# --- 3. DANE APLIKACJI ---
APP_ID = "NetworkMaster"
APP_PLATFORM = "windows"

# --- 4. ŚCIEŻKI PLIKÓW DANYCH ---
FIRST_RUN_FLAG = os.path.join(DB_DIR, "installed.flag")
DB_IP = os.path.join(DB_DIR, "ip_registry.sys")
DB_WOL = os.path.join(DB_DIR, "wol_registry.sys") 
DB_WIFI = os.path.join(DB_DIR, "wifi_vault.dat")  

# --- FUNKCJE POMOCNICZE ---
def init():
    """Tworzy niezbędne foldery przy starcie."""
    if not os.path.exists(DB_DIR): os.makedirs(DB_DIR)
    if not os.path.exists(REPORTS_DIR): os.makedirs(REPORTS_DIR)
    
    for f in [DB_IP, DB_WOL]:
        if not os.path.exists(f):
            with open(f, "w", encoding='utf-8') as file: file.write("")

def get_adapters_info():
    """Pobiera informacje o kartach sieciowych (używane w GUI)."""
    cmd = 'powershell "Get-NetAdapter | Select-Object Name, Status, LinkSpeed | ConvertTo-Csv -NoTypeInformation"'
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, shell=True).stdout
        info = {}
        lines = res.strip().split('\n')
        if len(lines) > 1:
            for line in lines[1:]:
                parts = line.replace('"', '').split(',')
                if len(parts) >= 3:
                    name = parts[0]
                    status = parts[1]
                    speed = parts[2]
                    is_up = status.strip().upper() == "UP"
                    info[name] = {"status": "UP" if is_up else "DOWN", "speed": speed.strip() if is_up else "--", "up": is_up}
        return info
    except:
        return {}