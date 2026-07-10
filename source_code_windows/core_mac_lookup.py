import time
import requests
import os

CACHE = {}

def get_vendor(mac):
    """Funkcja sprawdzająca producenta (API)"""
    if not mac or mac == "00:00:00:00:00:00":
        return "Bramka Systemowa"
    
    mac = mac.upper().replace("-", ":")
    if mac in CACHE: return CACHE[mac]

    # Wykrywanie MAC prywatnych (losowych w Windows/Android/iOS)
    # Jeśli drugi znak to 2, 6, A lub E (np. x2:xx:xx...)
    if len(mac) > 1 and mac[1] in "26AE":
        res = "Urządzenie Mobilne (MAC Prywatny/Losowy)"
        CACHE[mac] = res
        return res

    url = f"https://api.macvendors.com/{mac}"
    for _ in range(2): 
        try:
            time.sleep(0.6) # Lekkie opóźnienie dla API
            response = requests.get(url, timeout=4)
            if response.status_code == 200:
                vendor = response.text.strip()
                CACHE[mac] = vendor
                return vendor
            elif response.status_code == 429:
                time.sleep(1)
        except: pass
            
    return "Nieznany / Brak w bazie"

def run():
    """Tego brakowało - Menu interfejsu użytkownika"""
    while True:
        os.system('cls')
        print("================================================================")
        print("           SPRAWDZANIE PRODUCENTA PO ADRESIE MAC")
        print("================================================================")
        print(" Wpisz adres MAC (format XX:XX:XX:XX:XX:XX lub XX-XX...)")
        print(" [0] Powrót do menu głównego")
        print("----------------------------------------------------------------")
        
        mac = input("\n Adres MAC: ").strip()
        
        if mac == '0':
            break
            
        if len(mac) < 8:
            print(" [!] Za krótki adres. Spróbuj ponownie.")
            time.sleep(1)
            continue
            
        print(f"\n [i] Szukam producenta dla: {mac}...")
        try:
            vendor = get_vendor(mac)
            print("-" * 64)
            print(f" WYNIK: \033[92m{vendor}\033[0m")
            print("-" * 64)
        except Exception as e:
            print(f" [!] Błąd: {e}")
            
        input("\n Naciśnij Enter, aby sprawdzić kolejny...")