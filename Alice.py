# -*- coding: utf-8 -*-
from pytils import numeral
import vk, time, datetime, json, requests, urllib3, dateutil.parser
from captcha_solver import CaptchaSolver

access_token = "vk_token"
antigate_token = "antigate_token"

#Основная конфигурация
session = vk.Session(access_token=access_token)
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
    '6':'17',
    '7':'26',
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

def requests_image(file_url):
	img_data = requests.get(file_url,verify=False).content
	with open('captcha.jpg', 'wb') as handler:
		handler.write(img_data)

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

birthday_all = get_bdate_chat()

#Счетчик до начала Нового Года 2019
a = '2018-09-01'.split('-')
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

	#Счетчик дней лета
	cc = bb-aa
	dd = int(str(cc).split()[0])+1
	#days = print_(numeral.choose_plural(int(dd), (u'день', u'дня', u'дней')))
	#left = print_(numeral.choose_plural(int(dd), (u'Остался', u'Осталось', u'Осталось')))

	#Названия чатиков
	chat_titles = {
	'1':'4ПКС-115 | '+str(dd)+' день учебы',
	'2':'IV Курс | '+str(dd)+' день учебы',
	'3':'III Курс | '+str(dd)+' день учебы',
	'4':'II Курс | '+str(dd)+' день учебы',
	'5':'2ПКС-117 | '+str(dd)+' день учебы',
    '6':'I Курс | '+str(dd)+' день учебы',
    '7':'3ПКС-116 '+str(dd)+' день учебы',
	}

	#Чекаем дни рождения
	if cur_hour == 6 and cur_minute == 58:
		dstring = str(cur_day)+'.'+str(cur_month)
		bufkey = get_key(birthday_all,dstring)
		if bufkey != None:
			bday_user = api.users.get(user_ids=bufkey,name_case="acc",v=APIVersion)[0]
			msg = 'Поздравляем *id'+str(bufkey) + "(" + bday_user['first_name']+' '+bday_user['last_name']+') '+bday_string
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
			except Exception as e:

				captcha_sid=vk.exceptions.VkAPIError.captcha_sid.__get__(e)
				captcha_url = vk.exceptions.VkAPIError.captcha_img.__get__(e)
				if (captcha_sid == None) and (captcha_url == None):
					time.sleep(3)
					api.messages.editChat(chat_id=conf_id,title=chat_titles[str(i+1)],v=APIVersion)
				requests_image(captcha_url)
				solver = CaptchaSolver('antigate', api_key=antigate_token)
				raw_data = open('captcha.jpg', 'rb').read()
				captcha_ready = solver.solve_captcha(raw_data)
				api.messages.editChat(chat_id=conf_id,title=chat_titles[str(i+1)],v=APIVersion,captcha_sid=captcha_sid,captcha_key=captcha_ready)
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
