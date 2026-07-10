#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, time, core_config

def get_bytes(iface):
    try:
        # Linux trzyma liczniki bajtów w plikach tekstowych w /sys
        with open(f"/sys/class/net/{iface}/statistics/rx_bytes") as f: rx = int(f.read())
        with open(f"/sys/class/net/{iface}/statistics/tx_bytes") as f: tx = int(f.read())
        return rx, tx
    except: return 0, 0

def run():
    last = {}
    adapters = core_config.get_adapters_info()
    
    # Inicjalizacja
    for i in adapters: last[i] = get_bytes(i)
    
    while True:
        try:
            core_config.clear_screen()
            print(f" {'INTERFEJS':<15} | {'DL (KB/s)':<10} | {'UL (KB/s)':<10}")
            print("-" * 40)
            
            curr = {}
            # Ponowne pobranie listy, w razie gdyby interfejs zniknął/pojawił się
            current_adapters = core_config.get_adapters_info()
            
            for i in current_adapters:
                rx, tx = get_bytes(i)
                lrx, ltx = last.get(i, (rx, tx)) # Jeśli nowy, delta=0
                
                dl = (rx - lrx) / 1024
                ul = (tx - ltx) / 1024
                
                print(f" {i:<15} | {dl:<10.1f} | {ul:<10.1f}")
                curr[i] = (rx, tx)
            
            last = curr
            time.sleep(1)
        except KeyboardInterrupt: break