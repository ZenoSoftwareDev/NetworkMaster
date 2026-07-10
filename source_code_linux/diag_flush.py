#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess, time, core_config

def run():
    core_config.clear_screen()
    print(" [!] Czyszczenie cache DNS (systemd-resolved)...")
    # Metoda uniwersalna dla nowoczesnych Linuxów
    cmds = [
        "resolvectl flush-caches",
        "systemd-resolve --flush-caches",
        "service nscd restart" # Fallback dla starszych
    ]
    
    done = False
    for c in cmds:
        try:
            if subprocess.call(c, shell=True, stderr=subprocess.DEVNULL) == 0:
                print(f" [OK] Wykonano: {c.split()[0]}")
                done = True
                break
        except: pass
    
    if not done: print(" [i] Nie znaleziono lokalnego cache DNS (to normalne na Linuxie).")
    time.sleep(1.5)