#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, subprocess, core_config

def run_menu():
    while True:
        core_config.clear_screen()
        print("=== MENU PING (LINUX) ===\n [1] Google (x4)\n [2] Google (Ciągły)\n [3] Własny (x4)\n [4] Własny (Ciągły)")
        print(" [0] Powrót")
        
        c = input("\n Wybór: ")
        if c == '0': break
        
        try:
            if c == '1': subprocess.run("ping -c 4 8.8.8.8", shell=True)
            elif c == '2': subprocess.run("ping 8.8.8.8", shell=True) # Linux domyślnie ciągły
            elif c == '3': 
                adr = input(" Adres: ")
                subprocess.run(f"ping -c 4 {adr}", shell=True)
            elif c == '4': 
                adr = input(" Adres: ")
                subprocess.run(f"ping {adr}", shell=True)
            
            input("\n[KONIEC] Enter...")
        except KeyboardInterrupt: pass