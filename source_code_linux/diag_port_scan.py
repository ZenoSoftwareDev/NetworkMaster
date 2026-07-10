#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, socket, core_report, core_config

def run():
    while True:
        try:
            core_config.clear_screen()
            print("=== SKANER PORTÓW SIECIOWYCH ===")
            
            raw_input = input("\n Podaj IP (lub IP:PORT) lub [0] aby wrócić: ").strip()
            
            if raw_input == '0' or not raw_input: break
            
            target_port = None
            if ":" in raw_input:
                target, port_part = raw_input.split(":")
                try: target_port = int(port_part)
                except: target = raw_input
            else:
                target = raw_input

            # Lista portów
            common_ports = {
                20: "FTP-DATA", 21: "FTP", 22: "SSH", 23: "TELNET", 25: "SMTP",
                53: "DNS", 67: "DHCP", 80: "HTTP", 443: "HTTPS", 3306: "MYSQL",
                8080: "HTTP-PROXY", 5432: "POSTGRESQL", 3389: "RDP (Win)"
            }
            
            if target_port:
                if target_port not in common_ports: common_ports[target_port] = "USER"
                print(f" [!] Cel: {target} (Port: {target_port})")
            else:
                print(f" [!] Cel: {target}")

            print(" [!] Skanowanie... (Ctrl+C przerywa)")
            print("-" * 55)
            
            results = f"Raport skanowania dla: {target}\n"
            
            for port, svc in sorted(common_ports.items()):
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.5)
                try:
                    res = s.connect_ex((target, port))
                    status = "OTWARTY" if res == 0 else "Zamknięty"
                    mark = " <<<" if res == 0 else ""
                    
                    line = f" Port {port:<6} [{svc:<12}]: {status}{mark}"
                    print(f" [i] {line}")
                    results += line + "\n"
                except Exception as e:
                    print(f" [!] Błąd port {port}: {e}")
                finally:
                    s.close()

            print("-" * 55)
            if input("\n [?] Zapisać raport? (t/n): ").lower() == 't':
                core_report.save(results, f"PortScan_{target.replace('.','_')}")
            
            input("\n Enter aby powtórzyć...")
            
        except KeyboardInterrupt: break
        except Exception as e:
            print(f"\n [BŁĄD]: {e}"); input(" Enter...")