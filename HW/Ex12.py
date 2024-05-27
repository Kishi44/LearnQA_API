import requests as req


class TestAPIHeader:
    def test_header(self):
        '''
        Необходимо написать тест, который делает запрос на метод: https://playground.learnqa.ru/api/homework_header
        Этот метод возвращает headers с каким-то значением.
        Необходимо с помощью функции print() понять что за headers и с каким значением,
        и зафиксировать это поведение с помощью assert
       '''

        url = " https://playground.learnqa.ru/api/homework_header"
        resp = req.get(url)
        assert resp.status_code == 200, "Wrong response code"

        header = resp.headers

        assert 'x-secret-homework-header' in header, "There is no field 'answer' in the cookie"
        assert header['x-secret-homework-header'] == 'Some secret value', "Wrong header"