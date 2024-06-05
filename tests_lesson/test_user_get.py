from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_reqests import MyRequests


class TestUserGet(BaseCase):
    def test_get_user_details_not_auth(self):
        response = MyRequests.get("/user/2")

        Assertions.asser_json_has_key(response, "username")
        Assertions.asser_json_has_not_key(response, "email")
        Assertions.asser_json_has_not_key(response, "firstName")
        Assertions.asser_json_has_not_key(response, "lastName")

    def test_get_user_details_auth_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, 'auth_sid')
        token = self.get_header(response1, 'x-csrf-token')
        user_id = self.get_json_value(response1, "user_id")

        response2 = MyRequests.get(f"/user/{user_id}", headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid})

        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.asser_json_has_keys(response2, expected_fields)


