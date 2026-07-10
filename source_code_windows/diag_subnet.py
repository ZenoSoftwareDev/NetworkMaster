import os, ipaddress, time

G, R, C, Y, RESET = '\033[92m', '\033[91m', '\033[96m', '\033[93m', '\033[0m'

def run():
    while True:
        os.system('cls')
        print(f"{C}================================================================{RESET}")
        print(f"                {Y}KALKULATOR PODSIECI (IP CALCULATOR){RESET}")
        print(f"{C}================================================================{RESET}")
        
        raw = input("\n Podaj adres IP z maską (np. 192.168.1.55/24) \n lub samo IP (zapyta o maskę): ").strip()
        
        if not raw or raw == '0': break
        
        try:
            # Obsługa wpisania samego IP bez ukośnika
            if "/" not in raw:
                print("\n [1] /24 (255.255.255.0)   [2] /16 (255.255.0.0)   [3] /8")
                mask_input = input(" Podaj maskę (CIDR np. 24 lub format dziesiętny): ").strip()
                
                # Szybkie skróty
                if mask_input == '1': mask_input = '24'
                elif mask_input == '2': mask_input = '16'
                elif mask_input == '3': mask_input = '8'
                
                # Jeśli user wpisał maskę np. 255.255.255.0, ipaddress to obsłuży
                target = f"{raw}/{mask_input}"
            else:
                target = raw

            # Obliczenia biblioteką ipaddress
            net = ipaddress.IPv4Network(target, strict=False)
            ip_obj = ipaddress.IPv4Interface(target)
            
            # Wyliczanie zakresu
            hosts = list(net.hosts())
            first_host = hosts[0] if hosts else "N/A"
            last_host = hosts[-1] if hosts else "N/A"
            total_hosts = net.num_addresses - 2 if net.num_addresses > 2 else 0

            print(f"\n {G}>>> WYNIK OBLICZEŃ:{RESET}")
            print(f" ----------------------------------------------------------------")
            print(f" ADRES IP:       {ip_obj.ip}")
            print(f" MASKA (CIDR):   {net.netmask} (/{net.prefixlen})")
            print(f" ADRES SIECI:    {C}{net.network_address}{RESET}")
            print(f" BROADCAST:      {C}{net.broadcast_address}{RESET}")
            print(f" ----------------------------------------------------------------")
            print(f" PIERWSZY HOST:  {Y}{first_host}{RESET}")
            print(f" OSTATNI HOST:   {Y}{last_host}{RESET}")
            print(f" LICZBA HOSTÓW:  {G}{total_hosts}{RESET}")
            print(f" ----------------------------------------------------------------")

        except Exception as e:
            print(f"\n {R}[BŁĄD] Nieprawidłowy format adresu IP lub maski!{RESET}")
            print(f" Szczegóły: {e}")
            
        input("\n Naciśnij Enter, aby liczyć dalej (lub '0' w IP by wyjść)...")