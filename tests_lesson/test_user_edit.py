from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_reqests import MyRequests
import allure


@allure.epic('Check user edit')
class TestUserEdit(BaseCase):

    def setup_class(self):
        self.new_name = "Changed Name"

        with allure.step("Register user"):
            register_data = self.prepeare_registration_data()
            response1 = MyRequests.post('/user/', data=register_data)

            Assertions.assert_code_status(response1, 200)
            Assertions.asser_json_has_key(response1, "id")

            self.email = register_data['email']
            self.first_name = register_data['firstName']
            self.password = register_data['password']
            self.user_id = self.get_json_value(response1, 'id')

        with allure.step('Login new user'):
            login_data = {
                'email': self.email,
                'password': self.password
            }
            response2 = MyRequests.post("/user/login", data=login_data)

            self.auth_sid = self.get_cookie(response2, 'auth_sid')
            self.token = self.get_header(response2, 'x-csrf-token')

    @allure.description('Edit just creates user. Change first name')
    def test_edit_just_creates_user(self):

        with allure.step('Edit user name'):

            response3 = MyRequests.put(f"/user/{self.user_id}",
                                     headers={'x-csrf-token': self.token},
                                     cookies={'auth_sid': self.auth_sid},
                                     data={'firstName': self.new_name})

            Assertions.assert_code_status(response3, 200)

        with allure.step('Check changes'):
            response4 = MyRequests.get(f"/user/{self.user_id}",
                                     headers={'x-csrf-token': self.token},
                                     cookies={'auth_sid': self.auth_sid},
                                    )

            Assertions.assert_json_value_by_name(response4,
                                                 'firstName',
                                                 self.new_name,
                                                 "Wrong name after edit")

    @allure.description('Trying to change user data without authorization')
    def test_edit_user_without_auth(self):
        response = MyRequests.put(f"/user/{self.user_id}",
                                  data={'firstName': self.new_name})

        Assertions.assert_code_status(response, 400)
        Assertions.assert_contend_value(response, '{"error":"Auth token not supplied"}')

    @allure.description('Trying to change user data when authorization for another user')
    def test_edit_user_under_another_user(self):
        with allure.step("Register new user"):
            register_data = self.prepeare_registration_data()
            response1 = MyRequests.post('/user/', data=register_data)

            Assertions.assert_code_status(response1, 200)
            Assertions.asser_json_has_key(response1, "id")

            self.user_id_new = self.get_json_value(response1, 'id')
            self.email_new = register_data['email']
            self.first_name_new = register_data['firstName']
            self.password_new = register_data['password']

        with allure.step("Change data new user with token and sid another user"):
            response = MyRequests.put(f"/user/{self.user_id_new}",
                                       headers={'x-csrf-token': self.token},
                                       cookies={'auth_sid': self.auth_sid},
                                       data={'firstName': self.new_name})

            Assertions.assert_code_status(response, 200)

            with allure.step('Login new user'):
                login_data = {
                    'email': self.email_new,
                    'password': self.password_new
                }
                response2 = MyRequests.post("/user/login", data=login_data)

                self.auth_sid_new = self.get_cookie(response2, 'auth_sid')
                self.token_new = self.get_header(response2, 'x-csrf-token')

            with allure.step('Check data new user'):
                response3 = MyRequests.get(f"/user/{self.user_id_new}",
                                           headers={'x-csrf-token': self.token_new},
                                           cookies={'auth_sid': self.auth_sid_new},
                                           )

                Assertions.assert_json_value_by_name(response3,
                                                     'firstName',
                                                     self.first_name_new,
                                                     "Wrong name after edit")

    @allure.description('Change user data on incorrect email ')
    def test_edit_user_incorrect_email(self):
        incorrect_email = 'learnqa1xample.com'
        with allure.step('Edit user email'):
            response = MyRequests.put(f"/user/{self.user_id}",
                                       headers={'x-csrf-token': self.token},
                                       cookies={'auth_sid': self.auth_sid},
                                       data={'email': incorrect_email})

            Assertions.assert_code_status(response, 400)
            Assertions.assert_contend_value(response, '{"error":"Invalid email format"}')

    @allure.description('Change user first name on incorrect')
    def test_edit_user_incorrect_email(self):
        incorrect_firstName = 'l'
        with allure.step('Edit user firstName'):
            response = MyRequests.put(f"/user/{self.user_id}",
                                      headers={'x-csrf-token': self.token},
                                      cookies={'auth_sid': self.auth_sid},
                                      data={'firstName': incorrect_firstName})

            Assertions.assert_code_status(response, 400)
            Assertions.assert_contend_value(response, '{"error":"The value for field `firstName` is too short"}')









