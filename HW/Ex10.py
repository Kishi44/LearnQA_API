class TestExample:
    def test_input_string(self):
        '''
        Проверяем длинну введеной фразы
        :return:
        '''
        user_text = input('Укажите слово не более 15 символов: ')
        user_text_len = len(user_text)
        assert user_text_len <= 15, f'Длина строки больше {user_text_len}'