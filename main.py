import requests

text = input("Введите текст для картинки: ")
url = f"https://cataas.com/cat/says/{text}"
response = requests.get(url)

print(url)
print(response.status_code)
print(response.headers)
print(response.headers.get('Content-Type'))
print(len(response.content))