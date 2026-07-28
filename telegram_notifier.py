import subprocess
import json
import urllib.request
import time
import os

TELEGRAM_TOKEN = "8904638973:AAGXTE_35CpvcRgv3uUesFkKdEb1KFM6m6E"
TELEGRAM_CHAT_ID = "572022108"
SSH_HOST = "zabbixesvm@10.40.40.12"
LOG_FILE = "~/logs/ping_results.json"

def send_telegram(message):
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
        print("Telegram отправлено", flush=True)
    except Exception as e:
        print(f"Telegram ошибка: {e}", flush=True)

def get_latest_results():
    try:
        result = subprocess.run(
            ["ssh", "-o", "StrictHostKeyChecking=no",
             SSH_HOST, f"tail -300 {LOG_FILE}"],
            capture_output=True, text=True, timeout=10
        )
        lines = result.stdout.strip().split("\n")
        results = []
        for line in lines:
            if line.strip():
                try:
                    results.append(json.loads(line))
                except:
                    pass
        return results
    except Exception as e:
        print(f"SSH ошибка: {e}", flush=True)
        return []

def main():
    print("Telegram notifier запущен", flush=True)
    send_telegram("🚀 <b>Telegram Notifier запущен</b>\nПолучаю данные с Zabbix сервера...")

    prev_down = set()

    while True:
        results = get_latest_results()

        if not results:
            time.sleep(60)
            continue

        # берём последние результаты для каждого хоста
        latest = {}
        for r in results:
            latest[r["host"]] = r

        current_down = {
            ip: data for ip, data in latest.items()
            if data["status"] == "down"
        }

        newly_down = {ip: data for ip, data in current_down.items()
                      if ip not in prev_down}
        newly_up = {ip: data for ip, data in latest.items()
                    if ip in prev_down and data["status"] == "up"}

        if newly_down:
            msg = f"🔴 <b>ХОСТЫ НЕДОСТУПНЫ</b>\n\n"
            for ip, data in newly_down.items():
                name = data.get("name", ip)
                msg += f"• {name} ({ip})\n"
            send_telegram(msg)

        if newly_up:
            msg = f"✅ <b>ХОСТЫ ВОССТАНОВЛЕНЫ</b>\n\n"
            for ip, data in newly_up.items():
                name = data.get("name", ip)
                msg += f"• {name} ({ip})\n"
            send_telegram(msg)

        prev_down = set(current_down.keys())

        if current_down:
            print(f"Недоступно: {len(current_down)} устройств", flush=True)
        else:
            print(f"Все устройства доступны", flush=True)

        time.sleep(60)

if __name__ == "__main__":
    main()
