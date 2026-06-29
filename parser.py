import re
import requests
import base64

# Ваши сохраненные источники
SOURCES = [
    "https://raw.githubusercontent.com/zieng2/wl/refs/heads/main/vless_universal.txt", 
    "https://raw.githubusercontent.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/6.txt"
]

def decode_base64(text):
    try: return base64.b64decode(text).decode('utf-8')
    except: return text

def fetch_configs():
    unique_configs = {} # Словарь для автоматического удаления дубликатов по технической части
    vless_pattern = re.compile(r'vless://[^\s"<]+')

    headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15'}

    for url in SOURCES:
        try:
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code == 200:
                raw_text = response.text
                matches = vless_pattern.findall(raw_text)
                
                # Если в файле зашит base64, расшифровываем его
                if not matches:
                    matches = vless_pattern.findall(decode_base64(raw_text.strip()))
                
                for match in matches:
                    clean_config = match.replace('"', '').replace("'", "").replace('\\', '').strip()
                    
                    if "@" in clean_config and len(clean_config) > 30:
                        # Отсекаем название после знака #, чтобы сравнивать только UUID, IP и Порт
                        tech_part = clean_config.split('#')[0] if '#' in clean_config else clean_config
                        
                        # Если такой конфиг уже попадался в других источниках, он не продублируется
                        unique_configs[tech_part] = clean_config
        except Exception as e:
            print(f"Ошибка при чтении {url}: {e}")

    # Запись результатов в ваш файл
    with open("my_vless_configs.txt", "w", encoding="utf-8") as f:
        if unique_configs:
            for config_url in sorted(unique_configs.values()):
                f.write(config_url + "\n")
            print(f"Успешно сохранено уникальных конфигов: {len(unique_configs)}")
        else:
            f.write("# На данный момент конфигов не найдено.\n")
            print("Конфиги не найдены.")

if __name__ == "__main__":
    fetch_configs()
