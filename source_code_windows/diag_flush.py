import os, subprocess, time

def run():
    print(" [!] Czyszczenie pamięci DNS...")
    subprocess.run("ipconfig /flushdns", shell=True)
    print(" [OK] Pomyślnie wyczyszczono resolver DNS.")
    time.sleep(1)