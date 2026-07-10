import os, sys, subprocess, time, threading
import core_config

# Importy modułów diagnostycznych
try:
    import diag_ping, diag_tracert, diag_dns, diag_wifi, diag_geo_ip, diag_system, diag_flush, diag_hosts
    import db_ip, db_wol, net_card_menu
    import diag_net_scan, diag_port_scan, diag_whois, diag_bandwidth, core_mac_lookup, diag_subnet, diag_repair
    import diag_wifi_monitor, diag_dns_bench, diag_dashboard, diag_ssl
except ImportError:
    pass 

G, R, C, Y, RESET = '\033[92m', '\033[91m', '\033[96m', '\033[93m', '\033[0m'

# ================================================================
# PIERWSZE URUCHOMIENIE
# ================================================================

def check_first_run():
    flag_file = core_config.FIRST_RUN_FLAG
    
    # Jeśli plik istnieje, omijamy ekran startowy
    if os.path.exists(flag_file):
        return

    os.system('cls')
    print(f"\n {C}================================================================{RESET}")
    print(f"                 {Y}WITAJ W PROGRAMIE NETWORK MASTER{RESET}")
    print(f" {C}================================================================{RESET}")
    
    confirm = input(f"\n Czy napewno chcesz uruchomić program NetworkMaster? (wpisz {G}'TAK'{RESET}): ").strip().upper()
    
    if confirm == 'TAK':
        core_config.init() # <--- Ta funkcja utworzy folder core_data dopiero teraz
        
        # Tworzymy pusty plik flagi po upewnieniu się, że foldery istnieją
        with open(flag_file, "w") as f:
            f.write("OK")
            
        print(f"\n {G}Inicjalizacja zakończona.{RESET}"); time.sleep(1.5)
    else:
        print(f"\n {R}Program zostanie zamknięty.{RESET}")
        time.sleep(3); sys.exit()

# ================================================================
# GŁÓWNA FUNKCJA PROGRAMU
# ================================================================

def main():
    check_first_run()
    core_config.init()
    
    os.system('cls')
    print(f"{C}========================================{RESET}")
    print(f"             NETWORK MASTER")
    print(f"{C}========================================{RESET}")
    print(" Ładowanie modułów...")
    time.sleep(0.5)

    while True:
        try:
            os.system('cls')
            print(f"{C}================================================================{RESET}")
            print(f"                        {Y}NETWORK MASTER{RESET}")
            print(f"{C}================================================================{RESET}")
            
            adapters = core_config.get_adapters_info()
            iface_names = list(adapters.keys())
            
            print(f" {Y}{'ID':<3} | {'INTERFEJS':<25} | {'STATUS':<9} | {'PRĘDKOŚĆ'}{RESET}")
            print(f"{C}----------------------------------------------------------------{RESET}")
            
            for i, name in enumerate(iface_names, 1):
                info = adapters[name]
                st = f"{G}UP{RESET}" if info['status'] == "UP" else f"{R}DOWN{RESET}"
                print(f" [{G}{i:02}{RESET}] | {name[:25]:<25} | {st:<18} | {info['speed']}")
            
            print(f"{C}----------------------------------------------------------------{RESET}")
            print(f"\n {C}--- NARZĘDZIA DIAGNOSTYCZNE ---{RESET}")
            print(f" [{G}A{RESET}] ARP Tabela - adresy fizyczne")
            print(f" [{G}B{RESET}] Bandwidth - monitor obciązenia")
            print(f" [{G}C{RESET}] Calculator - kalkulator podsieci")
            print(f" [{G}D{RESET}] DNS Lookup - sprawdzanie domen")
            print(f" [{G}E{RESET}] Ekran Dowodzenia (Global Dashboard)")
            print(f" [{G}F{RESET}] Flush DNS - czyszczenie pamieci")
            print(f" [{G}G{RESET}] GeoIP Twoja lokalizacja")
            print(f" [{G}H{RESET}] HOSTS - edytor pliku systemowego")
            print(f" [{G}I{RESET}] IPConfig - pełna konfiguracja")
            print(f" [{G}M{RESET}] MAC Lookup - producent karty")
            print(f" [{G}N{RESET}] Netstat - aktywne porty")
            print(f" [{G}O{RESET}] Monitor WiFi - siła sygnału (Live)")
            print(f" [{G}P{RESET}] Port Skaner - usługi na hostach")
            print(f" [{G}Q{RESET}] DNS Benchmark - test szybkosci serwerow") 
            print(f" [{G}R{RESET}] Traceroute - śledzenie trasy")
            print(f" [{G}S{RESET}] Skaner Sieci - urządzenia IP")
            print(f" [{G}T{RESET}] Testy PING - opóźnienia")
            print(f" [{G}W{RESET}] WiFi Vault - hasła wifi")
            print(f" [{G}X{RESET}] WHOIS - informacje o domenie")
            print(f" [{G}Y{RESET}] SSL Audit - weryfikacja certyfikatów") 
            print(f" [{G}Z{RESET}] Zerowanie Sieci - naprawa/reset")
            
            print(f"\n {C}--- ZARZĄDZANIE ---{RESET}")
            print(f" [{G}J{RESET}] Baza Profili IP")
            print(f" [{G}K{RESET}] Baza WOL (budzenie komputerów)")
            print(f" [{G}L{RESET}] Menedżer Urządzeń")
            print(f" [{G}U{RESET}] Edytor Połączeń")
            
            print(f"\n [{R}0{RESET}] ZAMKNIJ")

            c = input("\n Wybór: ").lower().strip()
            if c == '0': sys.exit()
            
            if c.isdigit():
                idx = int(c) - 1
                if 0 <= idx < len(iface_names): net_card_menu.run(iface_names[idx])
                continue

            acts = {
                'a': diag_system.run_arp, 'b': diag_bandwidth.run, 'c': diag_subnet.run,
                'd': diag_dns.run, 'e': diag_dashboard.run, 'f': diag_flush.run, 'g': diag_geo_ip.run,
                'h': diag_hosts.run, 'i': diag_system.run_ipconfig, 'm': core_mac_lookup.run,
                'n': diag_system.run_netstat, 'o': diag_wifi_monitor.run, 'p': diag_port_scan.run,
                'q': diag_dns_bench.run, 'r': diag_tracert.run, 's': diag_net_scan.run, 
                't': diag_ping.run_menu, 'w': diag_wifi.run, 'x': diag_whois.run, 
                'y': diag_ssl.run, 'z': diag_repair.run,
                'j': db_ip.run_management, 'k': db_wol.run,
                'l': lambda: subprocess.run("start devmgmt.msc", shell=True),
                'u': lambda: subprocess.run("start control ncpa.cpl", shell=True)
            }
            if c in acts: acts[c]()

        except KeyboardInterrupt: sys.exit()
        except Exception as e: print(f"Błąd: {e}"); input("Enter...")

if __name__ == "__main__":
    main()