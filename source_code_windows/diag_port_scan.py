import os, socket, core_report

def run():
    while True:
        try:
            os.system('cls')
            # ZMIANA: Ogólny tytuł bez nazw producentów
            print("=== SKANER PORTÓW SIECIOWYCH ===")
            
            # ZMIANA: Czysty input bez sugerowania konkretnego IP
            raw_input = input("\n Podaj IP (lub IP:PORT) lub [0] aby wrócić: ").strip()
            
            if raw_input == '0' or not raw_input: break
            
            # --- LOGIKA ROZDZIELANIA IP I PORTU ---
            target_port = None
            if ":" in raw_input:
                target, port_part = raw_input.split(":")
                try:
                    target_port = int(port_part)
                except:
                    target = raw_input
            else:
                target = raw_input

            
            # Rozszerzona lista najpopularniejszych portów (Standardowe usługi)
            common_ports = {
                20: "FTP-DATA",
                21: "FTP",
                22: "SSH",
                23: "TELNET",
                25: "SMTP (MAIL)",
                53: "DNS",
                67: "DHCP",
                69: "TFTP",
                80: "HTTP (WWW)",
                110: "POP3",
                123: "NTP",
                135: "RPC (WIN)",
                137: "NETBIOS",
                139: "NETBIOS-SSN",
                143: "IMAP",
                161: "SNMP",
                389: "LDAP",
                443: "HTTPS (SSL)",
                445: "SMB (WIN)",
                465: "SMTP-SSL",
                514: "SYSLOG",
                554: "RTSP (CAM)",
                587: "SMTP-SUB",
                631: "IPP (PRINT)",
                636: "LDAPS",
                873: "RSYNC",
                993: "IMAP-SSL",
                995: "POP3-SSL",
                1194: "OPENVPN",
                1433: "MSSQL",
                1521: "ORACLE",
                1723: "PPTP",
                2049: "NFS",
                3306: "MYSQL",
                3389: "RDP (REMOTE)",
                5060: "SIP (VOIP)",
                5432: "POSTGRESQL",
                5500: "VNC-VIEWER",
                5900: "VNC-SERVER",
                6379: "REDIS",
                8000: "HTTP-ALT",
                8080: "HTTP-PROXY",
                8291: "WINBOX (MT)",
                8443: "HTTPS-ALT",
                9090: "COCKPIT",
                27017: "MONGODB"
            }
            
            # Jeśli użytkownik podał własny port w adresie (np. 1.1.1.1:5000), dodajemy go
            if target_port:
                if target_port not in common_ports:
                    common_ports[target_port] = "DEFINIOWANY"
                print(f" [!] Cel: {target} (Dodano port: {target_port})")
            else:
                print(f" [!] Cel: {target}")

            print(" [!] Skanowanie usług... (Ctrl+C przerywa)")
            print("-" * 55)
            
            results = f"Raport skanowania dla hosta: {target}\n"
            
            # Sortujemy porty, żeby wynik był czytelny
            for port, svc in sorted(common_ports.items()):
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.8) # Timeout 0.8s (optymalny dla LAN)
                
                try:
                    res = s.connect_ex((target, port))
                    
                    if res == 0:
                        status = "OTWARTY"
                        # Strzałka dla otwartych, żeby rzucało się w oczy
                        mark = " <<<" 
                    else:
                        status = "Zamknięty"
                        mark = ""
                    
                    # Formatowanie tabeli
                    line = f" Port {port:<6} [{svc:<12}]: {status}{mark}"
                    print(f" [i] {line}")
                    results += line + "\n"
                    
                except Exception as e:
                    print(f" [!] Błąd na porcie {port}: {e}")
                finally:
                    s.close()

            print("-" * 55)
            if input("\n [?] Zapisać raport na PULPICIE? (t/n): ").lower() == 't':
                core_report.save(results, f"PortScan_{target.replace('.','_')}")
            
            input("\n Naciśnij Enter, aby powtórzyć...")
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\n [BŁĄD KRYTYCZNY]: {e}")
            input(" Naciśnij Enter...")