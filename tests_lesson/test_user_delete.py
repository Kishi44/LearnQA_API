import pytest

from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_reqests import MyRequests
import allure
from time import sleep


@allure.epic("Delete user cases")
class TestUserDelete(BaseCase):

    @allure.description("Try delete user ID 2")
    def test_delete_user_2(self):

        with allure.step('Login user 2'):
            login_data = {
                'email': 'vinkotov@example.com',
                'password': '1234'
            }
            response1 = MyRequests.post("/user/login", data=login_data)
            Assertions.assert_code_status(response1, 200)

            auth_sid = self.get_cookie(response1, 'auth_sid')
            token = self.get_header(response1, 'x-csrf-token')

        with allure.step('Delete user 2'):

            response2 = MyRequests.delete('/user/2',
                                          headers={'x-csrf-token': token},
                                          cookies={'auth_sid': auth_sid})

        Assertions.assert_code_status(response2, 400)
        Assertions.assert_contend_value(response2, '{"error":"Please, do not delete test users with ID 1, 2, 3, 4 or 5."}')

    @allure.description('Delete user successfully')
    def test_delete_user_successfully(self):
        with allure.step("Create new user"):
            register_data = self.prepeare_registration_data()
            response1 = MyRequests.post('/user/', data=register_data)

            Assertions.assert_code_status(response1, 200)
            Assertions.asser_json_has_key(response1, "id")

            email = register_data['email']
            password = register_data['password']
            user_id = self.get_json_value(response1, 'id')

        with allure.step('Login new user'):
            login_data = {
                'email': email,
                'password': password
            }
            response2 = MyRequests.post("/user/login", data=login_data)

            auth_sid = self.get_cookie(response2, 'auth_sid')
            token = self.get_header(response2, 'x-csrf-token')

        with allure.step('Delete user'):
            response2 = MyRequests.delete(f'/user/{user_id}',
                                          headers={'x-csrf-token': token},
                                          cookies={'auth_sid': auth_sid})
            Assertions.assert_code_status(response2, 200)

        with allure.step("Check that the user has been deleted"):
            response3 = MyRequests.get(f'/user/{user_id}',
                                       headers={'x-csrf-token': token},
                                       cookies={'auth_sid': auth_sid}
                                       )
            Assertions.assert_code_status(response3, 404)
            Assertions.assert_contend_value(response3, 'User not found')

    @allure.description('Try to delete user when auth with another one')
    def test_delete_user_auth_another(self):
        with allure.step("Register user 1"):
            register_data = self.prepeare_registration_data()
            response1 = MyRequests.post('/user/', data=register_data)

            Assertions.assert_code_status(response1, 200)
            Assertions.asser_json_has_key(response1, "id")

            user_id_1 = self.get_json_value(response1, 'id')
            email_1 = register_data['email']
            password_1 = register_data['password']

        with allure.step('Login user 1'):
            login_data = {
                'email': email_1,
                'password': password_1
            }
            response2 = MyRequests.post("/user/login", data=login_data)

            auth_sid_1 = self.get_cookie(response2, 'auth_sid')
            token_1 = self.get_header(response2, 'x-csrf-token')

        with allure.step("Register user 2"):
            sleep(1)
            register_data = self.prepeare_registration_data()
            response3 = MyRequests.post('/user/', data=register_data)

            Assertions.assert_code_status(response3, 200)
            Assertions.asser_json_has_key(response3, "id")

            user_id_2 = self.get_json_value(response3, 'id')
            email_2 = register_data['email']
            password_2 = register_data['password']

        with allure.step('Login user 2'):
            login_data_2 = {
                'email': email_2,
                'password': password_2
            }
            response4 = MyRequests.post("/user/login", data=login_data_2)

            auth_sid_2 = self.get_cookie(response4, 'auth_sid')
            token_2 = self.get_header(response4, 'x-csrf-token')

        with allure.step("try delete"):
            response5 = MyRequests.delete(f'/user/{user_id_1}',
                                          headers={'x-csrf-token': token_2},
                                          cookies={'auth_sid': auth_sid_2})

            Assertions.assert_code_status(response5, 400)
            Assertions.assert_contend_value(response5, '{"error":"This user can only delete their own account."}')

        with allure.step('Checking users'):
            response6 = MyRequests.get(f"/user/{user_id_1}",
                                           headers={'x-csrf-token': token_1},
                                           cookies={'auth_sid': auth_sid_1},
                                           )
            Assertions.assert_code_status(response6, 200)

            response7 = MyRequests.get(f"/user/{user_id_2}",
                                       headers={'x-csrf-token': token_2},
                                       cookies={'auth_sid': auth_sid_2},
                                       )
            Assertions.assert_code_status(response6, 200)



