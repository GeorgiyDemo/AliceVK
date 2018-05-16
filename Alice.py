# -*- coding: utf-8 -*-
from pytils import numeral
import vk, random, time, datetime, json, requests, urllib3
import dateutil.parser

#Основная конфигурация
session = vk.Session(access_token='token')
api = vk.API(session)
APIVersion = 5.73
bday_string = 'c Днём Рождения!\nУдачи тебе во всем, котиков и много-много сна!\n🐍'
chat_users_all={}
message_longpoll = [0]

#Настройка id конф
conversations= {
    '1':'14',
    '2':'3',
    '3':'4',
    '4':'13',
    '5':'15',
}

#База ответов
base={
    '🐱':'Мур :3',
    '🐍':'🐍🐍🐍',
    'Кусь':'кусь!!',
    'кусь':'кусь!!',
    'КУСЬ':'кусь!!',
    'Кусь!':'кусь!!1',
    'кусь!':'кусь!!1',
    'Доброе':'Доброе 🐱',
    'Жрать хочу':'Диктуй адрес, закажем пиццу',
    'все уроды':'Согласна',
    'Все уроды':'Согласна!',
    'Доброе утро':'Доброе)',
    'Опоздаю':'Щито поделать десу',
}

#Настройка лонгпула
server = None
key    = None
ts     = None

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

#Функция для получения ближайшей электрички между двумя станциями
def TrainsForVitya(station_from, station_to):
    urllib3.disable_warnings()
    headers = {

    #Хедеры для Я.Электричек
    'Host': 'export.rasp.yandex.net',
    'Accept-Language': 'ru',
    'User-Agent': '%D0%AF%D0%BD%D0%B4%D0%B5%D0%BA%D1%81%20%D0%AD%D0%BB%D0%B5%D0%BA%D1%82%D1%80%D0%B8%D1%87%D0%BA%D0%B8/3233 CFNetwork/758.0.2 Darwin/15.0.0',
    'Accept': '*/*'
    }

    my_json = requests.get('https://export.rasp.yandex.net/v3/suburban/search_on_date?date='+str(datetime.date.today())+'&days_ahead=1&lang=ru_RU&station_from='+str(station_from)+'&station_to='+str(station_to)+'&tomorrow_upto=3&transfers=auto',headers=headers, verify=False).json();
    segments = my_json["days"][0]["segments"]

    for i in range(len(segments)):

        segment_now = segments[i]
        dateformat = dateutil.parser.parse(segment_now["departure"]["time"], dayfirst=True)
        time_buf = dateformat.replace(tzinfo=None)-datetime.datetime.now().replace(tzinfo=None)
        datetime.timedelta(0, 8, 562000)
        minuts_count = (divmod(time_buf.days * 86400 + time_buf.seconds, 60))[0]
        if minuts_count > 0:
            return "Электричка " + segment_now["thread"]["title"] + " через "  +  str(minuts_count) + " мин, "+ str(segment_now["tariff"]["value"])+ " руб"

#Функция формирования словаря с днями рождений
def get_bdate_chat():

    birthday_dictionary={}

    for chat_id in range(len(conversations)):
        chat_user_arr=api.messages.getChat(chat_id=conversations[str(chat_id+1)],fields='bdate',v=APIVersion)['users']

        for i in range(len(chat_user_arr)):

            chat_users_all[chat_user_arr[i]['id']] = conversations[str(chat_id+1)]
            try:
                buf = chat_user_arr[i]['bdate'].split('.')
                new_date = str(buf[0])+'.'+str(buf[1])
                birthday_dictionary[chat_user_arr[i]['id']] = new_date
            except:
                birthday_dictionary[chat_user_arr[i]['id']] = 'NaN'

    return birthday_dictionary

################################################################
def remove_weather_message(message_id):
    api.messages.delete()
###############################################################

birthday_all = get_bdate_chat()

#Счетчик дней учебы
a = '2017-08-30'.split('-')
aa = datetime.date(int(a[0]),int(a[1]),int(a[2]))

while True:

	#Фикс лонпула по харду
	if server == None:
		cfg = api.messages.getLongPollServer(v=APIVersion)
		server = cfg['server']
		key = cfg['key']
		ts = cfg['ts']

	response = requests.post(
		"https://{server}?act=a_check&key={key}&ts={ts}&wait=25&mode={mode}&version=2".format(**{
			"server": server,
            "key": key,
            "ts": ts,
            "mode": 2
        }),
    timeout=30
   	).json()

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

	#Счетчик
	cc = bb-aa
	dd = int(str(cc).split()[0])

	#Названия чатиков
	chat_titles = {
	'1': '3ПКС-115 | '+str(dd)+' день учебы',
	'2':'III Курс | '+str(dd)+' день учебы',
	'3':'II Курс | '+str(dd)+' день учебы',
	'4':'I Курс | '+str(dd)+' день учебы',
	'5':'1ПКС-117 | '+str(dd)+' день учебы',
	}

    #Чекаем дни рождения
	if cur_hour == 6 and cur_minute == 58:
		dstring = str(cur_day)+'.'+str(cur_month)
		bufkey = get_key(birthday_all,dstring)
		if bufkey != None:
			bday_user = api.users.get(user_ids=bufkey,name_case="acc",v=APIVersion)[0]
			msg = 'Поздравляем '+bday_user['first_name']+' '+bday_user['last_name']+' '+bday_string
			api.messages.send(chat_id=chat_users_all[bufkey],message=msg,v=APIVersion)
		time.sleep(120)

    #Чекаем названия бесед
	for i in range(len(conversations)):
		time.sleep(0.5)
		conf_id = conversations[str(i+1)]
		name_now = api.messages.getChat(chat_id=conf_id,v=APIVersion)
		check = name_now['title']

        #Если надо, то меняем название
		if check != chat_titles[str(i+1)]:
			try:
				api.messages.editChat(chat_id=conf_id,title=chat_titles[str(i+1)],v=APIVersion)
				print('['+for_logs+'] Изменили название беседы №'+str(i+1)+' c "'+check+'" на "'+chat_titles[str(i+1)]+'"')
			except:
				print('['+for_logs+'] (!) Что-то пошло не так при смене названия беседы №'+str(i+1))


	checker = False

	for i in range(len(response['updates'])):
		if checker != True:
			try:

				message_longpoll = response['updates'][i][5]
				chat_longpoll = response['updates'][i][3]-2000000000
				checker = True

			except:
				pass
	if checker == False:
		message_longpoll = [0]
		chat_longpoll = [0]

	ts = response['ts']

    #Чекаем входящие сообщения
	if message_longpoll != [0]:

		if check_dict(message_longpoll) != 0:
			api.messages.send(chat_id=chat_longpoll,message=base[message_longpoll],v=APIVersion)

		elif message_longpoll =='/weather' or message_longpoll =='/погода':
			mess = get_weather()
			api.messages.send(chat_id=chat_longpoll,message=mess,v=APIVersion)

		elif message_longpoll =='/электрички' or message_longpoll =='/train':
			if cur_hour < 13:
				mess = TrainsForVitya(237007,195506)
			else:
				mess = TrainsForVitya(195506,237007)
			api.messages.send(chat_id=chat_longpoll,message=mess,v=APIVersion)
