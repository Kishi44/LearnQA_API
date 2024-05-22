import requests
import pytest

class TestFirstAPI:
    names = [('Vi', 'Vi'),
              ('Ar', 'Ar'),
              ('', 'someone')
    ]

    @pytest.mark.parametrize('name, answer', names)
    def test_hello_call(self, name, answer):
        url = "https://playground.learnqa.ru/api/hello"
        data = {'name': name}

        response = requests.get(url, params=data)

        assert response.status_code == 200, "Wrong response code"

        response_dict = response.json()
        assert 'answer' in response_dict, 'There is no field "answer" in the response'

        expected_response_text = f"Hello, {answer}"
        actual_response_text = response_dict['answer']
        assert actual_response_text == expected_response_text, "The response is not correct"
