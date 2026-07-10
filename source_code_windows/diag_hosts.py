import os, subprocess

PATH = r"C:\Windows\System32\drivers\etc\hosts"

def run():
    while True:
        os.system('cls')
        print("=== EDYTOR PLIKU HOSTS ===\n")
        print(" [1] Wyświetl zawartość")
        print(" [2] Dodaj wpis (IP Domena)")
        print(" [3] Otwórz w Notatniku (Admin)")
        print(" [0] Powrót")
        
        c = input("\nWybór: ")
        if c == '0': break
        elif c == '1':
            with open(PATH, 'r') as f: print(f.read())
            input("\nEnter...")
        elif c == '2':
            ip = input(" Podaj IP: ")
            dom = input(" Podaj Domenę: ")
            with open(PATH, 'a') as f: f.write(f"\n{ip} {dom}")
            print(" [OK] Dodano."); os.system('pause')
        elif c == '3':
            subprocess.run(f"notepad.exe {PATH}", shell=True)