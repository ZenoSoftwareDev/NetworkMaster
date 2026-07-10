#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, time, core_config

G, R, C, Y, RESET = '\033[92m', '\033[91m', '\033[96m', '\033[93m', '\033[0m'
DB_PATH = core_config.DB_IP

def load_all_profiles():
    if not os.path.exists(DB_PATH): return []
    valid_profiles = []
    try:
        with open(DB_PATH, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line: continue
                parts = [p.strip() for p in line.split(";") if p.strip() or line.count(";") >= 5]
                if len(parts) > 0 and "." in parts[0] and parts[0].count(".") == 3: parts = ["-"] + parts
                while len(parts) < 6: parts.append("-")
                valid_profiles.append(parts[:6])
    except: pass
    return valid_profiles

def save_all(profiles):
    try:
        with open(DB_PATH, "w", encoding="utf-8") as f:
            for p in profiles: f.write(";".join(p[:6]) + ";\n")
    except Exception as e: print(f" Błąd: {e}"); time.sleep(1)

def select_profile_menu(mode="SELECT"):
    while True:
        profiles = load_all_profiles()
        core_config.clear_screen()
        fname = os.path.basename(DB_PATH)
        print(f"{C}=== BAZA PROFILI IP ({fname}) ==={RESET}")
        
        header = f" {'ID':<3} | {'NAZWA':<12} | {'IP':<15} | {'MASKA':<15} | {'BRAMA':<15} | {'DNS 1':<15}"
        print(header); print("-" * len(header))
        
        if not profiles: print(f" {R}[BRAK DANYCH] - Dodaj nowy [A]{RESET}")
        
        for i, p in enumerate(profiles, 1):
            n = (p[0][:10]+"..") if len(p[0])>12 else p[0]
            print(f" {i:<3} | {n:<12} | {p[1]:<15} | {p[2]:<15} | {p[3]:<15} | {p[4]:<15}")

        print("-" * len(header))
        
        if mode == "SELECT":
            print(f" {G}[ID]{RESET} Wybierz   {G}[A]{RESET} Dodaj   {G}[E]{RESET} Edytuj   {G}[D]{RESET} Usuń   {R}[0]{RESET} Powrót")
        else:
            print(f" {G}[A]{RESET} Dodaj   {G}[E]{RESET} Edytuj   {G}[D]{RESET} Usuń   {R}[0]{RESET} Powrót")
        
        c = input("\n Wybór: ").lower().strip()
        if c == '0': return None
        
        if c == 'a':
            new_p = manual_input_profile()
            if new_p: profiles.append(new_p); save_all(profiles)
            continue
        elif c == 'd':
            try:
                idx = int(input(" Numer ID do usunięcia: "))-1
                if 0 <= idx < len(profiles): del profiles[idx]; save_all(profiles)
            except: pass
            continue
        elif c == 'e':
            try:
                idx = int(input(" Numer ID do edycji: "))-1
                if 0 <= idx < len(profiles):
                    edited = manual_input_profile(profiles[idx])
                    if edited: profiles[idx] = edited; save_all(profiles)
            except: pass
            continue
            
        if mode == "SELECT":
            try:
                idx = int(c)-1
                if 0 <= idx < len(profiles): return profiles[idx]
            except: pass

def run_management():
    select_profile_menu(mode="MANAGE")

def manual_input_profile(old_data=None):
    current = old_data if old_data else ["-", "", "255.255.255.0", "-", "8.8.8.8", "8.8.4.4"]
    print(f"\n{Y}--- KREATOR PROFILU ---{RESET}")
    print(" (Enter = zachowaj)\n")
    
    name = input(f" Nazwa profilu [{current[0]}]: ").strip() or current[0]
    ip = input(f" Adres IP [{current[1]}]: ").strip() or current[1]
    if not ip or ip == "-": return None
        
    print(f" Maska (obecna: {current[2]}):")
    print(" [1] 255.255.255.0 (/24)  [2] 255.255.0.0 (/16)  [3] 255.0.0.0 (/8)  [4] WŁASNA")
    m_c = input(" Wybór: ").strip()
    if m_c == '1': mask = "255.255.255.0"
    elif m_c == '2': mask = "255.255.0.0"
    elif m_c == '3': mask = "255.0.0.0"
    elif m_c == '4': mask = input(f" Podaj własną maskę: ").strip() or current[2]
    else: mask = current[2]

    gate = input(f" Brama domyślna [{current[3]}]: ").strip() or current[3]
    dns1 = input(f" DNS 1 [{current[4]}]: ").strip() or current[4]
    dns2 = input(f" DNS 2 [{current[5]}]: ").strip() or current[5]
    
    return [name, ip, mask, gate, dns1, dns2]