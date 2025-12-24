
import threading, base64, os, time, re, json, random, subprocess, string

from datetime import datetime, timedelta

from time import sleep, strftime

from bs4 import BeautifulSoup

import requests, socket, sys



try:

    from faker import Faker

    from requests import session

    from colorama import Fore, Style

    from random import randint

    import pystyle

    import socks

except:

    os.system("pip install faker")

    os.system("pip install requests")

    os.system("pip install colorama")

    os.system("pip install bs4")

    os.system("pip install pystyle")

    print('__Vui Lòng Chạy Lại Tool__')

    exit()

BASE_URL = "https://api.mail.tm"

from pystyle import Add, Center, Anime, Colors, Colorate, Write, System



# Màu sắc

xnhac = "\033[1;36m"

do = "\033[1;31m"

luc = "\033[1;32m"

vang = "\033[1;33m"

xduong = "\033[1;34m"

hong = "\033[1;35m"

trang = "\033[1;39m"

whiteb = "\033[1;39m"

red = "\033[0;31m"

redb = "\033[1;31m"

end = '\033[0m'

dev = "\033[1;39m[\033[1;31m\033[1;39m]\033[1;39m"

def banner():
    print(f"""
\033[1;32m ████████╗   ██╗ ██ ██╗   ██╗ █████╗ ███╗   ██╗██╗  ██╗
\033[1;32m ╚══██╔══╝   ██║██╔╝██║   ██║██   ██╗████╗  ██║██║  ██║
\033[1;32m    ██║      ████╔╝ ████████║███████║██╔██╗ ██║███████║
\033[1;32m    ██║      ██╔██╗ ██║   ██║██   ██║██║╚██╗██║██╔══██║
\033[1;32m    ██║      ██║╚██╗██║   ██║██   ██║██║  ████║██║  ██║
\033[1;32m    ╚═╝  ██  ╚═╝ ╚═╝╚═╝   ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝
\033[97m╔═════════════════════════════════════════════════╗
\033[1;97m║ Tool By: \033[1;32mShop T.Khanh            \033[1;97mPhiên Bản: \033[1;32m1.0 \033[97m║    
\033[97m╚═════════════════════════════════════════════════╝

\033[97m╔═══════════════════════════════════════════════════════╗
\033[1;97m║[\033[1;91m❣\033[1;97m]\033[1;97m Zalo\033[1;31m  : \033[1;97m☞ \033[1;36mhttp://zalo.me/0854533557\033[1;31m♔ \033[1;97m☜             ║
\033[1;97m║[\033[1;91m❣\033[1;97m]\033[1;97m Tiktok\033[1;31m  : \033[1;97m☞ \033[1;36m@tk_a_h\033[1;31m♔ \033[1;97m☜                         ║
\033[1;97m║[\033[1;91m❣\033[1;97m]\033[1;97m Facebook\033[1;31m : \033[1;97m☞ \033[1;36mhttps://www.facebook.com/tkhanh223\033[1;31m♔ \033[1;97m☜ ║
\033[97m╚═══════════════════════════════════════════════════════╝

""")
    
def random_name(length=8):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))

def get_domains():
    r = requests.get(f"{BASE_URL}/domains")
    r.raise_for_status()
    return r.json()["hydra:member"][0]["domain"]

def create_account(email, password):
    r = requests.post(
        f"{BASE_URL}/accounts",
        json={"address": email, "password": password}
    )
    r.raise_for_status()

def get_token(email, password):
    r = requests.post(
        f"{BASE_URL}/token",
        json={"address": email, "password": password}
    )
    r.raise_for_status()
    return r.json()["token"]

def get_messages(token):
    r = requests.get(
        f"{BASE_URL}/messages",
        headers={"Authorization": f"Bearer {token}"}
    )
    r.raise_for_status()
    return r.json()["hydra:member"]

def get_message_content(token, msg_id):
    r = requests.get(
        f"{BASE_URL}/messages/{msg_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    r.raise_for_status()
    return r.json().get("text", "") or r.json().get("html", "")

def extract_otp(text):
    match = re.search(r"\b[a-zA-Z0-9]{4,8}\b", text)
    return match.group(0) if match else None

def main():
    os.system("cls" if os.name == "nt" else "clear")
    banner()
    input("Nhấn Enter để tiếp tục")

    domain = get_domains()
    email = f"{random_name()}@{domain}"
    password = random_name(10)

    create_account(email, password)
    token = get_token(email, password)

    print(f"\nMail tạm thời: {email}")
    print("Đang lấy mã otp từ {email} ...\n")

    start = time.time()
    timeout = 90
    checked = set()

    while time.time() - start < timeout:
        messages = get_messages(token)

        for msg in messages:
            if msg["id"] in checked:
                continue

            checked.add(msg["id"])
            content = get_message_content(token, msg["id"])
            otp = extract_otp(content)

            if otp:
                print("Đã lấy mã otp thành công")
                print(f"Kết quả: {otp}")
                return

        print("Kết quả: Đang lấy mã otp...")
        time.sleep(3)

    print("\nLấy mã otp thất bại")
    print("Hãy kiểm tra hoặc reset mã otp")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
