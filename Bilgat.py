import socket
import time
import sys
import os
import threading
import random
from concurrent.futures import ThreadPoolExecutor

# Tentative d'importation de requests avec gestion d'erreur automatique
try:
    import requests
except ImportError:
    print("Installing missing dependencies...")
    os.system(sys.executable + " -m pip install requests")
    import requests

"""
INSTRUCTIONS / HOW TO USE:
1. Target: Enter the IP address (e.g., 1.1.1.1) or Domain (e.g., google.com) you want to monitor.
2. Requests Count: Enter how many requests to send. Enter '0' for an infinite loop.
3. Speed: The engine is pre-set to 200 threads for maximum frequency.
4. Stop: Press ENTER or CTRL+C at any time to stop the process.
"""

# --- Couleurs ANSI pour un design Matrix/Cyber ---
class Col:
    G1 = '\033[38;5;46m'   # Vert Brillant
    G2 = '\033[38;5;40m'   # Vert Moyen
    G3 = '\033[38;5;34m'   # Vert Sombre
    G4 = '\033[38;5;28m'   # Vert Profond
    DARK_GREEN = '\033[38;5;28m'
    GREEN = '\033[38;5;46m' # Added to fix the 'AttributeError'
    CYAN = '\033[38;5;51m'
    WHITE = '\033[38;5;255m'
    RED = '\033[38;5;196m'
    YELLOW = '\033[38;5;226m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    clear_screen()
    # Application d'un dégradé sur le logo personnalisé
    banner = f"""
{Col.G1} ▒██  ██▒ ██░ ██ ▓█████  ██▓     ██▓    
{Col.G2} ▒▒ █ █ ▒░▓██░ ██▒▓█   ▀ ▓██▒     ▓██▒    
{Col.G3} ░░  █   ░▒██▀▀██░▒███   ▒██░     ▒██░    
{Col.G4}  ░ █ █ ▒ ░▓█ ░██ ▒▓█  ▄ ▒██░     ▒██░    
{Col.G3} ▒██▒ ▒██▒░▓█▒░██▓░▒████▒░██████▒░██████▒
{Col.G2} ▒▒ ░ ░▓ ░ ▒ ░░▒░▒░░ ▒░ ░░ ▒░▓  ░░ ▒░▓  ░
{Col.G1} ░░   ░▒ ░ ▒ ░▒░ ░ ░ ░  ░░ ░ ▒  ░░ ░ ▒  ░
{Col.G2}  ░    ░   ░  ░░ ░   ░      ░ ░      ░ ░  
{Col.G3}  ░    ░   ░  ░  ░   ░  ░     ░  ░     ░  
{Col.RESET}
    {Col.BOLD}{Col.WHITE}>> XHELL ENGINE // OVERPOWERED PROXY ROTATOR v8.0 <<{Col.RESET}
    """
    print(banner)

WORKING_PROXIES = []
STOP_EVENT = threading.Event()

def fetch_free_proxies():
    """Récupère des vrais proxies pour la rotation IP."""
    print(f"{Col.DARK_GREEN}[*] Accessing Proxy Database...{Col.RESET}")
    try:
        url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            proxy_list = response.text.split('\r\n')
            proxies = [p.strip() for p in proxy_list if p.strip()]
            print(f"{Col.GREEN}[+] {len(proxies)} identities ready for injection.{Col.RESET}")
            return proxies
    except Exception as e:
        # Fallback print if Col.RED fails for some reason
        print(f"FAILED TO FETCH PROXIES: {e}")
    return []

def check_host_real_proxy(target, port, request_id, proxy_list):
    """Moteur de connexion ultra-puissant via proxy."""
    if STOP_EVENT.is_set():
        return

    proxy = random.choice(proxy_list) if proxy_list else None
    
    try:
        start_time = time.perf_counter()
        
        if proxy:
            try:
                p_ip, p_port = proxy.split(':')
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.7)
                result = sock.connect_ex((p_ip, int(p_port)))
                sock.close()
            except:
                result = 1
            
            end_time = time.perf_counter()
            latency = round((end_time - start_time) * 1000, 2)
            
            if result == 0:
                status = f"{Col.GREEN}INJECTED{Col.RESET}"
                color = Col.GREEN
            else:
                status = f"{Col.RED}FAILED{Col.RESET}"
                color = Col.RED
                latency = "0.00"
        else:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((target, port))
            sock.close()
            status = f"{Col.YELLOW}DIRECT_IP{Col.RESET}"
            color = Col.YELLOW
            latency = "---"

        sys.stdout.write(
            f"\r{Col.DARK_GREEN}[{Col.WHITE}{request_id:06d}{Col.DARK_GREEN}]{Col.RESET} "
            f"{Col.GREEN}ID:{Col.RESET} {color}{proxy if proxy else 'LOCAL':<21}{Col.RESET} "
            f"{Col.GREEN}STATE:{Col.RESET} {status} "
            f"{Col.GREEN}LAT:{Col.RESET} {Col.WHITE}{latency}ms{Col.RESET}          "
        )
        sys.stdout.flush()

    except Exception:
        pass

def listen_for_stop():
    """Écoute la touche Entrée pour arrêter le script."""
    try:
        input()
        STOP_EVENT.set()
    except EOFError:
        pass

def main():
    print_banner()
    
    global WORKING_PROXIES
    WORKING_PROXIES = fetch_free_proxies()

    try:
        print(f"\n{Col.WHITE}--- CONFIGURATION ---{Col.RESET}")
        target = input(f"{Col.GREEN}┌──({Col.WHITE}root@xhell{Col.GREEN})-[{Col.WHITE}~/enter_target_ip{Col.GREEN}]\n└─> {Col.RESET}")
        if not target: 
            print(f"{Col.RED}[!] Target cannot be empty.{Col.RESET}")
            time.sleep(2)
            return
            
        try:
            limit_input = input(f"{Col.GREEN}└─({Col.WHITE}enter_requests_count{Col.GREEN})> {Col.RESET}")
            max_requests = int(limit_input) if limit_input else 0
        except ValueError:
            max_requests = 0

        threads_count = 200
        print(f"\n{Col.GREEN}[!] INITIALIZING POWER CORE...{Col.RESET}")
        print(f"{Col.DARK_GREEN}[*] Mode: Hyper-Speed | Threads: {threads_count} | Rotation: ACTIVE{Col.RESET}")
        print(f"{Col.YELLOW}[!] PRESS 'ENTER' TO STOP THE PROCESS{Col.RESET}\n")
        time.sleep(1)
        
        # Démarrage du thread d'écoute pour l'arrêt
        stop_thread = threading.Thread(target=listen_for_stop, daemon=True)
        stop_thread.start()

        request_count = 1
        
        with ThreadPoolExecutor(max_workers=threads_count) as executor:
            while not STOP_EVENT.is_set():
                if max_requests > 0 and request_count > max_requests:
                    break
                
                executor.submit(check_host_real_proxy, target, 80, request_count, WORKING_PROXIES)
                request_count += 1
                
                if request_count % 15 == 0:
                    time.sleep(0.0001)

        print(f"\n\n{Col.GREEN}[+] PROCESS STOPPED. ALL STREAMS FLUSHED.{Col.RESET}")
        input("Press Enter to close...") # Empêche la fermeture immédiate de la console

    except KeyboardInterrupt:
        print(f"\n\n{Col.RED}[!] FORCE EXIT DETECTED.{Col.RESET}")
        os._exit(0) 
    except Exception as e:
        print(f"\n{Col.RED}[!] SYSTEM CRASH : {e}{Col.RESET}")
        input("Press Enter to close...")

if __name__ == "__main__":
    main()