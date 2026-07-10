import os, subprocess, core_report

def run_ipconfig():
    print(" [!] Pobieranie pełnej konfiguracji sieciowej...")
    res = subprocess.run("ipconfig /all", capture_output=True, text=True, shell=True, encoding='cp852').stdout
    print(res)
    core_report.save(res, "IPConfig_All")
    input("\nEnter...")

def run_netstat():
    while True:
        os.system('cls')
        print("=== MONITOR POŁĄCZEŃ I PORTÓW (Netstat) ===\n")
        print(" [1] Tylko AKTYWNE połączenia (ESTABLISHED)")
        print(" [2] Wszystkie porty i procesy (Pełna lista)")
        print(" [0] Powrót")
        
        c = input("\nWybór: ")
        if c == '0': break
        
        os.system('cls')
        if c == '1':
            print(" [i] Filtrowanie: Wyświetlanie tylko aktywnych sesji...\n")
            # Filtrujemy po statusie ESTABLISHED (Ustanowiono)
            cmd = 'netstat -ano | findstr ESTABLISHED'
            header = f" {'PROT.':<7} | {'ADRES LOKALNY':<22} | {'ADRES ZEWNĘTRZNY':<22} | {'PID'}\n"
        else:
            print(" [i] Generowanie pełnej listy portów...\n")
            cmd = 'netstat -ano'
            header = f" {'PROT.':<7} | {'ADRES LOKALNY':<22} | {'ADRES ZEWNĘTRZNY':<22} | {'STATUS':<15} | {'PID'}\n"

        res = subprocess.run(cmd, capture_output=True, text=True, shell=True).stdout
        
        print(header)
        print("-" * 80)
        print(res)
        
        full_output = header + "-"*80 + "\n" + res
        if input("\n [?] Zapisać ten widok do raportu? (t/n): ").lower() == 't':
            core_report.save(full_output, "Netstat_Report")
        
        input("\nNaciśnij Enter, aby kontynuować...")

def run_arp():
    os.system('cls')
    print(" [!] Pobieranie tablicy skojarzeń ARP (IP <-> MAC)...")
    res = subprocess.run("arp -a", capture_output=True, text=True, shell=True, encoding='cp852').stdout
    print(res)
    core_report.save(res, "ARP_Table")
    input("\nEnter...")