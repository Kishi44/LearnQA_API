import requests as req


class TestAPI:
    def test_cookie(self):
        '''
        Необходимо написать тест, который делает запрос на метод: https://playground.learnqa.ru/api/homework_cookie
        Этот метод возвращает какую-то cookie с каким-то значением.
        Необходимо с помощью функции print() понять что за cookie и с каким значением,
        и зафиксировать это поведение с помощью assert
         '''

        url = "https://playground.learnqa.ru/api/homework_cookie"
        resp = req.get(url)
        assert resp.status_code == 200, "Wrong response code"

        cookie = resp.cookies

        assert 'HomeWork' in cookie, "There is no field 'answer' in the cookie"
        assert cookie['HomeWork'] == 'hw_value', "Wrong cookie"





