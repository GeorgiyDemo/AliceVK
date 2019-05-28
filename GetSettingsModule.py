import yaml

def GetSettings():
    """
        Процедура для чтения настроек с файла yaml

        Включает в себя:
        - Токен от vk
        - Токен от antigate
        - Директорию со шрифтом для подстановки

    """
    with open("./tokens.yaml", 'r') as stream:
        tokens_dictionary = yaml.load(stream)
        return tokens_dictionary


