"""
Наша задача - написать скрипт, который делал бы следующее:

1) создавал задачу
2) делал один запрос с token ДО того, как задача готова, убеждался в правильности поля status
3) ждал нужное количество секунд с помощью функции time.sleep() - для этого надо сделать import time
4) делал бы один запрос c token ПОСЛЕ того, как задача готова, убеждался в правильности поля status и наличии поля result
"""

import requests
import time


response1 = requests.get(' https://playground.learnqa.ru/ajax/api/longtime_job')
parsed_response = response1.json()
token = parsed_response['token']
wait_time = parsed_response['seconds']
params = {"token": token}

response2 = requests.get(' https://playground.learnqa.ru/ajax/api/longtime_job', params=params)
assert response2.json()['status'] == 'Job is NOT ready', 'Не верный статус'


time.sleep(wait_time)

response3 = requests.get(' https://playground.learnqa.ru/ajax/api/longtime_job', params=params)
parsed_response3 = response3.json()
status = parsed_response3['status']
assert status == 'Job is ready' and parsed_response3.get('result') is not None, 'Не верный ответ'