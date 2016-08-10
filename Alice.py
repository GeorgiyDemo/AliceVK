# -*- coding: utf-8 -*-
from pytils import numeral
import vk,random,time,datetime,os,json,requests,xlrd
session = vk.Session(access_token='token')
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
api = vk.API(session)
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

#Этот костыль надо нормально переписать
def open_excel(path):
	i = 5
	flag = 1

	router={
	'IBAS.xlsx':'http://www.fa.ru/projects/itcolledge/entrant/Documents/ИБАС%20бюджет.xlsx',
	'PKS.xlsx':'http://www.fa.ru/projects/itcolledge/entrant/Documents/ПКС%20бюджет.xlsx',
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
	while i < 55:
		velosiped = (first_sheet.cell(i,1).value).split(' ', 2)[0]+' '+(first_sheet.cell(i,1).value).split(' ', 2)[1]
		DATA +=str(flag)+' '+velosiped+' '+str(first_sheet.cell(i,2).value)+'\n'
		i = i + 1
		flag = flag + 1
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
        owner_id = str(ok['messages'][1]['uid'])

        if check_dict(message) != 0:
        	api.messages.send(chat_id=ok['messages'][1]['chat_id'],message=base[message])
        	time.sleep(1)

        elif message =='/ПКС' and owner_id != '13822995':
        	api.messages.send(chat_id=ok['messages'][1]['chat_id'],message='Секундочку..')
        	api.messages.send(chat_id=ok['messages'][1]['chat_id'],message=open_excel('PKS.xlsx'))

        elif message =='/ИБАС' and owner_id != '13822995':
        	api.messages.send(chat_id=ok['messages'][1]['chat_id'],message='Секундочку..')
        	api.messages.send(chat_id=ok['messages'][1]['chat_id'],message=open_excel('IBAS.xlsx'))

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