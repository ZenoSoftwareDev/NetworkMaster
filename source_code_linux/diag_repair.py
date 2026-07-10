#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, subprocess, time, core_config

G, R, C, Y, RESET = '\033[92m', '\033[91m', '\033[96m', '\033[93m', '\033[0m'

def run():
    core_config.clear_screen()
    print(f"{R}================================================================{RESET}")
    print(f"           {Y}NAPRAWA SIECI LINUX (NETWORK RESET){RESET}")
    print(f"{R}================================================================{RESET}")
    print(" [!] Wymagane uprawnienia ROOT (sudo).")
    print(" Kroki:")
    print(" 1. Restart usługi NetworkManager")
    print(" 2. Odświeżenie dzierżawy DHCP (dhclient)")
    print(" 3. Czyszczenie cache DNS (resolvectl)")
    
    if input("\n Kontynuować? (t/n): ").lower() != 't': return

    steps = [
        ("Restartowanie NetworkManager...", "sudo systemctl restart NetworkManager"),
        ("Zwalnianie DHCP...", "sudo dhclient -r"),
        ("Pobieranie nowego IP (DHCP)...", "sudo dhclient"),
        ("Flush DNS (resolvectl)...", "resolvectl flush-caches"),
    ]

    print("")
    for desc, cmd in steps:
        print(f" [*] {desc:<40}", end="", flush=True)
        try:
            ret = subprocess.call(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if ret == 0: print(f" {G}[OK]{RESET}")
            else: print(f" {R}[SKIP]{RESET}") # Skip jest ok, np. jak nie ma dhclienta
            time.sleep(1)
        except: print(f" {R}[BŁĄD]{RESET}")

    print(f"\n {G}[GOTOWE] Sprawdź połączenie.{RESET}")
    input("\n Enter...")