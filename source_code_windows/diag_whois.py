import os, subprocess, core_report, re

def run():
    while True:
        os.system('cls')
        print("=== WHOIS / REJESTRACJA DOMENY ===\n")
        domain = input(" Podaj domenę (np. google.com) lub [0] aby wrócić: ")
        if not domain or domain == '0': break
        
        print(f"\n [i] Pobieranie danych dla: {domain}...")
        cmd = f'powershell "Invoke-RestMethod https://rdap.org/domain/{domain}"'
        res_raw = subprocess.run(cmd, capture_output=True, text=True, shell=True).stdout
        
        try:
            # Uproszczone wyciąganie danych za pomocą regex, aby uniknąć błędów przy braku kluczy
            created = re.search(r'eventAction":"registration","eventDate":"([^"]+)"', res_raw)
            expired = re.search(r'eventAction":"expiration","eventDate":"([^"]+)"', res_raw)
            status = re.search(r'ldhName":"([^"]+)","events"', res_raw)
            
            output = f"\n WYNIK DLA: {domain.upper()}\n"
            output += f" {'-'*40}\n"
            output += f" REJESTRACJA: {created.group(1)[:10] if created else 'Brak danych'}\n"
            output += f" WYGASA:      {expired.group(1)[:10] if expired else 'Brak danych'}\n"
            output += f" SERWER WHOIS: {domain}\n"
            output += f" {'-'*40}\n"
            
            print(output)
            
            if input(" [?] Zapisać raport na PULPICIE? (t/n): ").lower() == 't':
                core_report.save(res_raw, f"Whois_{domain}")
                print(" [OK] Zapisano.")
                
        except:
            print(" [!] Błąd interpretacji danych lub domena nie istnieje.")
        
        input("\n Naciśnij Enter, aby sprawdzić kolejną domenę...")