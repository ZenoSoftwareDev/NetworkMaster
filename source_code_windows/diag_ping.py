import os, subprocess

def run_menu():
    while True:
        os.system('cls')
        print("=== MENU PING ===\n [1] Google (4x)\n [2] Google (-t)\n [3] Własny (4x)\n [4] Własny (-t)\n")
        print(" --- KONIEC ---")
        print(" [0] Powrót")
        
        c = input("\nWybór: ")
        if c == '0': break
        
        try:
            if c == '1': subprocess.run("ping 8.8.8.8", shell=True)
            elif c == '2': subprocess.run("ping 8.8.8.8 -t", shell=True)
            elif c == '3': 
                adr = input(" Adres: ")
                subprocess.run(f"ping {adr}", shell=True)
            elif c == '4': 
                adr = input(" Adres: ")
                subprocess.run(f"ping {adr} -t", shell=True)
            
            # Pauza po zakończeniu poprawnego pingu
            input("\n[KONIEC] Naciśnij Enter, aby kontynuować...")
            
        except KeyboardInterrupt:
            # Pauza po przerwaniu przez CTRL+C
            print("\n\n [!] Ping przerwany przez użytkownika.")
            input(" Naciśnij Enter, aby wrócić do menu pingu...")