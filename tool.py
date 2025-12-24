import requests
import time
import re
import random
import string
import sys

BASE_URL = "https://api.mail.tm"

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
    input("(Nhấn Enter để tiếp tục)")

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
