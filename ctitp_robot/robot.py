import config
import time
import telebot
from telebot import types
from datetime import date
import psycopg2
from psycopg2 import Error


#Каждую минуту поиск отличий!
def fn_find_diff():
    from datetime import datetime,timedelta
    import icalendar
    import recurring_ical_events
    import urllib.request
    step = ''
    print("--========================= fn_find_diff start ========================= --")
    start_date = datetime.now()
    print(start_date.hour)
    if 8 <= start_date.hour <= 23:
            connection = psycopg2.connect(user="ctitpbotusr",
                                        password="cti312874bxcmsr",
                                        host="ctitp_db_cntnr",
                                        port="5432",
                                        database="ctitpbot")
            
            cursor = connection.cursor()
            
            create_table_query = "create temp table temp_t_meetings as select * from bot.t_meetings where 1=0;"
            cursor.execute(create_table_query)
            
            #Сегодня
            start_date = date.today()
            end_date = date.today() + timedelta(days=1)
            step = 'step_0'
            
            cursor.execute("select * from bot.t_users where ical is not null and ical != '' and tgid is not null and tgid in (346573500,5065375376,500683099,783551643,402431402)")               
            records = cursor.fetchall()
            for row in records:
                try:
                    step = 'step_1'
                    print("--========================= user {} start ========================= --".format(row[1]))
                    markup = types.InlineKeyboardMarkup()
                    button_text = ''
                    #print(row[5], row[8], row[9])
                    username  = row[1]
                    useremail = row[5]
                    userical  = row[8]
                    usertgid  = row[9]
                    print(row[5], row[8], row[9])
                    print(usertgid)
                    
                    url = userical
                    
                    ical_string = urllib.request.urlopen(url).read()
                    calendar = icalendar.Calendar.from_ical(ical_string)
                    events = recurring_ical_events.of(calendar).between(start_date, end_date)
                    print(events)   
                    if events == []:
                        print('У вас нет встреч сегодня')
                    else:
                        step = 'step_1.1'
                        for event in events:
                            start = event["DTSTART"].dt
                            summary = event["SUMMARY"]
                            url = event["URL"]
                            uid = event["UID"]
                            lastmodified = event["LAST-MODIFIED"].dt
                            duration = event["DTEND"].dt - event["DTSTART"].dt
                            step = 'step_1.2'
                            insert_query = """ INSERT INTO temp_t_meetings(uid, usertgid, useremail, starttime, summary, descr, url, lastmodify) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
                            step = 'step_1.3'
                            descr = 'descr'
                            record_to_insert = (uid, usertgid, useremail, start, summary,descr, url, lastmodified)
                            step = 'step_1.4'
                            cursor.execute(insert_query, record_to_insert)
                        step = 'step_1.5'
                    #########################################################################################################
                    #Поиск новых встреч
                    print('-- ========================= ищу новые встречи user {} ========================= --'.format(username))
                    step = 'step_2'
                    cursor.execute(""" select to_char(b.starttime,'dd.mm hh24:mi') || ' - ' || b.summary, b.url
                       from bot.t_meetings a
                       full outer join temp_t_meetings b
                         on a.usertgid = b.usertgid
                        and a.uid = b.uid
                     where a.usertgid is null
                       and b.usertgid = %s
                       order by b.starttime asc;""", [usertgid])
                    rowcount = cursor.rowcount
                    
                    if rowcount > 0:
                        records = cursor.fetchall()
                        for row in records:
                            button_text = row[0]
                            button_url  = row[1]
                            markup.add(types.InlineKeyboardButton(button_text, url=button_url))
                        try:
                            bot.send_message(usertgid, 'У вас новые встречи на сегодня:', reply_markup=markup)
                        except telebot.apihelper.ApiTelegramException as e:
                            if e.description == "Forbidden: bot was blocked by the user":
                                print("Attention please! The user {} has blocked the bot. I can't send anything to them".format(usertgid))
                                print(username)
                            pass
                        except Exception as e:
                            print("Attention please! The user exception".format(usertgid))
                            print('|')
                            print(e)
                            print('|')
                            print(username)
                            pass
                        cursor.execute("""INSERT INTO bot.t_meetings(
                                            uid, usertgid, useremail, starttime, summary, descr, url, lastmodify, notif_morning)
                                        select b.uid, b.usertgid, b.useremail, b.starttime, b.summary, b.descr, b.url, b.lastmodify, 1::integer as notif_morning
                                                   from bot.t_meetings a
                                                   full outer join temp_t_meetings b
                                                     on a.usertgid = b.usertgid
                                                    and a.uid = b.uid
                                                 where a.usertgid is null
                                                 and b.usertgid = %s;""", [usertgid])
                    
                    #########################################################################################################
                    print('-- ========================= ищу перенесённые встречи user {} ========================= --'.format(username))
                    step = 'step_3'
                    cursor.execute(""" select to_char(a.starttime,'dd.mm hh24:mi') || ' - ' || a.summary || ' -> ' || to_char(b.starttime,'dd.mm hh24:mi'), a.url
                       from bot.t_meetings a
                       full outer join temp_t_meetings b
                         on a.usertgid = b.usertgid
                        and a.uid = b.uid
                     where b.usertgid is not null
                       and a.usertgid is not null
                       and a.starttime::date = current_date 
                       and a.starttime != b.starttime 
                       and a.usertgid = %s;""", [usertgid])
                    rowcount = cursor.rowcount
                    
                    if rowcount > 0:
                        records = cursor.fetchall()
                        for row in records:
                            button_text = row[0]
                            button_url  = row[1]
                            markup.add(types.InlineKeyboardButton(button_text, url=button_url))
                        try:
                            bot.send_message(usertgid, 'У вас перенеслись встречи:', reply_markup=markup)
                        except telebot.apihelper.ApiTelegramException as e:
                            if e.description == "Forbidden: bot was blocked by the user":
                                print("Attention please! The user {} has blocked the bot. I can't send anything to them".format(usertgid))
                                print(username)
                            pass
                        except Exception as e:
                            print("Attention please! The user exception".format(usertgid))
                            print('|')
                            print(e)
                            print('|')
                            print(username)
                            pass
                         
                        cursor.execute("""UPDATE bot.t_meetings as a SET starttime = b.starttime
                                            FROM temp_t_meetings as b
                                            WHERE b.usertgid = a.usertgid
                                            and a.uid = b.uid
                                            and a.starttime::date = current_date
                                            and a.starttime != b.starttime
                                            and a.usertgid = %s;""", [usertgid])
                        cursor.execute("""delete from bot.t_meetings
                                            WHERE usertgid = %s
                                            and starttime::date > current_date;""", [usertgid])
                    #########################################################################################################
                    print('-- ========================= ищу отменённые встречи user {} ========================= --'.format(username))
                    step = 'step_4'
                    cursor.execute(""" select to_char(a.starttime,'dd.mm hh24:mi') || ' - ' || a.summary, a.url
                       from bot.t_meetings a
                       full outer join temp_t_meetings b
                         on a.usertgid = b.usertgid
                        and a.uid = b.uid
                     where b.usertgid is null
                       and a.usertgid is not null
                       and a.starttime::date = current_date 
                       and a.usertgid = %s;""", [usertgid])
                    step = 'step_4.2'   
                    rowcount = cursor.rowcount
                    step = 'step_4.3'
                    print('rowcount')
                    print(rowcount)
                    
                    if rowcount > 0:
                        step = 'step_4.4'
                        records = cursor.fetchall()
                        step = 'step_4.5'
                        for row in records:
                            button_text = row[0]
                            button_url  = row[1]
                            markup.add(types.InlineKeyboardButton(button_text, url=button_url))
                        try:
                            bot.send_message(usertgid, 'У вас сегодня отменились встречи:', reply_markup=markup)
                        except telebot.apihelper.ApiTelegramException as e:
                            if e.description == "Forbidden: bot was blocked by the user":
                                print("Attention please! The user {} has blocked the bot. I can't send anything to them".format(usertgid))
                                print(username)
                            pass
                        except Exception as e:
                            print("Attention please! The user exception".format(usertgid))
                            print('|')
                            print(e)
                            print('|')
                            print(username)
                            pass
                        cursor.execute("""delete from bot.t_meetings
                                        where (t_meetings.uid, t_meetings.usertgid) in 
                                        (select a.uid, a.usertgid
                                            from bot.t_meetings a
                                            full outer join temp_t_meetings b
                                                on a.usertgid = b.usertgid
                                                and a.uid = b.uid
                                            where b.usertgid is null
                                            and a.usertgid is not null
                                            and a.starttime::date = current_date 
                                            and a.usertgid = %s)
                                        and t_meetings.starttime::date = current_date;""", [usertgid])
                    connection.commit()
                    #########################################################################################################
                    print("--========================= user {} end ========================= --".format(username))
                except Exception as e:
                    print('------Exception start-----------------------')
                    print("Attention please! The user exception".format(usertgid))
                    
                    print(e)
                   
                    print(username)
                    print(step)
                    connection.commit()
                    print('------Exception end-----------------------')
                    print("--========================= user {} end ========================= --".format(username))
                    pass
            
            connection.commit()
            connection.close()
    print("--========================= fn_find_diff end ========================= --")
bot = telebot.TeleBot(config.token)
hideBoard = types.ReplyKeyboardRemove()
        
if __name__ == '__main__':
    #print('0' + ' | ' + str('Start TG BOT #2') + ' | ' + str(' ') + ' | ' + str(' '))
    
    while True:     
        fn_find_diff()
        time.sleep(1)
    
 