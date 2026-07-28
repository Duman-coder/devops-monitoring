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
    hosts = []
    try:
        with open(filename, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if "," in line:
                    parts = line.split(",")
                    name = parts[0].strip()
                    ip = parts[1].strip()
                    hosts.append({"name": name, "ip": ip})
                else:
                    hosts.append({"name": line, "ip": line})
    except FileNotFoundError:
        hosts = [{"name": "8.8.8.8", "ip": "8.8.8.8"}]
    return hosts

def write_log(result):
    log_file = os.path.expanduser("~/logs/ping_results.json")
    os.makedirs(os.path.expanduser("~/logs"), exist_ok=True)
    with open(log_file, "a") as f:
        f.write(json.dumps(result) + "\n")

def main():
    hosts_file = os.path.expanduser("~/hosts.txt")
    hosts = read_hosts(hosts_file)
    interval = int(os.getenv("CHECK_INTERVAL", "60"))
    host_status = {h["ip"]: True for h in hosts}

    print(f"Мониторинг запущен. Устройств: {len(hosts)}, интервал: {interval}с", flush=True)
    send_telegram(f"🚀 <b>Мониторинг запущен</b>\nУстройств: {len(hosts)}\nИнтервал: {interval}с")

    while True:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n=== Проверка: {now} ===", flush=True)

        available = 0
        unavailable = 0
        newly_down = []
        newly_up = []

        for h in hosts:
            name = h["name"]
            ip = h["ip"]
            status = check_host(ip)

            result = {
                "timestamp": now,
                "name": name,
                "host": ip,
                "status": "up" if status else "down"
            }
            write_log(result)

            if status:
                available += 1
                if not host_status.get(ip, True):
                    newly_up.append(f"✅ {name} ({ip})")
                host_status[ip] = True
            else:
                unavailable += 1
                if host_status.get(ip, True):
                    newly_down.append(f"🔴 {name} ({ip})")
                host_status[ip] = False

        print(f"Итого: {available} up, {unavailable} down", flush=True)

        if newly_down:
            msg = f"🔴 <b>ХОСТЫ НЕДОСТУПНЫ</b>\n🕐 {now}\n\n"
            msg += "\n".join(newly_down)
            send_telegram(msg)

        if newly_up:
            msg = f"✅ <b>ХОСТЫ ВОССТАНОВЛЕНЫ</b>\n🕐 {now}\n\n"
            msg += "\n".join(newly_up)
            send_telegram(msg)

        if unavailable > 0:
            down_hosts = [h for h in hosts if not host_status.get(h["ip"], True)]
            print("Недоступны:", flush=True)
            for h in down_hosts:
                print(f"  ✗ {h['name']} ({h['ip']})", flush=True)

        time.sleep(interval)

if __name__ == "__main__":
    main()
