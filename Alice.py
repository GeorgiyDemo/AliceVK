# -*- coding: utf-8 -*-
from pytils import numeral
import vk,random,time,datetime,os,json,requests,xlrd,schedule
session = vk.Session(access_token='token')
admin_id = '257350143'
DATA_PKS = 'ПКС котики :з'
DATA_IBAS = 'ИБАС няшки <3'
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

#Этот костыль мы переписали просто на 10/10
#Но пока только временное решение
def open_excel():
	global DATA_PKS
	global DATA_IBAS
	i = 5
	z = 6

	#Работаем с ПКС
	url_PKS = 'http://www.fa.ru/projects/itcolledge/entrant/Documents/ПКС%20бюджет.xlsx'
	resp = requests.get(url_PKS)
	output = open('PKS.xlsx', 'wb')
	output.write(resp.content)
	output.close()

	#Работаем с ИБАС
	url_IBAS = 'http://www.fa.ru/projects/itcolledge/entrant/Documents/ИБАС%20бюджет.xlsx'
	resp = requests.get(url_IBAS)
	output = open('IBAS.xlsx', 'wb')
	output.write(resp.content)
	output.close()

	#Парсим xlsx ПКС
	book = xlrd.open_workbook('PKS.xlsx')
	first_sheet = book.sheet_by_index(0)
	DATA_PKS = first_sheet.cell(0,0).value+' (ПКС)\n\n'
	while i < 55:
		velosiped = (first_sheet.cell(i,1).value).split(' ', 2)[0]+' '+(first_sheet.cell(i,1).value).split(' ', 2)[1]
		DATA_PKS +=str(i-4)+' '+velosiped+' '+str(first_sheet.cell(i,2).value)+'\n'
		i = i + 1

	#Парсим xlsx ИБАС
	book = xlrd.open_workbook('IBAS.xlsx')
	first_sheet = book.sheet_by_index(0)
	DATA_IBAS = first_sheet.cell(0,0).value+' (ИБАС)\n\n'
	while z < 55:
		velosiped = (first_sheet.cell(z,1).value).split(' ', 2)[0]+' '+(first_sheet.cell(z,1).value).split(' ', 2)[1]
		DATA_IBAS +=str(z-4)+' '+velosiped+' '+str(first_sheet.cell(z,2).value)+'\n'
		z = z + 1

#Счетчик дней до начала учебы
a = '2016-09-01'.split('-')
aa = datetime.date(int(a[0]),int(a[1]),int(a[2]))

schedule.every(10).minutes.do(open_excel)
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

    #Cron-подобная фигня
    schedule.run_pending()

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
        	api.messages.send(chat_id=ok['messages'][1]['chat_id'],message=DATA_PKS)

        elif message =='/ИБАС' and owner_id != '13822995':
        	api.messages.send(chat_id=ok['messages'][1]['chat_id'],message=DATA_IBAS)

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