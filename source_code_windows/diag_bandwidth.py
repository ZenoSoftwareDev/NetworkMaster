import os
import subprocess
import time

def run():
    while True:
        try:
            # Pobieranie danych bezpośrednio przez PowerShell
            cmd = 'powershell "Get-NetAdapterStatistics | Select-Object Name, ReceivedBytes, SentBytes | Format-Table -AutoSize"'
            result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
            
            os.system('cls')
            print("================================================================")
            print("                MONITOR PASMA SIECIOWEGO - LIVE")
            print("================================================================")
            print(" [i] Odświeżanie co 1s. Naciśnij Ctrl+C, aby wrócić do menu.")
            print("-" * 64)
            
            if result.stdout.strip():
                print(result.stdout)
            else:
                print(" [!] Oczekiwanie na dane z kart sieciowych...")
            
            time.sleep(1)
            
        except KeyboardInterrupt:
            # To pozwala wrócić do main.py po naciśnięciu Ctrl+C
            print("\n [i] Powrót do menu głównego...")
            time.sleep(0.5)
            break
        except Exception as e:
            print(f" [!] Błąd monitora: {e}")
            input(" Naciśnij Enter, aby kontynuować...")
            break