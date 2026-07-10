#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time, requests, os, core_config

CACHE = {}

def get_vendor(mac):
    if not mac or mac == "00:00:00:00:00:00": return "Bramka Systemowa"
    mac = mac.upper().replace("-", ":")
    if mac in CACHE: return CACHE[mac]

    if len(mac) > 1 and mac[1] in "26AE":
        res = "MAC Prywatny/Losowy (Mobile)"
        CACHE[mac] = res
        return res

    url = f"https://api.macvendors.com/{mac}"
    for _ in range(2): 
        try:
            time.sleep(0.6)
            response = requests.get(url, timeout=3)
            if response.status_code == 200:
                vendor = response.text.strip()
                CACHE[mac] = vendor
                return vendor
            elif response.status_code == 429: time.sleep(1)
        except: pass
    return "Nieznany / Brak w bazie"

def run():
    while True:
        core_config.clear_screen()
        print("=== SPRAWDZANIE PRODUCENTA PO MAC ===")
        print(" [0] Powrót")
        
        mac = input("\n Adres MAC: ").strip()
        if mac == '0': break
        if len(mac) < 8: continue
            
        print(f"\n [i] Szukam: {mac}...")
        try:
            vendor = get_vendor(mac)
            print("-" * 40)
            print(f" WYNIK: \033[92m{vendor}\033[0m")
            print("-" * 40)
        except: pass
        input("\n Enter...")