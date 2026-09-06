import json

import requests

text = input("Введите текст для картинки: ")
url = f"https://cataas.com/cat/says/{text}"
response = requests.get(url)

print(url)
print(response.status_code)
print(response.headers)
print(response.headers.get('Content-Type'))
print(len(response.content))

cat_image = response.content


token = input("Введите токен с Полигона Яндекс.Диска: ")
headers = {"Authorization": f"OAuth {token}"}

params = {"path": "PY-158"}
response = requests.put(
    'https://cloud-api.yandex.net/v1/disk/resources',
    headers=headers,
    params=params
)

print(response.status_code)
print(response.text)

params = {
    "path": f"PY-158/{text}.jpg",
    "overwrite": "true"
}
response = requests.get(
    'https://cloud-api.yandex.net/v1/disk/resources/upload',
    headers=headers,
    params=params
)

print(response.status_code)
print(response.text)

href = response.json()['href']

response = requests.put(href, data=cat_image)

print(response.status_code)
print(response.text)


file_info = {
    "file_name": f"{text}.jpg",
    "size": len(cat_image)
}

result = [file_info]

with open("result.json", "w", encoding="utf-8") as file:
    json.dump(result, file, ensure_ascii=False, indent=4)