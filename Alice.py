# -*- coding: utf-8 -*-
from pytils import numeral
import vk,random,time,datetime,os,json,requests,xlrd
session = vk.Session(access_token='token')
api = vk.API(session)
admin_id = '257350143'

#Настройка id конф
conversations= {
	'1':'2',
	'2':'3',
	'3':'4',
}
#Настройка аватарок в конфах
photoconf={
    '2':'./KIP/4.jpg',
    '3':'./KIP/2.jpg',
    '4':'./KIP/1.jpg',
}
#База ответов
base={
    '🐱':'Мур :3',
    'Доброе':'Доброе 🐱',
    'Жрать хочу':'Диктуй адрес',
    'Доброе утро':'Доброе)',
}

#Настройка лонгпула
longi = api.messages.getLongPollServer(use_ssl=0,need_pts=1)
ts = longi['ts']
pts = longi['pts']
wtf = longi['key']

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
        'clear':'Ясно',
        'cloudy':'Облачно',
        'overcast':'Пасмурно',
        'cloudy-and-rain':'Облачно, дождь',
        'partly-cloudy':'Облачная погода с прояснениями, переменная облачность',
        'cloudy-and-light-rain':'Облачно, возможны небольшие осадки',
        'overcast-and-light-rain':'Пасмурно, возможны небольшие осадки',
        'partly-cloudy-and-rain':'Частично облачно, дождь',
        'partly-cloudy-and-light-rain':'Частично облачно, возможны небольшие осадки',
        }

        try:
            smysol = super_translate[word]
            return smysol
        except:
            return word

    headers = {
    #Хедеры с Я.Погодки
    'X-Yandex-Weather-Device-ID': 'UUID',
    'X-Yandex-Weather-Token': 'token',
    'X-Yandex-Weather-Device': 'os=iPhone OS; os_version=9.0.2; manufacturer=Apple; model=iPad; device_id=ID; uuid=UUID"',
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

#Я это даже исправлять не хочу :P
def open_excel(path):
    i = 4

    welcome_message = '\nМои поздравления <3'
    
    router={
    'IBAS.xlsx':'http://www.fa.ru/projects/itcolledge/entrant/Documents/ИБАС%20(бюджет,%20к%20зачислению).xlsx',
    'PKS.xlsx':'http://www.fa.ru/projects/itcolledge/entrant/Documents/ПКС%20(бюджет,%20к%20зачислению).xlsx',
    }

    names={
    'IBAS.xlsx':'ИБАС',
    'PKS.xlsx':'ПКС',
    }

    dls = router[path]
    resp = requests.get(dls)
    output = open(path, 'wb')
    output.write(resp.content)
    output.close()

    book = xlrd.open_workbook(path)
    first_sheet = book.sheet_by_index(0)
    DATA = first_sheet.cell(0,0).value+' ('+names[path]+')\n\n'
    while i < 54:
        velosiped = (first_sheet.cell(i,1).value).split(' ', 2)[0]+' '+(first_sheet.cell(i,1).value).split(' ', 2)[1]
        DATA +=velosiped+'\n'
        i = i + 1

    DATA = DATA + welcome_message
    return DATA

#Счетчик дней до начала учебы
a = '2016-09-01'.split('-')
aa = datetime.date(int(a[0]),int(a[1]),int(a[2]))

while True:

	#Работа с временем/датой
    now_date = datetime.date.today()
    now_time = datetime.datetime.now()
    day = now_date.isoweekday()
    cur_hour = now_time.hour
    cur_minute = now_time.minute
    cur_second = now_time.second
    for_logs = str(now_time.hour)+':'+str(now_time.minute)+':'+str(now_time.second)
    bb = datetime.date.today()

    #Опять счетчик дней до начала учебы
    cc = aa-bb
    dd = int(str(cc).split()[0])+1

    #Работа с падежами числительных
    days =  print_(numeral.choose_plural(int(dd), (u'день', u'дня', u'дней')))
    left = print_(numeral.choose_plural(int(dd), (u'Остался', u'Осталось', u'Осталось')))

    #Названия чатиков
    chat_titles = {
    '1': '2ПКС-215 | '+left+' '+str(dd)+' '+ days,
    '2':'II Курс | '+left+' '+str(dd)+' '+ days,
    '3':'I Курс | '+left+' '+str(dd)+' '+ days,
    }

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

        elif message =='/ПКС':
            api.messages.send(chat_id=ok['messages'][1]['chat_id'],message='Секундочку..')
            api.messages.send(chat_id=ok['messages'][1]['chat_id'],message=open_excel('PKS.xlsx'))

        elif message =='/ИБАС':
            api.messages.send(chat_id=ok['messages'][1]['chat_id'],message='Секундочку..')
            api.messages.send(chat_id=ok['messages'][1]['chat_id'],message=open_excel('IBAS.xlsx'))

        elif message =='/weather' or message =='/погода':
            mess = get_weather()
            api.messages.send(chat_id=ok['messages'][1]['chat_id'],message=mess)

        elif message == 'uptime' and owner_id == admin_id:
        	up = os.popen('uptime').read()
        	api.messages.send(chat_id=ok['messages'][1]['chat_id'],message=str(up))

        elif changed == 'обновила фотографию беседы' or changed == 'обновил фотографию беседы' or changed == 'удалил фотографию беседы' or changed == 'удалила фотографию беседы':
            api.messages.send(chat_id=ok['messages'][1]['chat_id'],message='Ну и зачем?')
            try:
                photoresult = api.photos.getChatUploadServer(chat_id=ok['messages'][1]['chat_id'],crop_x=1,crop_y=1078,crop_width=1078)
                upload_url = photoresult['upload_url']
                img = {'photo': ('img.jpg', open(r''+photoconf[str(ok['messages'][1]['chat_id'])], 'rb'))}
                response = requests.post(upload_url, files=img).json()['response']
                time.sleep(2)
                api.messages.setChatPhoto(file=response)
            except:
                time.sleep(2)
    time.sleep(1)
