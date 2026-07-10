import os, subprocess, time

G, R, C, Y, RESET = '\033[92m', '\033[91m', '\033[96m', '\033[93m', '\033[0m'

def run():
    os.system('cls')
    print(f"{R}================================================================{RESET}")
    print(f"           {Y}NAPRAWA POŁĄCZENIA SIECIOWEGO (HARD RESET){RESET}")
    print(f"{R}================================================================{RESET}")
    print(" Ta opcja wykona następujące czynności:")
    print(" 1. Reset Winsock (netsh winsock reset)")
    print(" 2. Reset stosu TCP/IP (netsh int ip reset)")
    print(" 3. Zwolnienie i odnowienie adresu IP (release/renew)")
    print(" 4. Wyczyszczenie pamięci DNS (flushdns)")
    print(f"\n {R}[UWAGA] Może być wymagany restart komputera!{RESET}")
    
    confirm = input("\n Czy na pewno chcesz kontynuować? (t/n): ").lower().strip()
    if confirm != 't': return

    print("\n [i] Rozpoczynam procedurę naprawczą...")
    time.sleep(1)

    steps = [
        ("Resetowanie katalogu Winsock...", "netsh winsock reset"),
        ("Resetowanie stosu TCP/IP...", "netsh int ip reset"),
        ("Zwalnianie obecnego adresu IP...", "ipconfig /release"),
        ("Czyszczenie pamięci podręcznej DNS...", "ipconfig /flushdns"),
        ("Odnawianie adresu IP (to może chwilę potrwać)...", "ipconfig /renew"),
    ]

    for desc, cmd in steps:
        print(f" [*] {desc}", end="", flush=True)
        try:
            # Ukrywamy output komend, żeby nie śmiecić
            subprocess.run(cmd, shell=True, capture_output=True)
            print(f" {G}[OK]{RESET}")
            time.sleep(0.5)
        except Exception as e:
            print(f" {R}[BŁĄD]{RESET}")

    print(f"\n {G}[SUKCES] Procedura zakończona.{RESET}")
    print(" Jeśli internet nadal nie działa, uruchom ponownie komputer.")
    
    input("\n Naciśnij Enter, aby wrócić...")