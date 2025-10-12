from pystyle import Add, Center, Anime, Colors, Colorate, Write, System
import requests, json, os, sys
from sys import platform
from time import sleep
from datetime import datetime

total = 0
may = 'mb' if platform[0:3] == 'lin' else 'pc'
CONFIG_FILE = "config.txt"


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


def banner():

    banner = f"""


"""

    for X in banner:

        sys.stdout.write(X)

        sys.stdout.flush()

        sleep(0.000001)

def _now():
    return datetime.now().strftime('%H:%M:%S')

LEVEL_MAP = {
    'SYSTEM': ('SYSTEM', Colors.cyan_to_blue),
    'LOGIN' : ('LOGIN' , Colors.green_to_white),
    'TASK'  : ('TASK'  , Colors.yellow_to_red),
    'FOLLOW': ('FOLLOW', Colors.green_to_white),
    'TIM'   : ('TIM'   , Colors.yellow_to_red),
    'ERROR' : ('ERROR' , Colors.red_to_yellow),
    'DELAY' : ('DELAY' , Colors.cyan_to_blue),
    'COIN'  : ('COIN'  , Colors.green_to_white),
}

def log(level, group, message, icon=""):
    tag, color = LEVEL_MAP.get(level, ('LOG', Colors.cyan_to_blue))
    t = _now()
    text = f"[{t}] [{group}] {icon} {message}"
    try:
        colored = Colorate.Horizontal(color, text)
        print(colored)
    except Exception:
        print(text)

def newbie_delay(dl):
    try:
        for i in range(dl, 0, -1):
            log('DELAY', 'SYSTEM', f"⏳ Chờ {i}s...", icon="⏳")
            sleep(1)
    except Exception:
        sleep(dl)
        log('DELAY', 'SYSTEM', f"⏳ Chờ {dl}s... (fallback)", icon="⏳")

def newbie_open(link, may):
    try:
        if may == 'mb':
            os.system(f'xdg-open "{link}"')
        else:
            os.system(f'cmd /c start "" "{link}"')
        log('SYSTEM', 'OPEN', f"🔗 Mở liên kết: {link}")
    except Exception as e:
        log('ERROR', 'OPEN', f"❌ Không thể mở liên kết: {e}")

class TraoDoiSub_Api:
    def __init__(self, token):
        self.token = token

    def get_profile(self):
        try:
            res = requests.get(f'https://traodoisub.com/api/?fields=profile&access_token={self.token}', timeout=15)
            data = res.json()
            return data.get('data', False)
        except Exception as e:
            log('ERROR', 'LOGIN', f"❌ Lỗi lấy profile: {e}")
            return False

    def configure_user(self, user):
        try:
            res = requests.get(f'https://traodoisub.com/api/?fields=tiktok_run&id={user}&access_token={self.token}', timeout=15)
            data = res.json()
            return data.get('data', False)
        except Exception as e:
            log('ERROR', 'CONFIG', f"❌ Lỗi cấu hình user: {e}")
            return False

    def fetch_job(self, type_):
        try:
            res = requests.get(f'https://traodoisub.com/api/?fields={type_}&access_token={self.token}', timeout=15)
            return res
        except Exception as e:
            log('ERROR', 'TASK', f"❌ Lỗi fetch nhiệm vụ {type_}: {e}")
            return False

    def check_cache(self, id_, type_):
        try:
            res = requests.get(f'https://traodoisub.com/api/coin/?type={type_}&id={id_}&access_token={self.token}', timeout=15)
            data = res.json()
            return 'cache' in data
        except Exception:
            return False

    def collect_coin(self, id_, type_):
        global total
        try:
            res = requests.get(f'https://traodoisub.com/api/coin/?type={type_}&id={id_}&access_token={self.token}', timeout=15)
            data = res.json().get('data', {})
            xu = data.get('xu', 0)
            msg = data.get('msg', '')
            job = data.get('job_success', None)
            xuthem = data.get('xu_them', 0)
            total += xuthem
            log('COIN', 'COIN', f"💰 Nhận: +{xuthem} xu | {msg} | Tổng: {total} xu")
            if job == 0:
                return 0
            return True
        except Exception as e:
            txt = getattr(e, 'message', str(e))
            log('ERROR', 'COIN', f"❌ Nhận xu thất bại: {txt}")
            return False

def show_banner():
    banner_lines = [
      " ████████╗   ██╗ ██ ██╗   ██╗ █████╗ ███╗   ██╗██╗  ██╗",
      " ╚══██╔══╝   ██║██╔╝██║   ██║██   ██╗████╗  ██║██║  ██║",
      "    ██║      ████╔╝ ████████║███████║██╔██╗ ██║███████║",
      "    ██║      ██╔██╗ ██║   ██║██   ██║██║╚██╗██║██╔══██║",
      "    ██║      ██║╚██╗██║   ██║██   ██║██║  ████║██║  ██║",
      "    ╚═╝  ██  ╚═╝ ╚═╝╚═╝   ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝",
        "   ╔═════════════════════════════════════════════════╗",
        "   ║ Tool By: Shop T.Khanh            Phiên Bản: 1.0 ║",    
        "   ╚═════════════════════════════════════════════════╝",

        "╔═══════════════════════════════════════════════════════╗",
        "║[❣] Zalo : ☞ http://zalo.me/0854533557♔ ☜              ║",
        "║[❣] Tiktok : ☞ @tk_a_hplus\033[1;31m♔ ☜                    ║",
        "║[❣] Facebook : ☞ https://www.facebook.com/tkhanh223♔ ☜ ║",
        "╚═══════════════════════════════════════════════════════╝"
    ]
    try:
        text = "\n".join(banner_lines)
        Anime.Fade(Add.Add(banner_lines), color=Colors.blue_to_cyan, interval=0.03, enter=True)
    except Exception:
        for line in banner_lines:
            log('SYSTEM', 'BANNER', line)

def newbietool_main():
    dem = 0
    show_banner()

    token = None
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                token = f.read().strip()
                log('SYSTEM', 'LOGIN', "🔑 Đã tải access_token từ file.")
        except Exception:
            token = None

    while True:
        if not token:
            token = input("Nhập Access_Token TDS: ").strip()
            with open(CONFIG_FILE, 'w') as f:
                f.write(token)
            log('SYSTEM', 'LOGIN', "🔑 Đã lưu access_token vào file.")
        tds = TraoDoiSub_Api(token)
        profile = tds.get_profile()
        if profile:
            try:
                xu = profile.get('xu', 0)
                xudie = profile.get('xudie', 0)
                user = profile.get('user', 'Unknown')
                log('LOGIN', 'LOGIN', f"✅ Đăng nhập thành công | Tài khoản: {user} | Xu: {xu} | Xu bị phạt: {xudie}")
                break
            except Exception:
                log('ERROR', 'LOGIN', "❌ Lỗi khi đọc profile, token có thể không hợp lệ.")
                token = None
                if os.path.exists(CONFIG_FILE):
                    os.remove(CONFIG_FILE)
                continue
        else:
            log('ERROR', 'LOGIN', "❌ Access Token không hợp lệ. Vui lòng thử lại.")
            token = None
            if os.path.exists(CONFIG_FILE):
                os.remove(CONFIG_FILE)
            continue


    while True:
        log('SYSTEM', 'MENU', "🔸 Chọn nhiệm vụ: [1] TIM | [2] FOLLOW | [3] FOLLOW NOW")
        nhiem_vu = input("Nhập Số Để Chạy Nhiệm Vụ: ").strip()
        try:
            dl = int(input("Nhập Delay (giây): ").strip())
        except:
            log('ERROR', 'INPUT', "❌ Delay không hợp lệ, sử dụng mặc định 3s.")
            dl = 3


        while True:
            try:
                nv_nhan = int(input("Sau bao nhiêu nhiệm vụ thì nhận xu (>=8, <=15): ").strip())
            except:
                log('ERROR', 'INPUT', "❌ Giá trị không hợp lệ. Nhập lại.")
                continue
            if nv_nhan < 8:
                log('ERROR', 'INPUT', "⚠️ Phải >= 8 nhiệm vụ để tránh lỗi.")
                continue
            if nv_nhan > 15:
                log('ERROR', 'INPUT', "⚠️ Giữ < 15 nhiệm vụ để tránh lỗi.")
                continue
            break

        user_cau_hinh = input("Nhập User Name TikTok cần cấu hình: ").strip()
        cau_hinh = tds.configure_user(user_cau_hinh)
        if not cau_hinh:
            log('ERROR', 'CONFIG', f"❌ Cấu hình thất bại cho user: {user_cau_hinh}")
            continue
        user = cau_hinh.get('uniqueID', user_cau_hinh)
        id_acc = cau_hinh.get('id', '0')
        os.system("cls" if os.name == "nt" else "clear")
        log('SYSTEM', 'CONFIG', f"🔧 Cấu hình thành công | ID: {id_acc} | User: {user}")

        dem = 0

        while True:
            if '1' in nhiem_vu:
                log('TASK', 'TIM', "🔍 Đang lấy nhiệm vụ TIM (like)...")
                listlike = tds.fetch_job('tiktok_like')
                if not listlike:
                    log('ERROR', 'TIM', "❌ Không lấy được nhiệm vụ Like.")
                    sleep(2); continue
                if 'error' in listlike.text:
                    err = listlike.json().get('error', '')
                    if err == 'Thao tác quá nhanh vui lòng chậm lại':
                        coun = listlike.json().get('countdown', 1)
                        log('SYSTEM', 'TIM', f"⏳ COUNTDOWN: {coun}")
                        sleep(2); continue
                    elif err == 'Vui lòng ấn NHẬN TẤT CẢ rồi sau đó tiếp tục làm nhiệm vụ để tránh lỗi!':
                        tds.collect_coin('TIKTOK_LIKE_API', 'TIKTOK_LIKE')
                        sleep(2); continue
                    else:
                        log('ERROR', 'TIM', f"❌ {err}")
                        sleep(2); continue
                try:
                    listlike = listlike.json().get('data', [])
                except Exception:
                    log('ERROR', 'TIM', "❌ Lỗi phân tích dữ liệu nhiệm vụ TIM.")
                    sleep(2); continue

                if len(listlike) == 0:
                    log('SYSTEM', 'TIM', "⚠️ Hết nhiệm vụ Like.")
                    sleep(2); continue

                log('SYSTEM', 'TIM', f"🔎 Tìm thấy {len(listlike)} nhiệm vụ Like.")
                for i in listlike:
                    id_ = i.get('id')
                    link = i.get('link')
                    newbie_open(link, may)
                    cache = tds.check_cache(id_, 'TIKTOK_LIKE_CACHE')
                    if not cache:
                        log('SYSTEM', 'TIM', f"✖️ Chưa cache (bỏ qua): {id_}")
                        sleep(1); continue
                    dem += 1
                    log('TIM', 'TIM', f"Đang làm nhiệm vụ | id: {id_} | [{dem}]")
                    newbie_delay(dl)
                    if dem % nv_nhan == 0:
                        nhan = tds.collect_coin('TIKTOK_LIKE_API', 'TIKTOK_LIKE')
                        if nhan == 0:
                            log('ERROR', 'COIN', "❌ Nhận xu thất bại. Chọn hành động:")
                            log('SYSTEM', 'CHOICE', "[1] Thay nhiệm vụ | [2] Thay Acc TikTok | [Enter] Tiếp tục")
                            chon = input("Lựa chọn: ").strip()
                            if chon == '1':
                                nhiem_vu = input("Nhập Số Để Chạy Nhiệm Vụ: ").strip()
                                break
                            elif chon == '2':
                                token = None
                                if os.path.exists(CONFIG_FILE):
                                    os.remove(CONFIG_FILE)
                                return

            if '2' in nhiem_vu:
                log('TASK', 'FOLLOW', "🔍 Đang lấy nhiệm vụ FOLLOW...")
                listfollow = tds.fetch_job('tiktok_follow')
                if not listfollow:
                    log('ERROR', 'FOLLOW', "❌ Không lấy được nhiệm vụ Follow.")
                    sleep(2); continue
                if 'error' in listfollow.text:
                    err = listfollow.json().get('error', '')
                    if err == 'Thao tác quá nhanh vui lòng chậm lại':
                        coun = listfollow.json().get('countdown', 1)
                        log('SYSTEM', 'FOLLOW', f"⏳ COUNTDOWN: {coun}")
                        sleep(2); continue
                    elif err == 'Vui lòng ấn NHẬN TẤT CẢ rồi sau đó tiếp tục làm nhiệm vụ để tránh lỗi!':
                        tds.collect_coin('TIKTOK_FOLLOW_API', 'TIKTOK_FOLLOW')
                        sleep(2); continue
                    else:
                        log('ERROR', 'FOLLOW', f"❌ {err}")
                        sleep(2); continue
                try:
                    listfollow = listfollow.json().get('data', [])
                except Exception:
                    log('ERROR', 'FOLLOW', "❌ Lỗi phân tích dữ liệu nhiệm vụ FOLLOW.")
                    sleep(2); continue

                if len(listfollow) == 0:
                    log('SYSTEM', 'FOLLOW', "⚠️ Hết nhiệm vụ Follow.")
                    sleep(2); continue

                log('SYSTEM', 'FOLLOW', f"🔎 Tìm thấy {len(listfollow)} nhiệm vụ Follow.")
                for i in listfollow:
                    id_ = i.get('id')
                    link = i.get('link')
                    newbie_open(link, may)
                    cache = tds.check_cache(id_, 'TIKTOK_FOLLOW_CACHE')
                    if not cache:
                        log('SYSTEM', 'FOLLOW', f"✖️ Chưa cache (bỏ qua): {id_}")
                        sleep(1); continue
                    dem += 1
                    log('FOLLOW', 'FOLLOW', f"Đang làm nhiệm vụ | id: {id_} | [{dem}]")
                    newbie_delay(dl)
                    if dem % nv_nhan == 0:
                        nhan = tds.collect_coin('TIKTOK_FOLLOW_API', 'TIKTOK_FOLLOW')
                        if nhan == 0:
                            log('ERROR', 'COIN', "❌ Nhận xu thất bại.")
                            chon = input("Lựa chọn (1: đổi nhiệm vụ, 2: đổi acc): ").strip()
                            if chon == '1':
                                nhiem_vu = input("Nhập Số Để Chạy Nhiệm Vụ: ").strip()
                                break
                            elif chon == '2':
                                token = None
                                if os.path.exists(CONFIG_FILE):
                                    os.remove(CONFIG_FILE)
                                return

            if '3' in nhiem_vu:
                log('TASK', 'FOLLOW_NOW', "🔍 Đang lấy nhiệm vụ FOLLOW NOW...")
                listfollow = tds.fetch_job('tiktok_follow')
                if not listfollow:
                    log('ERROR', 'FOLLOW_NOW', "❌ Không lấy được nhiệm vụ Follow Now.")
                    sleep(2); continue
                if 'error' in listfollow.text:
                    err = listfollow.json().get('error', '')
                    if err == 'Thao tác quá nhanh vui lòng chậm lại':
                        coun = listfollow.json().get('countdown', 1)
                        log('SYSTEM', 'FOLLOW_NOW', f"⏳ COUNTDOWN: {coun}")
                        sleep(2); continue
                    elif err == 'Vui lòng ấn NHẬN TẤT CẢ rồi sau đó tiếp tục làm nhiệm vụ để tránh lỗi!':
                        tds.collect_coin('TIKTOK_FOLLOW_API', 'TIKTOK_FOLLOW')
                        sleep(2); continue
                    else:
                        log('ERROR', 'FOLLOW_NOW', f"❌ {err}")
                        sleep(2); continue
                try:
                    listfollow = listfollow.json().get('data', [])
                except Exception:
                    log('ERROR', 'FOLLOW_NOW', "❌ Lỗi phân tích dữ liệu nhiệm vụ FOLLOW NOW.")
                    sleep(2); continue

                if len(listfollow) == 0:
                    log('SYSTEM', 'FOLLOW_NOW', "⚠️ Hết nhiệm vụ Follow Now.")
                    sleep(2); continue

                log('SYSTEM', 'FOLLOW_NOW', f"🔎 Tìm thấy {len(listfollow)} nhiệm vụ Follow Now.")
                for i in listfollow:
                    id_ = i.get('id')
                    uid = str(id_).split('_')[0]
                    que = i.get('uniqueID', '')
                    if may == 'mb':
                        newbie_open(f'tiktoknow://user/profile?user_id={uid}', may)
                    else:
                        newbie_open(f'https://now.tiktok.com/@{que}', may)
                    cache = tds.check_cache(id_, 'TIKTOK_FOLLOW_CACHE')
                    if not cache:
                        log('SYSTEM', 'FOLLOW_NOW', f"✖️ Chưa cache (bỏ qua): {id_}")
                        sleep(1); continue
                    dem += 1
                    log('FOLLOW', 'FOLLOW_NOW', f"Đang làm nhiệm vụ NOW | id: {id_} | [{dem}]")
                    newbie_delay(dl)
                    if dem % nv_nhan == 0:
                        nhan = tds.collect_coin('TIKTOK_FOLLOW_API', 'TIKTOK_FOLLOW')
                        if nhan == 0:
                            log('ERROR', 'COIN', "❌ Nhận xu thất bại. Chọn hành động:")
                            chon = input("Lựa chọn: ").strip()
                            if chon == '1':
                                nhiem_vu = input("Nhập Số Để Chạy Nhiệm Vụ: ").strip()
                                break
                            elif chon == '2':
                                token = None
                                if os.path.exists(CONFIG_FILE):
                                    os.remove(CONFIG_FILE)
                                return

if __name__ == "__main__":
    try:
        newbietool_main()
    except KeyboardInterrupt:
        log('SYSTEM', 'EXIT', "🔚 Thoát chương trình bởi người dùng.")
    except Exception as e:
        log('ERROR', 'CRASH', f"❌ Ứng dụng gặp lỗi: {e}")
