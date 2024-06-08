import pytest

from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_reqests import MyRequests


class TestUserRegister(BaseCase):
    exclude_params = [
        ('password'),
        ('username'),
        ('firstName'),
        ('lastName'),
        ('email'),
    ]

    def test_create_user_successfully(self):
        data = self.prepeare_registration_data()
        response = MyRequests.post('/user/', data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.asser_json_has_key(response, 'id')

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepeare_registration_data(email)

        response = MyRequests.post('/user/', data=data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_contend_value(response, f"Users with email '{email}' already exists")

    def test_create_user_with_incorrect_email(self):
        incorrect_email = 'vector_example.com'
        data = self.prepeare_registration_data(email=incorrect_email)
        response = MyRequests.post('/user/', data=data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_contend_value(response,'Invalid email format')

    @pytest.mark.parametrize('miss_val', exclude_params)
    def test_create_user_without_any_value(self, miss_val):
        data = self.prepeare_registration_data()
        data.pop(miss_val)
        response = MyRequests.post('/user/', data=data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_contend_value(response,f'The following required params are missed: {miss_val}')

    def test_create_user_with_short_firstname(self):
        data = self.prepeare_registration_data()
        data['firstName'] = 'f'
        response = MyRequests.post('/user/', data=data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_contend_value(response, "The value of 'firstName' field is too short")

    def test_create_user_with_huge_firstname(self):
        data = self.prepeare_registration_data()
        huge_first_name = ''.join([str(i) for i in range(250)])
        data['firstName'] = huge_first_name
        response = MyRequests.post('/user/', data=data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_contend_value(response, "The value of 'firstName' field is too long")

