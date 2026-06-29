import re
import requests

SOURCES = [
    "https://t.me",
    "https://t.me",
    "https://githubusercontent.com"
]

def fetch_configs():
    unique_configs = set()
    vless_pattern = re.compile(r'vless://[^\s"<]+')

    for url in SOURCES:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                matches = vless_pattern.findall(response.text)
                for match in matches:
                    clean_config = match.split('\\')[0].split('"')[0].strip()
                    unique_configs.add(clean_config)
        except Exception as e:
            print(f"Ошибка: {e}")

    with open("my_vless_configs.txt", "w", encoding="utf-8") as f:
        for config in sorted(unique_configs):
            f.write(config + "\n")

if __name__ == "__main__":
    fetch_configs()
