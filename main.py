import json
import os
from urllib.parse import quote

import requests


text = input("Введите текст для картинки: ")

encoded_text = quote(text, safe="")
url = f"https://cataas.com/cat/says/{encoded_text}"

response = requests.get(url)
response.raise_for_status()

cat_image = response.content


token = os.environ.get("YANDEX_TOKEN")

if not token:
    raise ValueError("Не задана переменная окружения YANDEX_TOKEN")

headers = {"Authorization": f"OAuth {token}"}


params = {"path": "PY-158"}

response = requests.put(
    "https://cloud-api.yandex.net/v1/disk/resources",
    headers=headers,
    params=params
)

if response.status_code != 409:
    response.raise_for_status()


params = {
    "path": f"PY-158/{text}.jpg",
    "overwrite": "true"
}

response = requests.get(
    "https://cloud-api.yandex.net/v1/disk/resources/upload",
    headers=headers,
    params=params
)

response.raise_for_status()

href = response.json()["href"]


response = requests.put(href, data=cat_image)
response.raise_for_status()


file_info = {
    "file_name": f"{text}.jpg",
    "size": len(cat_image)
}

result = [file_info]

with open("result.json", "w", encoding="utf-8") as file:
    json.dump(result, file, ensure_ascii=False, indent=4)

print("Готово")