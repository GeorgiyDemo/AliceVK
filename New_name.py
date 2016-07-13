# -*- coding: utf-8 -*-
from pytils import numeral
import vk,random,time,datetime,json,forecastio,requests,base64
session = vk.Session(access_token=base64.b64decode(token).decode('utf-8'))
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
api = vk.API(session)
longi = api.messages.getLongPollServer(use_ssl=0,need_pts=1)
ts = longi['ts']
pts = longi['pts']
wtf = longi['key']

def print_(s):
    from pytils.third import six
    if six.PY3:
        out = s
    else:
        out = s.encode('UTF-8')
    return(out)

#Поездка в СПБ 15.07.2016
spb = '2016-07-15'.split('-')
spb_ok = datetime.date(int(spb[0]),int(spb[1]),int(spb[2]))

#Счетчик дней лета
a = '2016-06-01'.split('-')
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

    #Поездка в СПБ 15.07.2016
    myspb = spb_ok-bb
    Saint_P = int(str(myspb).split()[0])
    FuckRussian =  print_(numeral.choose_plural(int(Saint_P), (u'день', u'дня', u'дней')))

    #Счетчик дней лета
    cc = bb-aa
    dd = int(str(cc).split()[0])+1

    #Названия чатиков
    chat_titles = {
    '1': '2ПКС-215 | '+str(dd)+' день лета',
    '2':'II Курс | '+str(dd)+' день лета',
    '3':'I Курс | '+str(dd)+' день лета',
    }

    if now_time.hour == 6 and now_time.minute == 58:
    	print('['+for_logs+'] Пишем сообщение Деме..')
    	SMS = 'Доброе утро, мур 🐱\nНаступает '+str(dd)+' день лета\nДо поездки Демы в Санкт-Петербург осталось лишь '+str(Saint_P)+ ' '+FuckRussian+'\n'
    	time.sleep(180)
    	try:
    		api.messages.send(user_ids='257350143',message=SMS)
    		print('['+for_logs+'] Отправили сообщение Деме')
    	except:
    		print('['+for_logs+'] (!) Что-то пошло не так при отправке сообщения Деме')

    for i in range(len(conversations)):
    	time.sleep(1)
    	conf_id = conversations[str(i+1)]
    	name_now = api.messages.getChat(chat_id=conf_id)
    	check = name_now['title']
    	if check != chat_titles[str(i+1)]:
    		try:
    			api.messages.editChat(chat_id=conf_id,title=chat_titles[str(i+1)])
    			print('['+for_logs+'] Изменили название беседы №'+str(i+1)+' c "'+check+'" на "'+chat_titles[str(i+1)]+'"')
    		except:
    			print('['+for_logs+'] (!) Что-то пошло не так при смене названия беседы №'+str(i+1))
    
    ok = api.messages.getLongPollHistory(ts=ts,pts=pts,preview_length=0)
    pts= ok['new_pts']
    if ok['messages'] != [0]:
        try:
            changed = ok['messages'][1]['body'].partition(' ')[2].partition(' ')[2]
        except:
            changed = '0'
        #пишем чо хотим
        message = str(ok['messages'][1]['body'])
        if message == 'Доброе' or message == 'Доброе утро' or message == '🐱' or message == 'Жрать хочу':
            api.messages.send(chat_id=ok['messages'][1]['chat_id'],message=base[message])
            time.sleep(1)

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



    