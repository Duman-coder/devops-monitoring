import subprocess
import datetime
import json
import os
import time
import urllib.request

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

def send_telegram(message):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = json.dumps({
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }).encode()
    req = urllib.request.Request(url, data=data)
    req.add_header("Content-Type", "application/json")
    try:
        urllib.request.urlopen(req)
    except Exception as e:
        print(f"Telegram ошибка: {e}", flush=True)

def check_host(host):
    result = subprocess.run(
        ["ping", "-c", "1", "-W", "2", host],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    return result.returncode == 0

def read_hosts(filename):
    try:
        with open(filename, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return ["8.8.8.8", "1.1.1.1", "google.com"]

def write_log(result):
    log_file = os.path.expanduser("~/logs/ping_results.json")
    os.makedirs(os.path.expanduser("~/logs"), exist_ok=True)
    with open(log_file, "a") as f:
        f.write(json.dumps(result) + "\n")

def main():
    hosts = read_hosts(os.path.expanduser("~/hosts.txt"))
    interval = int(os.getenv("CHECK_INTERVAL", "60"))
    host_status = {host: True for host in hosts}

    print(f"Мониторинг запущен. Интервал: {interval}с", flush=True)
    print(f"Хосты: {hosts}", flush=True)

    send_telegram("🚀 <b>Мониторинг запущен</b>\nОтслеживаю: " + ", ".join(hosts))

    while True:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n=== Проверка: {now} ===", flush=True)

        available = 0
        unavailable = 0

        for host in hosts:
            status = check_host(host)
            result = {
                "timestamp": now,
                "host": host,
                "status": "up" if status else "down"
            }
            write_log(result)

            if status:
                print(f"OK | {host}", flush=True)
                available += 1
                if not host_status[host]:
                    send_telegram(f"✅ <b>Хост восстановлен</b>\n🌐 {host}\n🕐 {now}")
                host_status[host] = True
            else:
                print(f"FAIL | {host}", flush=True)
                unavailable += 1
                if host_status[host]:
                    send_telegram(f"🔴 <b>ХОСТ НЕДОСТУПЕН</b>\n🌐 {host}\n🕐 {now}")
                host_status[host] = False

        print(f"Итого: {available} up, {unavailable} down", flush=True)
        time.sleep(interval)

if __name__ == "__main__":
    main()
