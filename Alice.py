import datetime
import time
from pytils import numeral
from pytils.third import six
import vk

import GetSettingsModule

# Основные параметры
# Версия VK API
API_VERSION = 5.73
SCRIPT_TIME_SLEEP = 4
CHAT_ID_DICT = {
    '1': '4',
    '2': '13',
    '3': '15',
    '4': '17',
    '5': '26',
    '6': '52',
    '7': '53',
    '8': '54',
}


class AliceClass(object):
    """
    Класс с основной логикой работы Алиски
    """

    def __init__(self):

        vk_token = GetSettingsModule.GetSettings()
        session = vk.Session(access_token=vk_token)
        self.api = vk.API(session)
        self.api_version = API_VERSION

        # Счетчик до 1 сентября
        a = '2019-09-01'.split('-')
        self.counter = datetime.date(int(a[0]), int(a[1]), int(a[2]))

        while True:
            self.processing_method()
            time.sleep(SCRIPT_TIME_SLEEP)

    def processing_method(self):

        # Счетчик дней лета
        cc = datetime.date.today() - self.counter
        dd = int(str(cc).split()[0]) + 1

        #left_days = self.word_formater(numeral.choose_plural(int(dd), (u'день', u'дня', u'дней')))
        #left_str = self.word_formater(numeral.choose_plural(int(dd), (u'Остался', u'Осталось', u'Осталось')))

        # Названия чатиков
        chat_titles = {
            '1': 'IV Курс | ' + str(dd) + " день учёбы",
            '2': 'III Курс | ' + str(dd) + " день учёбы",
            '3': '3ПКС-117 | '  + str(dd) + " день учёбы",
            '4': 'II Курс | ' + str(dd) + " день учёбы",
            '5': '4ПКС-116 | '  + str(dd) + " день учёбы",
            '6': 'I Курс | '  + str(dd) + " день учёбы",
            '7': 'FA | ' + str(dd) + " день учёбы",
            '8': 'ПМиИТ | '  + str(dd) + " день учёбы",
        }

        # Чекаем названия бесед
        for i in range(len(CHAT_ID_DICT)):
            time.sleep(0.5)
            conf_id = CHAT_ID_DICT[str(i + 1)]
            name_now = self.api.messages.getChat(chat_id=conf_id, v=self.api_version)['title']

            # Если надо, то меняем название
            if name_now != chat_titles[str(i + 1)]:
                try:
                    self.api.messages.editChat(chat_id=conf_id, title=chat_titles[str(i + 1)], v=self.api_version)
                except:
                    continue

    def word_formater(self, s):
        if six.PY3:
            out = s
        else:
            out = s.encode('UTF-8')
        return out


if __name__ == '__main__':
    AliceClass()
