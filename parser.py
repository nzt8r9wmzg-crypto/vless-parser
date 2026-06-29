import re
import requests

# Проверенные источники, где точно есть VLESS-ссылки в открытом виде
SOURCES = [
    "https://raw.githubusercontent.com/zieng2/wl/refs/heads/main/vless_universal.txt", 
    "https://raw.githubusercontent.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/6.txt"# Ссылка обновлена на README
]

def fetch_configs():
    unique_configs = set()
    # Более надежное регулярное выражение для поиска vless://
    vless_pattern = re.compile(r'vless://[^\s"<]+')

    for url in SOURCES:
        try:
            # Маскируемся под обычный браузер, чтобы сайты не блокировали скрипт
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                matches = vless_pattern.findall(response.text)
                for match in matches:
                    # Очищаем ссылку от возможных остатков HTML-кода и кавычек
                    clean_config = match.replace('"', '').replace("'", "").replace('\\', '').strip()
                    # Проверяем, что ссылка не обрезана и содержит базовую структуру
                    if len(clean_config) > 20 and "@" in clean_config:
                        unique_configs.add(clean_config)
        except Exception as e:
            print(f"Ошибка при чтении {url}: {e}")

    # Записываем результат
    with open("my_vless_configs.txt", "w", encoding="utf-8") as f:
        if unique_configs:
            for config in sorted(unique_configs):
                f.write(config + "\n")
            print(f"Успешно сохранено конфигов: {len(unique_configs)}")
        else:
            # Если ничего не нашли, запишем об этом в файл, чтобы вы видели статус
            f.write("# На данный момент живых конфигов в источниках не найдено. Попробуем в следующий цикл.\n")
            print("Конфиги не найдены.")

if __name__ == "__main__":
    fetch_configs()
