#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, core_config, core_report, glob

def run():
    core_config.clear_screen()
    print("="*60)
    print("      WIFI SECURITY AUDITOR (LINUX ROOT)")
    print("="*60)
    
    if os.geteuid() != 0:
        print(" [!] WYMAGANE UPRAWNIENIA ROOT (sudo).")
        print(" Hasła WiFi na Linuxie są chronione przez system.")
        input("\n Enter..."); return

    # Lista ścieżek do sprawdzenia. 
    # /run/... jest używane przez Live ISO i tymczasowe sesje
    paths_to_check = [
        "/etc/NetworkManager/system-connections/",
        "/run/NetworkManager/system-connections/"
    ]
    
    found_any_path = False
    for p in paths_to_check:
        if os.path.exists(p): found_any_path = True
            
    if not found_any_path:
        print(f" [!] Nie znaleziono katalogów NetworkManager.")
        print(" System może używać wpa_supplicant lub innego managera.")
        input(" Enter..."); return

    data = []
    
    # Przeszukiwanie wszystkich ścieżek
    for path in paths_to_check:
        if not os.path.exists(path): continue
        
        try:
            # Używamy glob, żeby złapać wszystkie pliki
            files = glob.glob(os.path.join(path, "*"))
            for full_path in files:
                try:
                    with open(full_path, 'r') as file:
                        content = file.read()
                        
                        ssid = None
                        psk = None
                        key_mgmt = "Open"
                        current_section = ""
                        
                        # Parser INI-like
                        for line in content.splitlines():
                            line = line.strip()
                            if line.startswith("[") and line.endswith("]"):
                                current_section = line
                            
                            if current_section == "[wifi]":
                                if line.startswith("ssid="): 
                                    ssid = line.split("=")[1].strip()
                                    
                            if current_section == "[wifi-security]":
                                if line.startswith("psk="): 
                                    psk = line.split("=")[1].strip()
                                if line.startswith("key-mgmt="):
                                    key_mgmt = line.split("=")[1].strip()
                        
                        # Dodajemy tylko unikalne (bo Live USB może dublować pliki)
                        if ssid:
                            entry = (ssid, key_mgmt, psk if psk else "[BRAK/SYSTEM]")
                            if entry not in data:
                                data.append(entry)
                except: pass
        except: pass

    if not data:
        print("\n [!] Nie znaleziono zapisanych profili.")
        print(" Jeśli jesteś na Live USB, połącz się z siecią i spróbuj ponownie.")
    else:
        print(f" {'SSID':<30} | {'TYP':<15} | {'HASŁO'}")
        print("-" * 65)
        
        res_txt = ""
        for ssid, typ, pwd in data:
            line = f" {ssid:<30} | {typ:<15} | {pwd}"
            print(line)
            res_txt += line + "\n"
            
        if input("\n Zapisać raport? (t/n): ").lower() == 't':
            core_report.save(res_txt, "WiFi_Passwords_Linux")
        
    input("\n Enter...")
