import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect")
print(len(response.history))
for i in response.history:
    print(i.url)

print(response.url)