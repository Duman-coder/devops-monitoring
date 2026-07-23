import subprocess
import datetime
import json
import os
import time

def check_host(host):
    """Проверяет доступность хоста через ping"""
    result = subprocess.run(
        ["ping", "-c", "1", "-W", "2", host],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    return result.returncode == 0

def read_hosts(filename):
    """Читает список хостов из файла"""
    try:
        with open(filename, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return ["8.8.8.8", "1.1.1.1", "google.com"]

def write_log(result):
    """Записывает результат в лог файл"""
    log_file = "/app/logs/ping_results.json"
    os.makedirs("/app/logs", exist_ok=True)
    with open(log_file, "a") as f:
        f.write(json.dumps(result) + "\n")

def main():
    hosts = read_hosts("/app/hosts.txt")
    interval = int(os.getenv("CHECK_INTERVAL", "60"))

    print(f"Мониторинг запущен. Интервал: {interval}с")
    print(f"Хосты: {hosts}")

    while True:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n=== Проверка: {now} ===")

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
                print(f"✓ {host} — доступен")
                available += 1
            else:
                print(f"✗ {host} — недоступен")
                unavailable += 1

        print(f"Итого: {available} up, {unavailable} down")
        time.sleep(interval)

if __name__ == "__main__":
    main()
