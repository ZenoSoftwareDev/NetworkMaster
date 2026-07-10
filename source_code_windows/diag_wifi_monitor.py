import os, subprocess, time

# Kolory
G, R, C, Y, RESET = '\033[92m', '\033[91m', '\033[96m', '\033[93m', '\033[0m'

def get_wifi_status():
    data = {
        "ssid": None,
        "bssid": "-",
        "signal": 0,
        "channel": "-",
        "radio": "-",
        "error_type": None # NOWE: Diagnoza błędu
    }
    
    try:
        # Próba pobrania danych w różnych kodowaniach
        encodings = ['cp852', 'utf-8', 'cp1250', 'latin1']
        output = ""
        
        for enc in encodings:
            try:
                cmd = "netsh wlan show interfaces"
                res = subprocess.run(cmd, capture_output=True, text=True, encoding=enc, errors='ignore', shell=True)
                if res.stdout:
                    output = res.stdout
                    break
            except: continue
            
        # --- DETEKCJA BLOKADY LOKALIZACJI ---
        output_lower = output.lower()
        if "location" in output_lower and "permission" in output_lower:
            data['error_type'] = "LOCATION_LOCKED"
            return data
            
        if "lokalizacj" in output_lower and "uprawnie" in output_lower:
             data['error_type'] = "LOCATION_LOCKED"
             return data

        # Parsowanie danych
        for line in output.split('\n'):
            line = line.strip()
            if ":" in line:
                key, val = line.split(":", 1)
                key = key.strip().lower()
                val = val.strip()
                if not val: continue 
                
                if "ssid" in key and "bssid" not in key: data['ssid'] = val
                elif "bssid" in key: data['bssid'] = val
                elif "%" in val and ("signal" in key or "sygnał" in key):
                    try: data['signal'] = int(val.replace('%', '').strip())
                    except: pass
                elif "channel" in key or "kanał" in key: data['channel'] = val
                elif "radio" in key or "typ" in key: data['radio'] = val
                
    except Exception as e:
        pass
        
    return data

def draw_signal_bar(percent):
    total_blocks = 20
    filled_blocks = int(total_blocks * percent / 100)
    bar = "█" * filled_blocks + "░" * (total_blocks - filled_blocks)
    color = R
    if percent > 40: color = Y
    if percent > 70: color = G
    return f"{color}[{bar}] {percent}%{RESET}"

def run():
    try:
        while True:
            info = get_wifi_status()
            os.system('cls')
            print(f"{C}================================================================{RESET}")
            print(f"            {Y}MONITOR SYGNAŁU WIFI (LIVE DASHBOARD){RESET}")
            print(f"{C}================================================================{RESET}")
            
            # 1. OBSŁUGA BLOKADY LOKALIZACJI
            if info['error_type'] == "LOCATION_LOCKED":
                print(f"\n {R}[!] DOSTĘP ZABLOKOWANY PRZEZ SYSTEM WINDOWS{RESET}")
                print("-" * 64)
                print(f" {Y}System Windows blokuje dostęp do informacji o sieci WiFi.{RESET}")
                print(" Aby to naprawić, musisz włączyć Usługi Lokalizacji:")
                print("\n 1. Otwórz: Ustawienia -> Prywatność i zabezpieczenia -> Lokalizacja")
                print(" 2. Włącz suwak 'Usługi lokalizacji'")
                print(" 3. Zezwól aplikacjom klasycznym na dostęp do lokalizacji")
                print("-" * 64)
            
            # 2. POPRAWNE POŁĄCZENIE
            elif info['ssid']:
                print(f" STAN:           {G}POŁĄCZONO{RESET}")
                print(f" SIEĆ (SSID):    {C}{info['ssid']}{RESET}")
                print(f" NADAJNIK (MAC): {info['bssid']}")
                print(f" KANAŁ:          {info['channel']}")
                print(f" RADIO:          {info['radio']}")
                print("-" * 64)
                print(f" JAKOŚĆ SYGNAŁU:")
                print(f" {draw_signal_bar(info['signal'])}")
                
                desc = "Krytyczny"
                if info['signal'] > 20: desc = "Słaby"
                if info['signal'] > 50: desc = "Dobry"
                if info['signal'] > 80: desc = "Doskonały"
                print(f" OCENA: {desc}")
                
            # 3. BRAK POŁĄCZENIA / INNY BŁĄD
            else:
                print(f" STAN: {R}NIE WYKRYTO AKTYWNEGO POŁĄCZENIA{RESET}")
                print(" Upewnij się, że jesteś połączony z WiFi.")
                # Jeśli to nie blokada lokalizacji, ale nadal brak danych
                if not info['error_type']:
                     print(f" {Y}[Info] Upewnij się, że lokalizacja w systemie jest włączona.{RESET}")

            print("\n [Ctrl+C] Powrót do menu")
            time.sleep(1)
            
    except KeyboardInterrupt:
        pass