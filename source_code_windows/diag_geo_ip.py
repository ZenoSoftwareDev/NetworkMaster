import os, requests, core_report

def run():
    os.system('cls')
    print("=== LOKALIZACJA GEOGRAFICZNA IP ===\n")
    print(" [i] Pobieranie danych o Twoim publicznym adresie IP...")
    
    try:
        # Korzystamy z darmowego API ip-api
        response = requests.get("http://ip-api.com/json/").json()
        
        if response['status'] == 'success':
            data = f"""
 ADRES IP:    {response['query']}
 KRAJ:        {response['country']} ({response['countryCode']})
 MIASTO:      {response['city']}
 REGION:      {response['regionName']}
 DOSTAWCA:    {response['isp']}
"""
            print(data)
            
            print("-" * 40)
            if input(" [?] Zapisać raport na PULPICIE? (t/n): ").lower() == 't':
                core_report.save(data, "Raport_GeoIP")
                print(" [OK] Zapisano.")
        else:
            print(" [!] Nie udało się pobrać danych.")
            
    except Exception as e:
        print(f" [!] Błąd połączenia z serwerem GeoIP: {e}")
        print(" [i] Upewnij się, że masz połączenie z internetem.")
        
    input("\n Naciśnij Enter, aby wrócić...")