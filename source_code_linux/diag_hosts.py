#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, subprocess, core_config

PATH = "/etc/hosts"

def run():
    while True:
        core_config.clear_screen()
        print("=== EDYTOR /ETC/HOSTS ===")
        print(" [1] Wyświetl")
        print(" [2] Dodaj wpis (sudo)")
        print(" [3] Edytuj w nano (sudo)")
        print(" [0] Powrót")
        
        c = input("\n Wybór: ")
        if c == '0': break
        elif c == '1':
            os.system(f"cat {PATH}")
            input("\n Enter...")
        elif c == '2':
            ip = input(" IP: ")
            dom = input(" Domena: ")
            cmd = f"echo '{ip} {dom}' | sudo tee -a {PATH}"
            os.system(cmd)
            print(" [OK] Dodano.")
            time.sleep(1)
        elif c == '3':
            os.system(f"sudo nano {PATH}")