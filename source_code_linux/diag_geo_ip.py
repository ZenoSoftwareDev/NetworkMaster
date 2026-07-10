#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, requests, core_report, core_config

def run():
    core_config.clear_screen()
    print("=== LOKALIZACJA GEOGRAFICZNA IP ===\n")
    print(" [i] Pobieranie danych...")
    
    try:
        response = requests.get("http://ip-api.com/json/", timeout=5).json()
        if response['status'] == 'success':
            data = f"""
 ADRES IP:    {response['query']}
 KRAJ:        {response['country']} ({response['countryCode']})
 MIASTO:      {response['city']}
 REGION:      {response['regionName']}
 DOSTAWCA:    {response['isp']}
"""
            print(data)
            print("-" * 40)
            if input(" [?] Zapisać raport? (t/n): ").lower() == 't':
                core_report.save(data, "Raport_GeoIP")
        else:
            print(" [!] Błąd API.")
    except Exception as e:
        print(f" [!] Błąd połączenia: {e}")
        
    input("\n Enter...")