import requests
import pytest
from lib.base_case import BaseCase


class TestUserAuth(BaseCase):

    exclude_params = [
        ('no_cookie'),
        ('no_token')
    ]

    def setup_class(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = requests.post('https://playground.learnqa.ru/api/user/login', data=data)

        self.auth_sid = self.get_cookie(response1, 'auth_sid')
        self.token = self.get_header(response1, 'x-csrf-token')
        self.user_id_from_auth = self.get_json_value(response1, 'user_id')

    def test_auth_user(self):

        response2 = requests.get(
            'https://playground.learnqa.ru/api/user/auth',
            headers={'x-csrf-token': self.token},
            cookies={'auth_sid': self.auth_sid}
        )

        assert 'user_id' in response2.json(), 'There is no user id in the second response'
        user_id_from_check = response2.json()['user_id']

        assert self.user_id_from_auth == user_id_from_check, ' ID не совпадают'


    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative_check(self, condition):

        if condition == 'no_cookie':
            response2 = requests.get(
                'https://playground.learnqa.ru/api/user/auth',
                headers={'x-csrf-token': self.token}
            )
        else:
            response2 = requests.get(
                'https://playground.learnqa.ru/api/user/auth',
                cookies={'auth_sid': self.auth_sid}
            )

        assert 'user_id' in response2.json(), 'There is no user id in the second response'
        user_id_from_check = response2.json()['user_id']

        assert user_id_from_check == 0, f'User is auth with condition {condition}'


