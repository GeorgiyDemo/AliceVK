import yaml

def GetTokens():
    """
        Процедура для чтения токенов antigate и vk с файла yaml
    """
    with open("./tokens.yaml", 'r') as stream:
        tokens_dictionary = yaml.load(stream)
        return tokens_dictionary


