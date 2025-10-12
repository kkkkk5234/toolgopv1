import requests
import time
import json

LOGIN_URL = "https://traodoisub.com/scr/login.php"
TRANSFER_URL = "https://traodoisub.com/view/tangxu/tangxu.php"

username = input("Nhập username: ").strip()
password = input("Nhập password: ").strip()
target_user = input("Người nhận xu: ").strip()
amount = input("Số xu muốn chuyển: ").strip()

BASE_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://traodoisub.com",
    "Referer": "https://traodoisub.com/",
    "X-Requested-With": "XMLHttpRequest",
}

def main():
    with requests.Session() as s:
        s.headers.update(BASE_HEADERS)

        login_data = {"username": username, "password": password}
        try:
            print("[*] Đang đăng nhập...")
            resp = s.post(LOGIN_URL, data=login_data, timeout=15)
            resp.raise_for_status()
        except requests.RequestException as e:
            print("Lỗi đăng nhập:", e)
            return

        login_ok = False
        try:
            j = resp.json()
            print("[<=] Login JSON:", j)
            if isinstance(j, dict) and (j.get("status") in (1, "1", "success") or j.get("success") in (1, True, "true")):
                login_ok = True
            elif "success" in str(j).lower() or "thành công" in str(j).lower():
                login_ok = True
        except ValueError:
            txt = resp.text or ""
            print("[<=] Login text:", txt[:800])
            if "Đăng nhập thành công" in txt or "success" in txt.lower():
                login_ok = True

        if not login_ok:
            print("Đăng nhập thất bại.")
            return

        time.sleep(1)
        transfer_data = {"usernhan": target_user, "xutang": amount}
        try:
            print(f"[*] Chuyển {amount} xu đến {target_user} ...")
            resp2 = s.post(TRANSFER_URL, data=transfer_data, timeout=15)
            resp2.raise_for_status()
        except requests.RequestException as e:
            print("Lỗi khi chuyển xu:", e)
            return

        try:
            j2 = resp2.json()
            print("[<=] Phản hồi:", json.dumps(j2, indent=2, ensure_ascii=False))
        except ValueError:
            txt2 = resp2.text or ""
            print("[<=] Phản hồi:")
            print(txt2[:2000])

        print("[✓] Hoàn tất.")

if __name__ == "__main__":
    main()
