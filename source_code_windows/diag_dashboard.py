import os
import time
import subprocess
import socket
import re
import core_config

G, R, C, Y, RESET = '\033[92m', '\033[91m', '\033[96m', '\033[93m', '\033[0m'

def get_live_ping():
    """Wysyła 1 szybki pakiet ping, aby sprawdzić aktualne opóźnienie."""
    try:
        cmd = "ping -n 1 -w 800 8.8.8.8"
        res = subprocess.run(cmd, capture_output=True, text=True, shell=True, encoding='cp852', errors='ignore').stdout
        match = re.search(r"(?:czas|time)[=<](\d+)ms", res, re.IGNORECASE)
        if match:
            return int(match.group(1))
        return -1
    except:
        return -1

def get_adapters_data():
    """Pobiera adresy IP oraz łączne statystyki dla wszystkich kart."""
    data = {}
    try:
        cmd_ip = 'powershell "Get-NetIPAddress -AddressFamily IPv4 -ErrorAction SilentlyContinue | Select-Object InterfaceAlias, IPAddress | ConvertTo-Csv -NoTypeInformation -Delimiter \',\'"'
        res_ip = subprocess.run(cmd_ip, capture_output=True, text=True, shell=True, encoding='cp852', errors='ignore').stdout.strip()
        
        for line in res_ip.split('\n')[1:]:
            line = line.strip()
            if line:
                parts = line.replace('"', '').split(',')
                if len(parts) >= 2:
                    name = parts[0].strip()
                    ip = parts[1].strip()
                    if name not in data: data[name] = {}
                    if ip and not ip.startswith("169.254") and ip != "127.0.0.1":
                        data[name]['ip'] = ip

        cmd_bw = 'powershell "Get-NetAdapterStatistics | Select-Object Name, ReceivedBytes, SentBytes | ConvertTo-Csv -NoTypeInformation -Delimiter \',\'"'
        res_bw = subprocess.run(cmd_bw, capture_output=True, text=True, shell=True, encoding='cp852', errors='ignore').stdout.strip()
        
        for line in res_bw.split('\n')[1:]:
            line = line.strip()
            if line:
                parts = line.replace('"', '').split(',')
                if len(parts) >= 3:
                    name = parts[0].strip()
                    if name not in data: data[name] = {}
                    try:
                        data[name]['rx'] = int(parts[1].strip())
                        data[name]['tx'] = int(parts[2].strip())
                    except:
                        data[name]['rx'] = 0
                        data[name]['tx'] = 0
    except:
        pass
    
    return data

def format_speed(bytes_per_sec):
    """Odpowiednio formatuje bajty na sekundę do B/s, KB/s lub MB/s."""
    if bytes_per_sec >= 1024 * 1024:
        return f"{bytes_per_sec / 1024 / 1024:>6.1f} MB/s"
    elif bytes_per_sec >= 1024:
        return f"{bytes_per_sec / 1024:>6.1f} KB/s"
    else:
        return f"{bytes_per_sec:>6.0f} B/s "

def run():
    os.system('cls')
    print(f"{C}================================================================{RESET}")
    print(f"             {Y}KONFIGURACJA EKRANU DOWODZENIA{RESET}")
    print(f"{C}================================================================{RESET}")
    
    adapters = core_config.get_adapters_info()
    iface_names = list(adapters.keys())
    
    if not iface_names:
        print(f" {R}[!] Nie wykryto kart sieciowych w systemie.{RESET}")
        time.sleep(2)
        return

    print(f" {Y}Wybierz karty do monitorowania:{RESET}\n")
    for i, name in enumerate(iface_names, 1):
        st = f"{G}UP{RESET}" if adapters[name]['status'] == "UP" else f"{R}DOWN{RESET}"
        print(f" [{G}{i}{RESET}] {name:<25} ({st})")
        
    print(f"\n [{G}0{RESET}] Wszystkie aktywne karty (Auto-detekcja)")
    
    choices = input("\n Wybór (np. 1 lub 1,3 lub 0): ").strip()
    selected_adapters = []
    
    if choices == '0' or not choices:
        selected_adapters = iface_names 
    else:
        for c in choices.split(','):
            try:
                idx = int(c.strip()) - 1
                if 0 <= idx < len(iface_names):
                    selected_adapters.append(iface_names[idx])
            except:
                pass
                
    if not selected_adapters:
        selected_adapters = iface_names 
        
    os.system('cls')
    print(f"\n {C}Inicjalizacja Ekranu Dowodzenia...{RESET}")
    print(f" {Y}Zbieranie początkowych danych z interfejsów...{RESET}")
    
    hostname = socket.gethostname()
    
    # [!] Pobieramy pierwszy zrzut danych, żeby mieć do czego odnieść prędkość
    prev_data = get_adapters_data()
    last_time = time.time()
    time.sleep(1) # Czekamy chwilę na ukształtowanie się ruchu

    while True:
        try:
            current_time = time.time()
            delta_t = current_time - last_time
            
            p = get_live_ping()
            net_data = get_adapters_data()
            
            if p == -1:
                ping_str = f"{R}BRAK INTERNETU (Timeout){RESET}"
            elif p < 40:
                ping_str = f"{G}{p} ms (Znakomity){RESET}"
            elif p < 100:
                ping_str = f"{Y}{p} ms (Średni){RESET}"
            else:
                ping_str = f"{R}{p} ms (Wysoki){RESET}"

            os.system('cls')
            print(f"{C}================================================================{RESET}")
            print(f"             {Y}GLOBAL DASHBOARD (MONITOR CZASU RZECZYWISTEGO){RESET}")
            print(f"{C}================================================================{RESET}")
            
            print(f" NAZWA HOSTA: {C}{hostname}{RESET}")
            print(f" STATUS WWW:  {ping_str}")
            print(f"{C}----------------------------------------------------------------{RESET}")
            print(f" {Y}RUCH SIECIOWY I ADRESY IP (Wybrane interfejsy):{RESET}\n")
            
            has_data = False
            for name in selected_adapters:
                info = net_data.get(name, {})
                prev_info = prev_data.get(name, {})
                
                ip = info.get('ip', 'Brak IP (Rozłączono/APIPA)')
                rx_bytes = info.get('rx', 0)
                tx_bytes = info.get('tx', 0)
                
                prev_rx = prev_info.get('rx', rx_bytes)
                prev_tx = prev_info.get('tx', tx_bytes)
                
                if choices in ['0', ''] and rx_bytes == 0 and tx_bytes == 0 and 'Brak IP' in ip:
                    continue 
                    
                has_data = True
                
                # Obliczanie aktualnej prędkości
                rx_speed = max(0, (rx_bytes - prev_rx) / delta_t) if delta_t > 0 else 0
                tx_speed = max(0, (tx_bytes - prev_tx) / delta_t) if delta_t > 0 else 0
                
                # Obliczanie sumy całkowitej
                rx_total_mb = rx_bytes / 1024 / 1024
                tx_total_mb = tx_bytes / 1024 / 1024
                
                print(f"  > {C}{name[:22]:<22}{RESET} | IP: {Y}{ip:<15}{RESET}")
                print(f"    {'Prędkość (Live):':<22} | ↓ {format_speed(rx_speed):<10} | ↑ {format_speed(tx_speed)}")
                print(f"    {'Suma (Total):':<22} | ↓ {rx_total_mb:>6.1f} MB   | ↑ {tx_total_mb:>6.1f} MB\n")
                
            if not has_data:
                print(f"  {R}> Brak aktywnych danych do wyświetlenia (karty odłączone?).{RESET}")
                
            print(f"{C}----------------------------------------------------------------{RESET}")
            print(f" Odświeżanie automatyczne. Naciśnij {R}[Ctrl+C]{RESET} aby wyjść.")

            # Aktualizujemy "stare" dane do następnej pętli
            prev_data = net_data
            last_time = current_time

            time.sleep(1.5)

        except KeyboardInterrupt:
            print(f"\n {G}[i] Zamykanie dashboardu. Powrót do menu...{RESET}")
            time.sleep(1)
            break
        except Exception as e:
            print(f"\n {R}[!] Krytyczny Błąd Dashboardu: {e}{RESET}")
            time.sleep(2)
            break