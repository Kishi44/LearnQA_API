import requests
import pytest

class TestUserAuth():
    def test_auth_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = requests.post('https://playground.learnqa.ru/api/user/login', data=data)

        assert 'auth_sid' in response1.cookies, 'There is no auth cookie in the response'
        assert 'x-csrf-token' in response1.headers, 'There is no CSRF token header in the response'
        assert 'user_id' in response1.json(), 'There is no user id in the response'

        auth_sid = response1.cookies.get('auth_sid')
        token = response1.headers.get('x-csrf-token')
        user_id_from_auth = response1.json()['user_id']

        response2 = requests.get(
            'https://playground.learnqa.ru/api/user/auth',
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid}
        )

        assert 'user_id' in response2.json(), 'There is no user id in the second response'
        user_id_from_check = response2.json()['user_id']

        assert user_id_from_auth == user_id_from_check, ' ID не совпадают'

    exclude_params = [
        ('no_cookie'),
        ('no_token')
    ]
    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative_check(self, condition):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = requests.post('https://playground.learnqa.ru/api/user/login', data=data)

        assert 'auth_sid' in response1.cookies, 'There is no auth cookie in the response'
        assert 'x-csrf-token' in response1.headers, 'There is no CSRF token header in the response'
        assert 'user_id' in response1.json(), 'There is no user id in the response'

        auth_sid = response1.cookies.get('auth_sid')
        token = response1.headers.get('x-csrf-token')

        if condition == 'no_cookie':
            response2 = requests.get(
                'https://playground.learnqa.ru/api/user/auth',
                headers={'x-csrf-token': token}
            )
        else:
            response2 = requests.get(
                'https://playground.learnqa.ru/api/user/auth',
                cookies={'auth_sid': auth_sid}
            )

        assert 'user_id' in response1.json(), 'There is no user id in the second response'
        user_id_from_check = response2.json()['user_id']

        assert user_id_from_check == 0, f'User is auth with condition {condition}'


