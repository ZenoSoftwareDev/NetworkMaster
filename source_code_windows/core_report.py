import os, time, core_config

G, R, C, Y, RESET = '\033[92m', '\033[91m', '\033[96m', '\033[93m', '\033[0m'

def save(content, filename_prefix="Report"):
    """
    Zapisuje treść do pliku tekstowego w folderze Reports.
    filename_prefix: np. "PortScan_192.168.1.1"
    """
    # Dodajemy datę do nazwy pliku, żeby się nie nadpisywały
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    full_name = f"{filename_prefix}_{timestamp}.txt"
    
    # Używamy nowej ścieżki z core_config
    file_path = os.path.join(core_config.REPORTS_DIR, full_name)
    
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
            
        print(f"\n {G}[SUKCES]{RESET} Raport zapisano pomyślnie.")
        # Wyświetlamy relatywną ścieżkę (Reports/plik.txt), wygląda czyściej
        print(f" Lokalizacja: {C}Reports\\{full_name}{RESET}")
        
    except Exception as e:
        print(f"\n {R}[BŁĄD ZAPISU]{RESET} Nie udało się zapisać raportu.")
        print(f" Szczegóły: {e}")