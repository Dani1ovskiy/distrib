import config
#import requests
#import json
import time
import telebot
import random
#import base64
from telebot import types
#import smtplib
import pandas as pd
from telebot import types
from datetime import date
import re
import openai

v_phone = ''
v_lastname = ''
v_firstname = ''
v_step = ''

NUM_RE = re.compile(r".*(\d).*(\d).*(\d).*(\d).*(\d).*(\d).*(\d).*(\d).*(\d).*(\d).*")


bot = telebot.TeleBot(config.token)
users = [230946227,346573500]
hideBoard = types.ReplyKeyboardRemove()

file1 = '/usr/src/app/dockerdata/contact.xlsx'
xlsx = pd.ExcelFile(file1)
df1 = xlsx.parse('contact')

#file2 = '/usr/src/app/dockerdata/salarycalendar.xlsx'
#xlsx2 = pd.ExcelFile(file2)
#df2 = xlsx2.parse('calendar')


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
#

def userid_list():
    dff = pd.read_csv("/usr/src/app/dockerdata/ids.log", sep=";", header=0)
    dff = dff['ID']
    dff = dff.tolist()
    return dff
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
# help
# function to handle the /help command
@bot.message_handler(commands=['help'], func=lambda message: message.from_user.id in userid_list())
def fn_main_help(message):
    print('6' + ' | message.from_user.id = ' + str(message.from_user.id) + ' | message.chat.id = ' + str(message.chat.id) + ' | message.text = ' + str(message.text))
    bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(1)
    
    bot.send_message(message.chat.id, '\nВ моём арсенале есть следущее 🔽🔽🔽 \n/issues - Информация о заявках поддержки \n/contacts - Контакты команды \n/website - Ресурсы компании \n/calendar - Мои встречи \n/help - Помощь \n/wiki - База знаний \nА так же я с удовольствием отвечу на твои вопросы. Для этого просто напиши мне😊', reply_markup=hideBoard)
# start
# function to handle the /start command
@bot.message_handler(commands=['start'])
def fn_main_start(message):
    print('10' + ' | message.from_user.id = ' + str(message.from_user.id) + ' | message.chat.id = ' + str(message.chat.id) + ' | message.text = ' + str(message.text))
    mes = f'Привет. Я корпоративный бот компании ЦТИТП.'
    hello_mes = f'Теперь мне нужно проверить являешься ли ты сотрудником компании...'
    bot.send_message(message.chat.id,mes, parse_mode='html')
    time.sleep(2)
    bot.send_message(message.chat.id,hello_mes, parse_mode='html')
    time.sleep(2)
    phone_btn = telebot.types.ReplyKeyboardMarkup(True, True)
    phone_btn.add(types.KeyboardButton(text='Отправить контакт', request_contact=True))
    msg = bot.send_message(message.chat.id, 'Для этого нажми кнопку *Отправить контакт* 👇 ниже', parse_mode='Markdown',
                           reply_markup=phone_btn)
    bot.register_next_step_handler(msg, start_4)
    
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------

def start_4(message):
    time.sleep(1)    
    if (message.contact is not None and message.from_user.id == message.contact.user_id):
        bot.send_message(message.chat.id, 'Проверяю доступ ...', reply_markup=hideBoard)
        time.sleep(3)
        start_access(message, message.contact.phone_number)           
    else:
        bot.send_message(message.chat.id, 'Вы прислали не свой контакт 😈', reply_markup=hideBoard)
        
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
def start_access(message, phone):
    NUM_RE = re.compile(r".*(\d).*(\d).*(\d).*(\d).*(\d).*(\d).*(\d).*(\d).*(\d).*(\d).*")
    df1["Phone"] = df1["Phone"].apply(str)
    df1["Phone"] = df1["Phone"].apply(lambda x: "+7" + ''.join(NUM_RE.match(x).groups()))
    adf1 = df1["Phone"]
    adf1 = adf1.tolist()
    print(adf1)
    func=lambda phone: phone in adf1
    ph = lambda x: "+7" + ''.join(NUM_RE.match(x).groups())
    if not adf1:#(func(ph(phone))):
        bot.send_message(message.chat.id,'У Вас нет доступа или доступ запрещен😈', reply_markup=hideBoard)
    else:
        start_5(message, str(ph(phone)))
        
def start_5(message, phone):
    d1 = {'ID': [message.from_user.id], 'phone': [phone]}
    df = pd.DataFrame(d1)
    df.to_csv("/usr/src/app/dockerdata/ids.log", sep=";", mode='a', header=False)
    
    
    fileXLSX = '/usr/src/app/dockerdata/contact.xlsx'
    xlsx = pd.ExcelFile(fileXLSX)
    dfXLSX = xlsx.parse('contact')   
    NUM_RE = re.compile(r".*(\d).*(\d).*(\d).*(\d).*(\d).*(\d).*(\d).*(\d).*(\d).*(\d).*")
    idx = dfXLSX.index[dfXLSX['Phone'].apply(lambda x: "+7" + ''.join(NUM_RE.match(x).groups())) == phone].values[0]
    dfXLSX.at[idx, 'TgId'] = message.from_user.id
    dfXLSX.to_excel(xlsx, "contact", index=False)
    xlsx = pd.ExcelFile(fileXLSX)
    dfXLSX = xlsx.parse('contact')
    print(dfXLSX)
    
    bot.send_message(message.chat.id, 'Вы зарегистрированы в чатботе! \nУ меня есть следующие команды: \n/issues - Информация о заявках поддержки \n/contacts - Контакты команды \n/website - Ресурсы компании \n/calendar - Мои встречи \n/help - Помощь \n/wiki - База знаний \nА так же я с удовольствием отвечу на твои вопросы. Для этого просто напиши мне😊', reply_markup=hideBoard)
    
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
#
#
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
# help
# function to handle the /contact command
@bot.message_handler(commands=['contacts'], func=lambda message: message.from_user.id in userid_list())
def fn_main_contact(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton("✋ Отмена")
    markup.add(btn1)
    msg = bot.send_message(message.chat.id, "Умею искать по фамилии, e-mail, мобильному и рабочему телефону(+7 (98*)). Фамилию пиши в именительном падеже, а почту полностью 👇Например, Иванов или Ivanov@gp.ru", reply_markup=markup)
    bot.register_next_step_handler(msg, fn3, '', '', '')
        
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
def fn3(message, v_phone, v_firstname, v_lastname):
    if (message.text == "✋ Отмена"):
        bot.send_message(message.chat.id, 'Может быть в другой раз 😉', parse_mode='html', reply_markup=hideBoard)
    elif (message.text == "Сохранить контакт"):
        bot.send_contact(message.chat.id, phone_number=v_phone, first_name=v_firstname,last_name=v_lastname, reply_markup=hideBoard)
    elif (message.text == "Найти ещё"):
        fn_main_contact(message)
    elif (message.text == "Спасибо"):
        bot.send_message(message.chat.id, 'Обращайся 😊', parse_mode='html', reply_markup=hideBoard)
    elif (message.text == "Да"):
        fn_main_contact(message)
    else:
        fn_contact_find(message)
    #elif v_step == 2:
    #    fn_contact_find(message)
    #elif v_step == 1:
    #    bot.send_message(message.chat.id, 'Извини, я тебя не понял. Если что, у меня есть /help', parse_mode='html')
        
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
def fn_contact_find(message):
    markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton("Сохранить контакт")
    btn2 = types.KeyboardButton("Найти ещё")
    btn3 = types.KeyboardButton("Спасибо")
    markup1.add(btn1, btn2, btn3)

    markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn4 = types.KeyboardButton("Да")
    btn5 = types.KeyboardButton("✋ Отмена")
    markup2.add(btn4, btn5)

    f1 = ''
    flag = 0 # 1 - email 2 phone 3 Surname 4 Surname_eng
    mess = message.text.strip().lower()

    messphone = mess.replace("+", "").replace("(", "").replace(")", "").replace("-", "").replace(" ", "")

    v_phone = '' 
    v_lastname = ''
    v_firstname = ''
    
    #eng = re.compile(r"^[a-zA-Za]+$")

    if "@" in mess:
        flag = 1
        for i in df1['Email']:
            if i.lower().strip() == mess:
                f1 = i
    elif messphone.isdigit():
        NUM_RE = re.compile(r".*(\d).*(\d).*(\d).*(\d).*(\d).*(\d).*(\d).*(\d).*(\d).*(\d).*")
        ph = lambda x: "+7" + ''.join(NUM_RE.match(x).groups())
        messphone = ph(messphone)
        flag = 2
        for i in df1['Phone'].apply(str).apply(lambda x: "+7" + ''.join(NUM_RE.match(x).groups())):
            if i == messphone:
                f1 = i   
    elif 'а' <= mess <= 'я':
        flag = 3
        for i in df1['Surname']:
            if i.strip().lower() == mess:
                f1 = i
    elif 'a' <= mess <= 'z':
        flag = 4
        for i in df1['Surname_eng']:
            if i.strip().lower() == mess:
                f1 = i
    if f1 == '' and flag == 0:
        msg = bot.send_message(message.chat.id, f'Я не смог найти коллегу по запросу <b>{message.text}</b>. Запрос <b> {message.text}</b> не похож на email, телефон или фамилию – возможно закралась ошибка.💢 Попробуем еще раз?', parse_mode='html', reply_markup=markup2)
        bot.register_next_step_handler(msg, fn3, '', '', '')
    elif flag == 1 and f1 != '':
        m = ''
        d = df1[df1['Email'] == f1]
        for index, row in d.iterrows():
            v_phone =  str(row['Phone']).strip()
            v_lastname = str(row['Surname']).strip()
            v_firstname = str(row['Name']).strip()
            m += '\n\n' + str(row['Surname']).strip() + ' ' + str(row['Name']).strip() + '\n' + str(row['Department']).strip()  + '\n' + 'Мобильный: ' + str(row['Phone']).strip() + '\n' + 'E-mail: ' + str(row['Email']).strip() + '\n\n'
        msg = bot.send_message(message.chat.id, f'Я нашёл коллегу по <b>email</b>: {m} Попробуем еще раз? /contact', parse_mode='html', reply_markup=markup1)
        bot.register_next_step_handler(msg, fn3, v_phone, v_lastname, v_firstname)
    elif flag == 2 and f1 != '':
        NUM_RE = re.compile(r".*(\d).*(\d).*(\d).*(\d).*(\d).*(\d).*(\d).*(\d).*(\d).*(\d).*")
        m = ''
        d = df1[df1['Phone'].apply(str).apply(lambda x: "+7" + ''.join(NUM_RE.match(x).groups())) == f1]
        for index, row in d.iterrows():
            v_phone =  str(row['Phone']).strip()
            v_lastname = str(row['Surname']).strip()
            v_firstname = str(row['Name']).strip()
            m += '\n\n' + str(row['Surname']).strip() + ' ' + str(row['Name']).strip() + '\n' + str(row['Department']).strip()  + '\n' + 'Мобильный: ' + str(row['Phone']).strip() + '\n' + 'E-mail: ' + str(row['Email']).strip() + '\n\n'
        msg = bot.send_message(message.chat.id, f'Я нашёл коллегу по <b>номеру телефона</b>: {m} Попробуем еще раз? /contact', parse_mode='html', reply_markup=markup1)
        bot.register_next_step_handler(msg, fn3, v_phone, v_lastname, v_firstname)
    elif flag == 3 and f1 != '':
        m = ''
        d = df1[df1['Surname'] == f1]
        for index, row in d.iterrows():
            v_phone = str(row['Phone']).strip()
            v_lastname = str(row['Surname']).strip()
            v_firstname = str(row['Name']).strip()
            m += '\n\n' + str(row['Surname']).strip() + ' ' + str(row['Name']).strip() + '\n' + str(row['Department']).strip()  + '\n' + 'Мобильный: ' + str(row['Phone']).strip() + '\n' + 'E-mail: ' + str(row['Email']).strip() + '\n\n'
        msg = bot.send_message(message.chat.id, f'Я нашёл коллегу по <b>фамилии</b>: {m} Попробуем еще раз? /contact', parse_mode='html', reply_markup=markup1)
        bot.register_next_step_handler(msg, fn3, v_phone, v_lastname, v_firstname)
    elif flag == 4 and f1 != '':
        m = ''
        d = df1[df1['Surname_eng'] == f1]
        for index, row in d.iterrows():
            v_phone = str(row['Phone']).strip()
            v_lastname = str(row['Surname_eng']).strip()
            v_firstname = str(row['Name']).strip()
            m += '\n\n' + str(row['Surname_eng']).strip() + ' ' + str(row['Name']).strip() + '\n' + str(row['Department']).strip()  + '\n' + 'Мобильный: ' + str(row['Phone']).strip() + '\n' + 'E-mail: ' + str(row['Email']).strip() + '\n\n'
        msg = bot.send_message(message.chat.id, f'Я нашёл коллегу по <b>фамилии</b>: {m} Попробуем еще раз? /contact', parse_mode='html', reply_markup=markup1)
        bot.register_next_step_handler(msg, fn3, v_phone, v_lastname, v_firstname)
    #если не нашли по атрибуту
    elif flag == 1 and f1 == '':
        m = df1[df1['Email'] == f1]
        msg = bot.send_message(message.chat.id, f'Я не нашёл коллегу по <b>email</b> <b>{message.text}</b> из запроса. Попробуем еще раз?', parse_mode='html', reply_markup=markup2)
        bot.register_next_step_handler(msg, fn3, '', '', '')
    elif flag == 2 and f1 == '':
        m = df1[df1['Phone'] == f1]
        msg = bot.send_message(message.chat.id, f'Я не нашёл коллегу по <b>номеру телефона</b> <b>{message.text}</b> из запроса. Попробуем еще раз?', parse_mode='html', reply_markup=markup2)
        bot.register_next_step_handler(msg, fn3, '', '', '')
    elif flag == 3 and f1 == '':
        m = df1[df1['Surname'] == f1]
        msg = bot.send_message(message.chat.id, f'Я не нашёл коллегу по <b>фамилии</b> <b>{message.text}</b> из запроса. Попробуем еще раз?', parse_mode='html', reply_markup=markup2)
        bot.register_next_step_handler(msg, fn3, '', '', '')
    elif flag == 4 and f1 == '':
        m = df1[df1['Surname_eng'] == f1]
        msg = bot.send_message(message.chat.id, f'Я не нашёл коллегу по <b>фамилии</b> <b>{message.text}</b> из запроса. Попробуем еще раз?', parse_mode='html', reply_markup=markup2)
        bot.register_next_step_handler(msg, fn3, '', '', '')

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
#
#
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
# website
# function to handle the /website command
@bot.message_handler(commands=['website'], func=lambda message: message.from_user.id in userid_list())
def fn_main_website(message):
    markup1 = types.InlineKeyboardMarkup()
    markup1.add(types.InlineKeyboardButton("Перейти на ctitp.ru", url="https://ctitp.ru/"))
    bot.send_message(message.chat.id, "Сайт ctitp.ru", reply_markup=markup1)

    markup2 = types.InlineKeyboardMarkup()
    markup2.add(types.InlineKeyboardButton("Перейти на wiki", url="https://wiki.yandex.ru/"))
    bot.send_message(message.chat.id, "Вики", reply_markup=markup2)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
#
#
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
# calendar
# function to handle the /calendar command
@bot.message_handler(commands=['calendar'], func=lambda message: message.from_user.id in userid_list())
       
def fn_main_calendar(message):

    from datetime import datetime,timedelta
    import icalendar
    import recurring_ical_events
    import urllib.request
    
    
    file = '/usr/src/app/dockerdata/contact.xlsx'
    xlsx = pd.ExcelFile(file)
    df = xlsx.parse('contact')
    dd = df[df['TgId'] == message.from_user.id]
    for emp in dd.items():
        
        if emp == dd.empty:
            print('Вы не отправили настройки для доступа к календарю')
        else:
            print(emp)
            
    else:        
        url = dd['ICal'].values[0]       
        
    dict_url = {}
    dict_url["u"] = url
    get_url = dict_url.get('u')
    print(get_url)
    
    #Сегодня
    start_date = datetime.now()
    end_date =   date.today() + timedelta(days=1)
        
    ical_string = urllib.request.urlopen(get_url).read()
    calendar = icalendar.Calendar.from_ical(ical_string)
    events = recurring_ical_events.of(calendar).between(start_date, end_date)
    
    markup = types.InlineKeyboardMarkup()
    button_text = ''
    
    if events == []:
        bot.send_message(message.chat.id, "У вас нет встреч сегодня", parse_mode='html', reply_markup=hideBoard)
    else:
        
        for event in events:
            start = event["DTSTART"].dt
            summary = event["SUMMARY"]
            url = event["URL"]
            lastmodified = event["LAST-MODIFIED"].dt
            duration = event["DTEND"].dt - event["DTSTART"].dt
            #print("start {} summary {} url {} last-modified {}".format(start, summary, url, lastmodified))
            button_text = (start.strftime('%d.%m %H:%M') + ' - ' + event["DTEND"].dt.strftime('%H:%M') + '. ' + str(summary or 'Нет названия')).ljust(100, ' ')
            markup.add(types.InlineKeyboardButton(button_text, url=url)) 
        
        bot.send_message(message.chat.id, 'Ваши встречи на сегодня:', reply_markup=markup)
        
    #Завтра
    start_date = date.today() + timedelta(days=1)
    end_date =   date.today() + timedelta(days=2)


    ical_string = urllib.request.urlopen(get_url).read()
    calendar = icalendar.Calendar.from_ical(ical_string)
    events = recurring_ical_events.of(calendar).between(start_date, end_date)
    
    markup = types.InlineKeyboardMarkup()
    button_text = ''
    
    if events == []:
        bot.send_message(message.chat.id, "У вас нет встреч завтра", parse_mode='html', reply_markup=hideBoard)
    else:
    
        for event in events:
            start = event["DTSTART"].dt
            summary = event["SUMMARY"]
            url = event["URL"]
            lastmodified = event["LAST-MODIFIED"].dt
            duration = event["DTEND"].dt - event["DTSTART"].dt
            #print("start {} summary {} url {} last-modified {}".format(start, summary, url, lastmodified))
            button_text = (start.strftime('%d.%m %H:%M') + ' - ' + event["DTEND"].dt.strftime('%H:%M') + '. ' + str(summary or 'Нет названия')).ljust(100, ' ')
            markup.add(types.InlineKeyboardButton(button_text, url=url)) 
        
        bot.send_message(message.chat.id, 'Ваши встречи на завтра:', reply_markup=markup)
              
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
# issues
# function to handle the /issues command

@bot.message_handler(commands=['wiki'], func=lambda message: message.from_user.id in userid_list())
def fn_main_wiki(message):

    lists = [ 
        {
    'txt':'Регламент работы ЦТИТП с Заказчиками',
    'url':'https://disk.yandex.ru/i/u0BOtAEXHJONTw'
        },
        {
    'txt':'Бланк исходящего письма',
    'url':'https://disk.yandex.ru/i/JZjqY5WoYtxEQw'
        },
        {
    'txt':'Презентация ЦТИТП',
    'url':'https://disk.yandex.ru/i/Tdsa3hsGxEA_Xg'
        },
        {
    'txt':'Сертификат_доступ к обновлениям',
    'url':'https://disk.yandex.ru/i/yRvYl14axN3chw'
        },
        {
    'txt':'Сертификат_техническая поддержка SLA стандарт',
    'url':'https://disk.yandex.ru/i/hHsgHYBpgauG7g'
        },
        {
    'txt':'Акт на услуги_фиксированная ставка часа',
    'url':'https://disk.yandex.ru/i/RJ7V7OpVP7kB4Q'
        },
        {
    'txt':'Заявка на услуги_фиксированная ставка часа',
    'url':'https://disk.yandex.ru/i/Onq7GXvVtNtoDA'
        },
        {
    'txt':'ЦТИТП__рамочный договор услуг_фиксированная ставка часа',
    'url':'https://disk.yandex.ru/i/t5MJnIaEckcPtQ'
        },
        {
    'txt':'Инструкция по использованию кабинета технической поддержки клиента',
    'url':'https://disk.yandex.ru/i/6jX8rD-M6jsxRA'
        },
        {
    'txt':'Договор на услуги_абонентская ставка',
    'url':'https://disk.yandex.ru/i/372fjJiv7_tyhg'
        },
        {
    'txt':'Акт сдачи-приемки услуг_абонентская ставка',
    'url':'https://disk.yandex.ru/i/F58dKBgboE4SiQ'
        },
        {
    'txt':'Рамочный договор на услуги_заказы',
    'url':'https://disk.yandex.ru/i/dMg9tO5bvWX6Iw'
        },
        {
    'txt':'Заказ к рамочному договору на услуги',
    'url':'https://disk.yandex.ru/i/Hb90pjP5z0FuXg'
        },        
        {
    'txt':'Файлы пайплайн ',
    'url':'https://disk.yandex.ru/client/disk/CTITP/Файлы%20пайплайн'
        },
        {
    'txt':'Графические материалы компании',
    'url':'https://disk.yandex.ru/client/disk/CTITP/Документирование%20деятельности%20ЦТИТП/Графические%20материалы%20компании'
        },
        {
    'txt':'Шаблон договора на доступ к порталу',
    'url':'https://disk.yandex.ru/i/UXuauNf0_Wqa6w'
        },
        {
    'txt':'Презентация ЦТИТП',
    'url':'https://disk.yandex.ru/i/xLDtLgmBA4ORvg'
        },
        {
    'txt':'Сертификаты IBM',
    'url':'https://disk.yandex.ru/client/disk/CTITP_%D0%9F%D0%A0%D0%9E%D0%98%D0%97%D0%92%D0%9E%D0%94%D0%A1%D0%A2%D0%92%D0%9E/%D0%A1%D0%B5%D1%80%D1%82%D0%B8%D1%84%D0%B8%D0%BA%D0%B0%D1%82%D1%8B/IBM'
        },
        {
    'txt':'Другие сертификаты',
    'url':'https://disk.yandex.ru/client/disk/CTITP_%D0%9F%D0%A0%D0%9E%D0%98%D0%97%D0%92%D0%9E%D0%94%D0%A1%D0%A2%D0%92%D0%9E/%D0%A1%D0%B5%D1%80%D1%82%D0%B8%D1%84%D0%B8%D0%BA%D0%B0%D1%82%D1%8B/Other'
        },
    ]
    
    keyboard = types.InlineKeyboardMarkup()
    for list in lists:
        text = list.get("txt")
        url = list.get("url")
        btn = types.InlineKeyboardButton(text=text,url = url)
        keyboard.add(btn)
    bot.send_message(message.from_user.id, text='База знаний', reply_markup=keyboard)
        
    
    
# @bot.message_handler(commands=['statistics'], func=lambda message: message.from_user.id in userid_list())
# def fn_main_statistics(message):
    # from redminelib import Redmine
    # from datetime import datetime
    
    # bords = [
        
        # {
    # 'url':'https://service.labvs.ru/',
    # 'key':'e51dfcc1c8a8bcccdc3e4a4134bbc538bd304933'
        # },
        # {
    # 'url':'https://ets.dionaholding.ru/',
    # 'key':'796b684ed73b1a9d2d987002e79ba67bc54c7bff'
        # },
        # {
    # 'url':'https://support.ctitp.ru/',
    # 'key':'ea9b90a90862f8ea6cb30ffa578ba2315a57dfb1'
        # },
    # ]

    # for bord in bords:
        # url =bord.get("url")
        # key = bord.get("key")
        # redmine = Redmine(url=url,key = key)    
    
    
        # project = redmine.project.all()
        # for project in redmine.project.all():
        
            # project_name = project.name 
            # issues = redmine.issue.filter(project_id=project.identifier, status_id = '*', sort='id:asc')
            # issues_list = list(issues)
            # print(issues_list)
            
          
          
          
          
@bot.message_handler(commands=['push'], func=lambda message: message.from_user.id in userid_list())
def fn_push_menu(message):
    
    
    bords = [
    {
    'choose_yes':'Заявки поддержки',
    'choose_no':'Уведомления о встречах'
    }
   
    ]
    for bord in bords:
        choose_yes = bord.get('choose_yes')
        choose_no = bord.get('choose_no')
        yes = types.KeyboardButton(choose_yes)
        no = types.KeyboardButton(choose_no)
    
    file = '/usr/src/app/dockerdata/contact.xlsx'
    xlsx = pd.ExcelFile(file)
    df = xlsx.parse('contact')
    dd = df[df['TgId'] == message.from_user.id]
    for values in dd.items():
        push_call = dd['PushCall'].values[0]
        push_issue = dd['PushIssue'].values[0]
        
    push_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_yes = yes
    btn_no = no
    push_markup.add(btn_yes, btn_no)
    msg = bot.send_message(message.chat.id, 'Здесь ты сможешь выбрать о чём я буду тебя уведомлять 😊', reply_markup=push_markup)
    bot.register_next_step_handler(msg, fn_call_and_issue)
    
    
    
    
def fn_call_and_issue(message):
    if (message.text == 'Уведомления о встречах'):
        call_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        call_btn_yes = 'Подписаться✅'
        call_btn_no = 'Отписаться❌'
        call_markup.add(call_btn_yes,call_btn_no)
                         
        msg_call = bot.send_message(message.chat.id, 'Хотите ли вы получать уведомления о ваших встречах?', reply_markup = call_markup)        
        
        bot.register_next_step_handler(msg_call, fn_answer_call)
    elif (message.text == 'Заявки поддержки'):
        issue_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        issue_btn_yes = 'Подписаться✅'
        issue_btn_no = 'Отписаться❌'
        issue_markup.add(issue_btn_yes,issue_btn_no)
       
        msg_issue = bot.send_message(message.chat.id, 'Хотите ли вы получать уведомления c порталов поддержки?', reply_markup = issue_markup)   
        
        bot.register_next_step_handler(msg_issue, fn_answer_issue)
       
def fn_answer_call(message):
    
    if (message.text == 'Подписаться✅'):
        file = '/usr/src/app/dockerdata/contact.xlsx'
        xlsx = pd.ExcelFile(file)
        df = xlsx.parse('contact')
        dd = df.index[df['TgId'] == message.from_user.id].values[0]
        df.at[dd, 'PushCall'] = 1
        df.to_excel(xlsx, "contact", index=False)
        xlsx = pd.ExcelFile(file)
        df = xlsx.parse('contact')
        bot.send_message(message.chat.id, "Подписка оформлена✅", parse_mode='html', reply_markup=hideBoard)
    
    elif (message.text == 'Отписаться❌'):
        file = '/usr/src/app/dockerdata/contact.xlsx'
        xlsx = pd.ExcelFile(file)
        df = xlsx.parse('contact')
        dd = df.index[df['TgId'] == message.from_user.id].values[0]
        df.at[dd, 'PushCall'] = 0
        df.to_excel(xlsx, "contact", index=False)
        xlsx = pd.ExcelFile(file)
        df = xlsx.parse('contact')
        bot.send_message(message.chat.id, "Подписка отменена❌", parse_mode='html', reply_markup=hideBoard)

def fn_answer_issue(message):   
    if (message.text == 'Подписаться✅'):
        file = '/usr/src/app/dockerdata/contact.xlsx'
        xlsx = pd.ExcelFile(file)
        df = xlsx.parse('contact')
        dd = df.index[df['TgId'] == message.from_user.id].values[0]
        df.at[dd, 'PushIssue'] = 1
        df.to_excel(xlsx, "contact", index=False)
        xlsx = pd.ExcelFile(file)
        df = xlsx.parse('contact')
        bot.send_message(message.chat.id, "Подписка оформлена✅", parse_mode='html', reply_markup=hideBoard)
    
    elif (message.text == 'Отписаться❌'):
        file = '/usr/src/app/dockerdata/contact.xlsx'
        xlsx = pd.ExcelFile(file)
        df = xlsx.parse('contact')
        dd = df.index[df['TgId'] == message.from_user.id].values[0]
        df.at[dd, 'PushIssue'] = 0
        df.to_excel(xlsx, "contact", index=False)
        xlsx = pd.ExcelFile(file)
        df = xlsx.parse('contact')
        bot.send_message(message.chat.id, "Подписка отменена❌", parse_mode='html', reply_markup=hideBoard)
    

@bot.message_handler(commands=['issues'], func=lambda message: message.from_user.id in userid_list())
def fn_main_issues(message):
    from redminelib import Redmine
    from datetime import datetime
    
    bords = [
        
        {
    'url':'https://service.labvs.ru/',
    'key':'e51dfcc1c8a8bcccdc3e4a4134bbc538bd304933'
        },
        {
    'url':'https://ets.dionaholding.ru/',
    'key':'796b684ed73b1a9d2d987002e79ba67bc54c7bff'
        },
        {
    'url':'https://support.ctitp.ru/',
    'key':'ea9b90a90862f8ea6cb30ffa578ba2315a57dfb1'
        },
    ]

    for bord in bords:
        url =bord.get("url")
        key = bord.get("key")
        redmine = Redmine(url=url,key = key)    
        
        project = redmine.project.all()        
        current = datetime.now()
        try:       
            for project in redmine.project.all():
                if project.name == 'Техподдержка':
                    project_name = 'Техподдержка (Дубли для L1)'
                else:
                    project_name = project.name
                issues = redmine.issue.filter(project_id=project.identifier, sort='id:asc')
                issues_list = list(issues)
                number_of_elements = len(issues_list)
                if (not issues_list) or (project.name == 'Сопровождение'):
                    continue
                else:
                    markup = types.InlineKeyboardMarkup()
                    for case in issues:
                        case_id = str(case.id)
                        case_updated_on = case.updated_on
                        
                        update_date = case_updated_on.strftime("%d.%m.%Y. %H:%M")
                        case_assigned_to = str(case.assigned_to).replace(" (Технический инженер)", "")
                        case_priority = str(case.priority)
                        
                        if case_priority == '4 Низкий':
                            case_priority = '⚪'
                        elif case_priority == '3 Средний':
                            case_priority = '🟡'
                        elif case_priority == '2 Высокий':
                            case_priority = '🟠'
                        elif case_priority == '1 Критичный (только для прод)':
                            case_priority = '🔴'
                        else: case_priority = '⚫'
                      
                        diff = current - case_updated_on                    
                        
                        if diff.days >= 3:
                            diffmsg = ' - просрочена'
                        elif diff.days >= 2:
                            diffmsg = ' - истекает срок'
                        else:
                            diffmsg = ''
                        
                        button_text = case_priority + " № " + case_id + " " + case_assigned_to + diffmsg + " | Изм. " + str(update_date) 
                        
                        markup.add(types.InlineKeyboardButton(button_text, url=url + 'issues/' + str(case.id)))
                    bot.send_message(message.chat.id, str(project_name) + ''', Количество  открытых заявок - '''  + str(number_of_elements), reply_markup=markup)
                    time.sleep(1)
        except:
            bot.send_message(message.chat.id, "Портал {} не отвечает. Сообщение о недоступности портала отправлено в поддержку".format(url), parse_mode='html', reply_markup=hideBoard)
            pass
    bot.send_message(message.chat.id, '⚪️ - 4 Низкий\n🟡 - 3 Средний\n🟠 - 2 Высокий\n🔴 - 1 Критичный\n⚫️ - Приоритет не определен', parse_mode='html', reply_markup=hideBoard)
    

    
        
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
#
#
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
# other text
# function to handle the "other text"
@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    import openai
    
    openai.api_key = "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"

    #MODEL = "gpt-3.5-turbo"
    model_engine = "text-davinci-003"     
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=message.text,
        max_tokens=2024,
        temperature=0.5,
        n=1,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    
    
    
        
    #Chat    
    # response = openai.ChatCompletion.create(
        # model = MODEL,
        # messages=[
            # {"role": "system", "content": "Ты инженер первой линии поддержки, который распределяет заявки."},
            # {"role": "user", "content": "У меня есть два сотрудника. Сотрудник 1 знает IBM DB2, Сотрудник 2 знает Oracle DB.Ко мне приходит заявка по ошибке в PLSQL. Кому распределить данную заявку?"},
            # {"role": "assistant", "content": "Заявку необходимо распределить сотруднику 2, поскольку он знает Oracle DB. Поскольку PLSQL является языком программирования для Oracle, то сотрудник 2 будет наилучшим выбором для распределения заявки."},
            # {"role": "user", "content": "Сейчас пришла зявка с текстом select rownum, 1 from ... На кого назначить заявку?"}
        # ],
        # messages=[
        #     {"role": "system", "content": "Ты инженер первой линии поддержки, который распределяет заявки в зависимости от продукта заказчикаи его проблемы."},
        #     {"role": "system","name":"example_user", "content": "У меня есть два сотрудника. Сотрудник 1 знает IBM DB2, Сотрудник 2 знает Oracle DB.Ко мне приходит заявка по ошибке в PLSQL. Кому распределить данную заявку?"},
        #     {"role": "system","name":"example_assistant", "content": "Заявку необходимо распределить сотруднику 2, поскольку он знает Oracle DB. Поскольку PLSQL является языком программирования для Oracle, то сотрудник 2 будет наилучшим выбором для распределения заявки."},
        #     {"role": "system","name":"example_user", "content": "Сейчас пришла зявка с текстом: SELECT * FROM employees WHERE ROWNUM < 10;....Ошибка ora-01017...  На кого назначить заявку?"},
        #     {"role": "system","name":"example_assistant","content": "Так как ошибка ORA-01017 указывает на проблему с аутентификацией пользователя, то данную заявку необходимо назначить сотруднику, который специализируется на аутентификации и управлении пользователями в базе данных. Если в вашей команде есть такой сотрудник, то заявку следует ему назначить. Если же такого сотрудника нет, то заявку можно назначить сотруднику, который имеет опыт работы с ошибками базы данных и может помочь в поиске решения проблемы."},
        #     {"role": "system","name":"example_user", "content": "А сейчас пришла заявка по продукту IBM MQ, вот её текст:Добрый день!Наши коллеги выявили корреляцию объема трафика с началом накопления сообщений в трансмиссионной очереди, а именно - при достижении трафика больше 32мб\с появляются накопленияПросьба пояснить/подтвердить/опровергнуть данные выводы.Если это как-то регулируется конфигурацией менеджера/ОС/проч., просьба сообщить где именно."}
        # ],
        # messages = [
            # {"role":"system","content": "Ты обладаешь знаниями по  различным продуктам IBM и их версиям.Ты помогаешь людям устранять проблемы в продуктах IBM, очень подробно обясняя и используя термины."},
            # {"role":"user", "content": "Расскажи про продукты IBM и их версии"},
            # {"role":"assistant","content":"Могу рассказать тебе об одном из родуктов"} 
        # ],    
        # temperature = 0.5    
    # )

    output_completion = completion['choices'][0]['text']#['content'] ['text']['message']
    bot.send_message(message.chat.id, text = output_completion, reply_markup=hideBoard)
    
    print('1' + ' | ' + str(message.from_user.id) + ' | ' + str(message.chat.id) + ' | ' + str(message.text))
    
    func=lambda x: x in userid_list()
    if not(func(message.from_user.id)):
        fn_main_start(message)
    else:
        msgs_start = ['/start']
        msgs_wifi  = ['/wifi']
        msgs_help  = ['/help']
        msgs_thx   = ['Спасибо!', 'спасибо!', 'Спасибо', 'спасибо', 'Спс', 'cпс', 'thx', 'thanks', 'спасиб', 'пасиб']
        msgs_hello = ['Привет','привет','hi','hello','Здравствуй']
        ###bot.send_message(346573500, 'Ко мне обращается пользователь' + str(message.chat.id), reply_markup=hideBoard)
        if message.text in msgs_thx:
            print('7' + ' | ' + str(message.from_user.id) + ' | ' + str(message.chat.id) + ' | ' + str(message.text))
            rply_list = ['Пожалуйста', 'Рад стараться!😏 ', 'Пожалуйста 😇']
            random_index = random.randint(0, len(rply_list) - 1)
            bot.send_message(message.chat.id, rply_list[random_index], reply_markup=hideBoard)
        elif message.text in msgs_hello:
            print('19' + ' | ' +  str(message.from_user.id) + ' | ' + str(message.chat.id) + ' | ' + str(message.text))
            bot.send_message(message.chat.id, 'Привет!', reply_markup=hideBoard)
        # else:
            # print('8' + ' | ' + str(message.from_user.id) + ' | ' + str(message.chat.id) + ' | ' + str(message.text))
            # f = open('/usr/src/app/dockerdata/message_else_text.log', 'a')
            # f.write(message.text + '\n')
            # bot.send_message(message.chat.id, 'К сожалению, не понимаю Вас 😢', reply_markup=hideBoard)
        
if __name__ == '__main__':
    print('0' + ' | ' + str('Start TG BOT') + ' | ' + str(' ') + ' | ' + str(' '))  
    
    bot.infinity_polling()
    
    #append_df_to_excel(r'd:/temp/res.xlsx', df.iloc[5:7, 3:5] * 100, startrow=5+1, startcol=3+1, index=False, header=False)
                            
                            
    ##data_filtered.to_excel(writer, "Main", cols=['Diff1', 'Diff2'])
    

    
    ###d1 = {'ID': [message.from_user.id], 'phone': [phone]}
    ###df = pd.DataFrame(d1)
    ###df.to_csv("/usr/src/app/dockerdata/ids.log", sep=";", mode='a', header=False)
    ###bot.send_message(message.chat.id, 'Вы зарегистрированы в чатботе', reply_markup=hideBoard)
###-----------------------------------------------------------------------------------------------


