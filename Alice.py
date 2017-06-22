# -*- coding: utf-8 -*-
from pytils import numeral
import vk, random, time, datetime, os, json, requests
session = vk.Session(access_token='token')
api = vk.API(session)
admin_id = '257350143'
bday_string = 'c Днём Рождения!\nУдачи тебе на сессии, котиков и много-много сна!\n🐍'

#Настройка id конф
conversations= {
    '1':'11',
    '2':'3',
    '3':'4',
}

#База ответов
base={
    '🐱':'Мур :3',
    'Доброе':'Доброе 🐱',
    'Жрать хочу':'Диктуй адрес, закажем пиццу',
    'все уроды':'Согласна',
    'Все уроды':'Согласна!',
    'Доброе утро':'Доброе)',
    'Опоздаю':'Щито поделать десу',
}

#Настройка лонгпула
longi = api.messages.getLongPollServer(use_ssl=0,need_pts=1)
ts = longi['ts']
pts = longi['pts']
wtf = longi['key']


def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k

def check_dict(word):
    try:
        bike = base[word]
        return bike
    except:
        return 0

def print_(s):
	from pytils.third import six
	if six.PY3:
		out = s
	else:
		out = s.encode('UTF-8')
	return(out)		

#Погодка
def get_weather():

    def translate(word):

        super_translate ={

        "clear": "Ясно",
        "mostly-clear": "Малооблачно",
        "partly-cloudy": "Малооблачно",
        "overcast": "Пасмурно",
        "partly-cloudy-and-light-rain": "Небольшой дождь",
        "partly-cloudy-and-rain": "Дождь",
        "overcast-and-rain": "Сильный дождь",
        "overcast-thunderstorms-with-rain": "Сильный дождь, гроза",
        "cloudy": "Облачно с прояснениями",
        "cloudy-and-light-rain": "Небольшой дождь",
        "overcast-and-light-rain": "Небольшой дождь",
        "cloudy-and-rain": "Дождь",
        "overcast-and-wet-snow": "Дождь со снегом",
        "partly-cloudy-and-light-snow": "Небольшой снег",
        "partly-cloudy-and-snow": "Снег",
        "overcast-and-snow": "Снегопад",
        "cloudy-and-light-snow": "Небольшой снег",
        "overcast-and-light-snow": "Небольшой снег",
        "cloudy-and-snow": "Снег",
        "full-moon": "Полнолуние",
        "decreasing-moon": "Убывающая луна",
        "last-quarter": "Последняя четверть",
        "new-moon": "Новолуние",
        "growing-moon": "Растущая луна",
        "first-quarter": "Первая четверть",
    
        }

        try:
            smysol = super_translate[word]
            return smysol
        except:
            return word

    headers = {
    #Хедеры с Я.Погодки
    'X-Yandex-Weather-Device-ID': 'Device-ID',
    'X-Yandex-Weather-Token': 'Token',
    'X-Yandex-Weather-Device': 'os=iPhone OS; os_version=9.0.2; manufacturer=Apple; model=iPad; device_id=Device-ID; uuid=uuid"',
    'X-Yandex-Weather-Client': 'YandexWeatherIOS/2051',
    'X-Yandex-Weather-UUID': 'UUID',
    'X-Yandex-Weather-Timestamp': '1471287200'
    }

    my_json = requests.get('https://api.weather.yandex.ru/v1/forecast?ext_kind=weather&lang=ru_RU&geoid=213',headers=headers).json()
    sunrise = my_json['forecasts'][0]['sunrise']
    sunset = my_json['forecasts'][0]['sunset']
    parts = my_json['forecasts'][0]['parts']
    city = my_json['geo_object']['province']['name']

    now = my_json['fact']
    temp = str(now['temp'])+'°C'
    feels = str(now['feels_like'])+'°C'
    wind_speed = str(now['wind_speed'])+' м/с'
    humidity = str(now['humidity'])+'%'
    pressure_mm = str(now['pressure_mm'])+' мм рт. ст.'
    morning = str(parts['morning']['temp_avg'])+'°C'
    day = str(parts['day']['temp_avg'])+'°C'
    evening = str(parts['evening']['temp_avg'])+'°C'
    description = translate(now['condition'])
    formatting_parts = '\nУтро: '+morning+'\nДень: '+day+'\nВечер: '+evening
    formatting_set = '\nВосход: '+sunrise+'\nЗакат: ' +sunset
    out = city+'\n'+description+'\nСейчас: '+temp+'\nПо ощущениям: '+feels+'\nСкорость ветра: '+wind_speed+'\nВлажность: '+humidity+'\nДавление: '+pressure_mm+'\n'+formatting_parts+'\n'+formatting_set

    return out

#Функция формирования словаря с днями рождений
def get_bdate_chat(chat_id):
	birthday_dictionary={}
	chat_user_arr=api.messages.getChat(chat_id=conversations[chat_id],fields='bdate')['users']
	for i in range(len(chat_user_arr)):
		try:
			buf = chat_user_arr[i]['bdate'].split('.')
			new_date = str(buf[0])+'.'+str(buf[1])
			birthday_dictionary[chat_user_arr[i]['uid']] = new_date
		except:
			birthday_dictionary[chat_user_arr[i]['uid']] = 'NaN'
	return birthday_dictionary

birthday_k2 = get_bdate_chat(str(2))

#Счетчик дней до летней сессии 
#a = '2017-06-22'.split('-')
#aa = datetime.date(int(a[0]),int(a[1]),int(a[2]))

while True:

    #Работа с временем/датой
    now_date = datetime.date.today()
    now_time = datetime.datetime.now()
    day = now_date.isoweekday()
    cur_hour = now_time.hour
    cur_minute = now_time.minute
    cur_second = now_time.second
    cur_month = now_date.month
    cur_day = now_date.day
    for_logs = str(now_time.hour)+':'+str(now_time.minute)+':'+str(now_time.second)
    bb = datetime.date.today()

    #Счетчик дней учебы
    #cc = aa-bb
    #dd = int(str(cc).split()[0])

    #Работа с падежами числительных
    #days =  print_(numeral.choose_plural(int(dd), (u'день', u'дня', u'дней')))

    #Названия чатиков
    chat_titles = {
    '1': '2ПКС-115 | Сессия',
    '2':'II Курс | Сессия',
    '3':'I Курс | Сессия',
    }

    #Чекаем дни рождения
    if cur_hour == 6 and cur_minute == 58:
    	dstring = str(cur_day)+'.'+str(cur_month)
    	bufkey = get_key(birthday_k2,dstring)
    	if bufkey != None:
    		bday_user = api.users.get(user_ids=bufkey)[0]
    		msg = 'Поздравляем '+bday_user['first_name']+' '+bday_user['last_name']+' '+bday_string
    		api.messages.send(chat_id=conversations['2'],message=msg)
    	time.sleep(120)

    #Чекаем названия бесед
    for i in range(len(conversations)):
        time.sleep(1)
        conf_id = conversations[str(i+1)]
        name_now = api.messages.getChat(chat_id=conf_id)
        check = name_now['title']

        #Если надо, то меняем название
        if check != chat_titles[str(i+1)]:
            try:
                api.messages.editChat(chat_id=conf_id,title=chat_titles[str(i+1)])
                print('['+for_logs+'] Изменили название беседы №'+str(i+1)+' c "'+check+'" на "'+chat_titles[str(i+1)]+'"')
            except:
                print('['+for_logs+'] (!) Что-то пошло не так при смене названия беседы №'+str(i+1))
    
    ok = api.messages.getLongPollHistory(ts=ts,pts=pts,preview_length=0)
    pts= ok['new_pts']

    #Чекаем входящие сообщения
    if ok['messages'] != [0]:
        try:
            changed = ok['messages'][1]['body'].partition(' ')[2].partition(' ')[2]
        except:
            changed = '0'
        message = str(ok['messages'][1]['body'])
        owner_id = str(ok['messages'][1]['uid'])

        if check_dict(message) != 0:
            api.messages.send(chat_id=ok['messages'][1]['chat_id'],message=base[message])
            time.sleep(1)

        elif message =='/weather' or message =='/погода':
            mess = get_weather()
            api.messages.send(chat_id=ok['messages'][1]['chat_id'],message=mess)

        elif message == 'uptime' and owner_id == admin_id:
            up = os.popen('uptime').read()
            api.messages.send(chat_id=ok['messages'][1]['chat_id'],message=str(up))

    time.sleep(1.5)