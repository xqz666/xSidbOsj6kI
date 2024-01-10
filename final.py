import os
import time
import requests
from datetime import datetime, timedelta
import platform
import signal
import pyfiglet
#from rich import print

title = pyfiglet.figlet_format('P C D - ID', font='xsbookb')


session = requests.Session()
session.verify = False

bot_token = '6912377174:AAHUApQEpyssi_uNNVDkDrdoS-_TKrCQokQ'
chat_id = '5338801749'

file_path = "/data/data/com.termux/files/usr/etc/.license"
default_content = "by @PemburuCelanaDalam - @chzklf"
is_running = True

# ANSI escape codes untuk warna RGB
def rgb_color(r, g, b):
    return f"\033[38;2;{r};{g};{b}m"

# Reset warna ANSI
def reset_color():
    return "\033[0m"

def save_and_exit(signum, frame):
    global is_running
    print("\nUser menekan CTRL+C, Exiting script...")

    # Set isi license.txt kembali ke default_content
    with open(file_path, "w") as file:
        file.write(default_content)
    
    is_running = False  # Hentikan loop utama
    exit()

def test_connection():
    try:
        response = requests.get("https://pastebin.com/raw/S2A0nhjr", timeout=1)
        response.raise_for_status()
      #  print(f"{rgb_color(0, 255, 0)}Connected..{reset_color()}")
        return response.text.strip()
    except requests.exceptions.RequestException as e:
        print(f"{rgb_color(255, 0, 0)}Cannot connect to pastebin.com. Check your internet connection. ({e}){reset_color()}")
        return None

        
# {"validasi":"ya","expired":"15-01-2024"}
def exp():
    try:
        response = requests.get("https://pastebin.com/raw/2QLf2uq3", timeout=1)
        validator = requests.get("https://pastebin.com/raw/ck10H3AD", timeout=1)
        response.raise_for_status()

        content = response.json()
        content_validator = validator.text.strip()

        validation_key = content_validator.strip()

        if 'validasi' in content and content['validasi'] == validation_key:
            if 'expired' in content:
                expiration_date = content['expired']
                current_date = datetime.now().strftime("%d-%m-%Y")

                if datetime.strptime(expiration_date, "%d-%m-%Y") < datetime.strptime(current_date, "%d-%m-%Y"):
                    print(f"{rgb_color(255, 0, 0)}Script expired! Mohon join channel @PemburuCelanaDalam untuk informasi lebih lanjut.\nDetail: Sudah Expired sejak {expiration_date}{reset_color()}")
                    save_default_content()
                    exit(1)
                else:
                    print(f"{rgb_color(0, 255, 0)}Tervalidasi !\nExpiration Date: {expiration_date}\n")
            else:
                print(f"{rgb_color(255, 0, 0)}Invalid license format! 'expired' key is missing.{reset_color()}")
                save_default_content()
                exit(1)
        else:
            print(f"{rgb_color(255, 0, 0)}Invalid validation key!{reset_color()}")
            save_default_content()
            exit(1)

        return content

    except requests.exceptions.RequestException as e:
        print(f"{rgb_color(255, 0, 0)}Cannot connect to Pastebin. Check your internet connection. ({e}){reset_color()}")
        save_default_content()
        return None

def save_default_content():
    # Set isi license.txt kembali ke default_content
    with open(file_path, "w") as file:
        file.write(default_content)

        



def send_result_to_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}"
        requests.get(url)
    except Exception as e:
        print(f"{rgb_color(255, 0, 0)}Error{reset_color()}")

def get_device_info():
    try:
        os_info = platform.system() + " " + platform.version()
        return f"Device Information: {os_info}"
    except Exception as e:
        return f"Error"

def main():
    global is_running
    signal.signal(signal.SIGINT, save_and_exit)

    show_welcome_message()
    
    while is_running:
        pastebin_url = "https://pastebin.com/raw/S2A0nhjr"
        license_content = exp()
        
        if license_content is not None:
            if os.path.exists(file_path):
                with open(file_path, "w") as file:
                    file.write(requests.get(pastebin_url).text.strip())
                print(f"{rgb_color(0, 255, 0)}Lisensi berhasil diganti\nbuka new tab lalu jalankan script IGC!{reset_color()}\n")
                # Tunggu selama 30 menit sebelum mengganti lagi
                time.sleep(1800)
            else:
                print(f"{rgb_color(255, 0, 0)}File .license tidak ditemukan, jalankan script IGC terlebih dahulu!{reset_color()}")
        else:
            print(f"{rgb_color(255, 0, 0)}Terjadi masalah saat menghubungkan ke pastebin.com. Merubah isi .license menjadi nilai awal.{reset_color()}")
            
            # Update .license content to default_content
            with open(file_path, "w") as file:
                file.write(default_content)
                
    # Move exit(1) outside of the while loop
    exit(1)
            
def show_welcome_message():
    print(f'{rgb_color(196, 54, 247)}{title}{reset_color()}')
    time.sleep(1.5)
    print(f"{rgb_color(255, 165, 0)}Meng-Autentikasi..{reset_color()}")
    license_content = test_connection()

    if license_content is not None:
        send_result_to_telegram(f"IGC Bypasser Monitor\n\nStatus: Connected\nIP: {requests.get('https://api.ipify.org').text}\nWaktu: {datetime.now().strftime('%H:%M:%S - %d/%m/%y')}")
        

if __name__ == "__main__":
    main()
