import requests as req
import pytest


class TestAPIUserAgent:

    test_data = [
        ('Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
         {'platform': 'Mobile', 'browser': 'No', 'device': 'Android'}),
        ('Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1',
         {'platform': 'Mobile', 'browser': 'Chrome', 'device': 'iOS'}),
        ('Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
         {'platform': 'Googlebot', 'browser': 'Unknown', 'device': 'Unknown'}),
        ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0',
         {'platform': 'Web', 'browser': 'Chrome', 'device': 'No'})

    ]
    @pytest.mark.parametrize('user_agent, result', test_data)
    def test_user_agent(self, user_agent, result):
        '''
        Наша задача написать параметризированный тест.
        Этот тест должен брать из дата-провайдера User Agent и ожидаемые значения,
        GET-делать запрос с этим User Agent и убеждаться,
        что результат работы нашего метода правильный - т.е. в ответе ожидаемое значение всех трех полей.
       '''
        answer_lst = []
        url = "https://playground.learnqa.ru/ajax/api/user_agent_check"
        headers = {"User-Agent": user_agent}
        resp = req.get(url, headers=headers)
        assert resp.status_code == 200, "Wrong response code"
        resp_as_dict = resp.json()
        for key, val in result.items():
            if resp_as_dict.get(key) != val:
                answer_lst.append({key: resp_as_dict.get(key)})
        assert len(answer_lst) == 0, (f"Wrong answer. Prodlem User Agent '{user_agent}'\nWrong param: {answer_lst}.")


