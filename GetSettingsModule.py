import yaml


def GetSettings():
    """
        Процедура для чтения токена vk с файла yaml
    """
    with open("./token.yaml", "r") as stream:
        return yaml.safe_load(stream)
