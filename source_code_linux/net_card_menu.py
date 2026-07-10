#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, subprocess, time, db_ip, core_config
import ipaddress

G, R, C, Y, RESET = '\033[92m', '\033[91m', '\033[96m', '\033[93m', '\033[0m'

def get_connection_profile(iface):
    """
    Znajduje nazwę profilu (np. 'Wired connection 1') przypisaną do interfejsu.
    Szuka we WSZYSTKICH połączeniach, nie tylko aktywnych.
    """
    try:
        # Usunięto flagę --active, aby widzieć profile wyłączonych kart
        out = subprocess.check_output("nmcli -t -f NAME,DEVICE con show", shell=True).decode()
        for line in out.splitlines():
            parts = line.split(":")
            if len(parts) > 1 and parts[1] == iface:
                return parts[0]
    except: pass
    return None # Zwracamy None jeśli nie znaleziono profilu

def get_adapter_status(iface):
    try:
        with open(f"/sys/class/net/{iface}/operstate") as f:
            state = f.read().strip()
        with open(f"/sys/class/net/{iface}/address") as f:
            mac = f.read().strip()
        st_color = G if state == "up" else R
        return f"{st_color}{state.upper()}{RESET}", mac
    except: return f"{R}DOWN{RESET}", "00:00:00:00:00:00"

def get_current_config(iface):
    cfg = {"ip": "-", "mask": "-", "gw": "-", "dns1": "-", "dns2": "-"}
    try:
        # 1. IP i Maska
        out = subprocess.check_output(f"ip -4 addr show dev {iface}", shell=True).decode()
        for line in out.splitlines():
            if "inet " in line:
                parts = line.strip().split()
                ip_cidr = parts[1]
                if "/" in ip_cidr:
                    ip_obj = ipaddress.IPv4Interface(ip_cidr)
                    cfg['ip'] = str(ip_obj.ip)
                    cfg['mask'] = str(ip_obj.netmask)
                else:
                    cfg['ip'] = ip_cidr
                break
        
        # 2. Brama (szukamy w ip route dla tego deva)
        out_gw = subprocess.check_output("ip route", shell=True).decode()
        for line in out_gw.splitlines():
            if "default" in line and iface in line:
                cfg['gw'] = line.split()[2]
                break

        # 3. DNS
        out_dns = subprocess.check_output(f"nmcli dev show {iface} | grep DNS", shell=True).decode()
        dns_list = []
        for line in out_dns.splitlines():
            if ":" in line:
                dns_list.append(line.split(":")[1].strip())
        if len(dns_list) > 0: cfg['dns1'] = dns_list[0]
        if len(dns_list) > 1: cfg['dns2'] = dns_list[1]
    except: pass
    return cfg

def mask_to_cidr(mask):
    try: return ipaddress.IPv4Network(f"0.0.0.0/{mask}").prefixlen
    except: return 24

def apply_config(iface, ip, mask, gw, d1, d2):
    # Do edycji musimy znać nazwę profilu. Jeśli nie ma, tworzymy nowy.
    con = get_connection_profile(iface)
    if not con:
        print(f" {Y}[INFO]{RESET} Brak profilu dla {iface}. Tworzę nowy...")
        con = f"Wired connection {iface}"
        subprocess.run(f"sudo nmcli con add type ethernet con-name '{con}' ifname {iface}", shell=True)
        time.sleep(1)

    cidr = mask_to_cidr(mask)
    print(f" [i] Konfiguracja profilu '{con}'...")
    
    gw_cmd = f"ipv4.gateway {gw}" if gw and gw not in ["-", "", "None", "0.0.0.0"] else "ipv4.gateway ''"
    
    dns_list = []
    if d1 and d1 not in ["-", ""]: dns_list.append(d1)
    if d2 and d2 not in ["-", ""]: dns_list.append(d2)
    dns_cmd = f"ipv4.dns '{' '.join(dns_list)}'" if dns_list else "ipv4.dns ''"

    cmd = f"sudo nmcli con mod '{con}' ipv4.addresses {ip}/{cidr} {gw_cmd} {dns_cmd} ipv4.method manual"
    
    if subprocess.call(cmd, shell=True) == 0:
        print(" [i] Restartowanie interfejsu...")
        # Używamy metody brute-force: down -> up
        subprocess.run(f"sudo nmcli con down '{con}'", shell=True, stderr=subprocess.DEVNULL)
        subprocess.run(f"sudo nmcli con up '{con}'", shell=True)
        print(f" {G}[SUKCES]{RESET} Ustawiono IP: {ip}/{cidr}")
    else:
        print(f" {R}[BŁĄD]{RESET} Nie udało się zapisać zmian.")
    time.sleep(2)

def set_dhcp(iface):
    con = get_connection_profile(iface)
    if not con: 
        print(f" {R}[BŁĄD]{RESET} Nie znaleziono profilu połączenia.")
        return

    print(f" [i] Ustawianie DHCP dla '{con}'...")
    cmd = f"sudo nmcli con mod '{con}' ipv4.method auto ipv4.addresses '' ipv4.gateway '' ipv4.dns ''"
    if subprocess.call(cmd, shell=True) == 0:
        subprocess.run(f"sudo nmcli con down '{con}'", shell=True, stderr=subprocess.DEVNULL)
        subprocess.run(f"sudo nmcli con up '{con}'", shell=True)
        print(f" {G}[SUKCES]{RESET} DHCP Aktywne.")
    time.sleep(2)

def toggle_iface(iface, state):
    """
    Inteligentne włączanie/wyłączanie karty.
    Działa nawet na VirtualBoxie i USB bez znanej nazwy profilu.
    """
    print(f" [i] Zmieniam stan {iface} na: {state.upper()}...")
    
    if state == "down":
        # 1. Rozłącz logicznie
        subprocess.run(f"sudo nmcli dev disconnect {iface}", shell=True, stderr=subprocess.DEVNULL)
        # 2. Wyłącz fizycznie (sterownik)
        subprocess.run(f"sudo ip link set {iface} down", shell=True)
    else:
        # 1. Włącz fizycznie
        subprocess.run(f"sudo ip link set {iface} up", shell=True)
        time.sleep(0.5)
        # 2. Połącz logicznie (Auto-connect - sam znajdzie najlepszy profil)
        subprocess.run(f"sudo nmcli dev connect {iface}", shell=True)
    
    time.sleep(1.5)

def run(iface):
    while True:
        core_config.clear_screen()
        status, mac = get_adapter_status(iface)
        cfg = get_current_config(iface)
        
        print(f"{C}================================================================{RESET}")
        print(f"        KARTA: {Y}{iface}{RESET}  |  MAC: {mac}")
        print(f"        STATUS: {status:<19}")
        print(f"        IP: {cfg['ip']:<15} MASKA: {cfg['mask']}")
        print(f"        GW: {cfg['gw']:<15} DNS: {cfg['dns1']}, {cfg['dns2']}")
        print(f"{C}================================================================{RESET}")
        
        print(f" [{G}1{RESET}] DHCP (Auto)")
        print(f" [{G}2{RESET}] Ustaw ręcznie IP")
        print(f" [{G}3{RESET}] Baza Profili")
        print(f" [{G}4{RESET}] Restart (Down/Up)")
        print(f" [{G}ON{RESET}] Włącz kartę        [{R}OFF{RESET}] Wyłącz kartę")
        print(f" [{G}5{RESET}] Snapshot do bazy")
        print(f"\n [{R}0{RESET}] Powrót")
        
        c = input("\n Wybór: ").strip().lower()
        
        if c == '0': break
        elif c == '1': set_dhcp(iface)
        elif c == '2':
            d = db_ip.manual_input_profile()
            if d: apply_config(iface, d[1], d[2], d[3], d[4], d[5])
        elif c == '3':
            p = db_ip.select_profile_menu(mode="SELECT")
            if p: apply_config(iface, p[1], p[2], p[3], p[4], p[5])
        elif c == '4':
            toggle_iface(iface, "down")
            toggle_iface(iface, "up")
        elif c == 'on': toggle_iface(iface, "up")
        elif c == 'off': toggle_iface(iface, "down")
        elif c == '5':
            name = input(" Nazwa profilu: ")
            if name:
                snap_gw = cfg['gw'] if cfg['gw'] else "-"
                snap_d1 = cfg['dns1'] if cfg['dns1'] else "8.8.8.8"
                snap_d2 = cfg['dns2'] if cfg['dns2'] else "-"
                db_ip.save_all(db_ip.load_all_profiles() + [[name, cfg['ip'], cfg['mask'], snap_gw, snap_d1, snap_d2]])
                print(f" {G}Zapisano.{RESET}")
                time.sleep(1)
