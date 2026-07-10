#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, subprocess, core_report, core_config

def run_ipconfig():
    core_config.clear_screen()
    print(" [!] Pobieranie pełnej konfiguracji sieciowej (ip addr, route, dns)...")
    
    # Łączymy kilka komend dla pełnego obrazu
    cmd = "echo '--- ADRESY IP ---'; ip addr show; echo '\n--- TRASY (ROUTING) ---'; ip route show; echo '\n--- DNS (RESOLV.CONF) ---'; cat /etc/resolv.conf"
    res = subprocess.run(cmd, capture_output=True, text=True, shell=True).stdout
    
    print(res)
    core_report.save(res, "IPConfig_All_Linux")
    input("\n Enter...")

def run_netstat():
    while True:
        core_config.clear_screen()
        print("=== MONITOR POŁĄCZEŃ (SS/Netstat) ===\n")
        print(" [1] Tylko AKTYWNE połączenia (ESTABLISHED)")
        print(" [2] Wszystkie porty nasłuchujące (LISTENING)")
        print(" [0] Powrót")
        
        c = input("\n Wybór: ")
        if c == '0': break
        
        core_config.clear_screen()
        if c == '1':
            print(" [i] Aktywne sesje TCP (ss -tun state established)...\n")
            # ss jest szybsze i dokładniejsze na Linuxie
            cmd = 'ss -tun state established'
        else:
            print(" [i] Porty nasłuchujące (ss -tuln)...\n")
            cmd = 'ss -tuln'

        res = subprocess.run(cmd, capture_output=True, text=True, shell=True).stdout
        
        print("-" * 80)
        print(res)
        print("-" * 80)
        
        if input("\n [?] Zapisać raport? (t/n): ").lower() == 't':
            core_report.save(res, "Netstat_Linux")
        
        input("\n Enter...")

def run_arp():
    core_config.clear_screen()
    print(" [!] Pobieranie tablicy sąsiadów (ARP / ip neigh)...")
    # ip neigh to nowoczesny odpowiednik arp -a
    res = subprocess.run("ip neigh", capture_output=True, text=True, shell=True).stdout
    print(res)
    core_report.save(res, "ARP_Table_Linux")
    input("\n Enter...")