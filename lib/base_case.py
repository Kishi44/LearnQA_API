import json.decoder

from requests import Response

class BaseCase:
    @staticmethod
    def get_cookie(response: Response, cookie_name):
        assert cookie_name in response.cookies, f'There is no cookie with name {cookie_name} in the response'
        return response.cookies[cookie_name]

    @staticmethod
    def get_header(response: Response, headers_name):
        assert headers_name in response.headers, f'There is no headers with name {headers_name} in the response'
        return response.headers[headers_name]

    @staticmethod
    def get_json_value(response: Response, name):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f'Response is not in JSON format. Response text is "{response.text}"'

        assert name in response_as_dict, f"Response JSON doesn't have key '{name}'"

        return response.json()[name]