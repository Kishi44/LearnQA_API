import requests
"""
1. Wrong method provided
2. код 400
3. {"success":"!"}
4.
"""
#1.
response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type")
print(response.text)
print(response.status_code)

#2.
response = requests.head("https://playground.learnqa.ru/ajax/api/compare_query_type")
print(response.text)
print(response.status_code)

#3.
params = {"method": "GET"}
response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params)
print(response.text)
print(response.status_code)

#4.
# for i in ["GET", "POST", "PUT", "DELETE", "HEAD"]:
#     params = {"method": i}
#
#     print(i)
#     response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params=params)
#     print(response.text)
#     print(response.status_code)
#     print()
