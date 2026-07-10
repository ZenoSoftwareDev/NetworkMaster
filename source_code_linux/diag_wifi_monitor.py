#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, time, sys
import core_config

G, R, C, Y, RESET = '\033[92m', '\033[91m', '\033[96m', '\033[93m', '\033[0m'

def get_realtime_wifi():
    """
    Czyta dane bezpośrednio z jądra Linux (/proc/net/wireless).
    Omija cache NetworkManagera.
    """
    results = []
    try:
        with open("/proc/net/wireless", "r") as f:
            lines = f.readlines()
            # Format pliku:
            # Inter-| sta-|   Quality        |   Discarded packets               | Missed | WE
            #  face | tus | link level noise |  nwid  crypt   frag  retry   misc | beacon | 22
            # wlan0: 0000   55.  -55.  -256        0      0      0      0      0        0
            
            for line in lines[2:]:
                parts = line.split()
                if len(parts) > 4:
                    iface = parts[0].replace(":", "")
                    
                    # Kolumna 'link' (Quality) to zazwyczaj jakość 0-70 lub 0-100
                    # Kolumna 'level' (Signal) to dBm (np. -55)
                    
                    raw_link = parts[2].replace(".", "")
                    raw_level = parts[3].replace(".", "")
                    
                    try:
                        link_val = int(raw_link)
                        level_val = int(raw_level)
                    except: continue
                    
                    results.append({
                        "iface": iface,
                        "link": link_val, # Zazwyczaj max 70
                        "level": level_val # dBm
                    })
    except FileNotFoundError:
        pass
    return results

def run():
    try:
        while True:
            core_config.clear_screen()
            print(f"{C}================================================================{RESET}")
            print(f"            {Y}MONITOR SYGNAŁU WIFI (KERNEL REALTIME){RESET}")
            print(f"{C}================================================================{RESET}")
            
            stats = get_realtime_wifi()
            
            if not stats:
                print(f"\n {R}[!] Brak danych o WiFi.{RESET}")
                print(" 1. Jeśli jesteś w VirtualBox: WiFi jest widoczne jako kabel (eth0).")
                print("    Nie ma 'sygnału', jest zawsze 100%.")
                print(" 2. Brak sterowników lub karta wyłączona.")
            else:
                print(f" {'INTERFEJS':<12} | {'JAKOŚĆ':<20} | {'DBM':<6} | {'OCENA'}")
                print("-" * 64)
                
                for s in stats:
                    # Konwersja Link Quality na Procenty (Standardowo max to 70 w Linuxie)
                    max_qual = 70.0
                    percent = int((s['link'] / max_qual) * 100)
                    if percent > 100: percent = 100
                    
                    # Pasek graficzny
                    bar_len = int(percent / 5)
                    bar_str = "█" * bar_len + "░" * (20 - bar_len)
                    
                    # Kolorowanie
                    col = G
                    rating = "DOSKONAŁY"
                    if s['level'] < -60: 
                        col = Y; rating = "DOBRY"
                    if s['level'] < -75: 
                        col = R; rating = "SŁABY"
                        
                    print(f" {s['iface']:<12} | {col}[{bar_str}]{RESET} | {s['level']} | {col}{rating}{RESET}")
                    
            print(f"\n {C}[i]{RESET} Odświeżanie co 1s... (Ctrl+C aby wyjść)")
            time.sleep(1)
            
    except KeyboardInterrupt: pass
