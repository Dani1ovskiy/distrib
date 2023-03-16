 select * 
   from bot.t_meetings a
   full outer join bot.temp_ttt_meetings b
     on a.usertgid = b.usertgid
	and a.uid = b.uid
 where a.usertgid is null
    or b.usertgid is null;

--У вас сегодня назначены следующие встречи:
 select * 
   from bot.t_meetings a
  where a.usertgid = 218714164
    and a.starttime::date = current_date;
--У вас начинается встреча XXX через 15 минут
 select to_char(a.starttime,'dd.mm hh24:mi') || ' - ' || a.summary,
        a.url,
		a.starttime
   from bot.temp_ttt_meetings a 
  where a.usertgid = 218714164 
    and a.starttime::date = current_date
	and 1 = 1
  order by a.starttime asc;

--У вас начинается встреча XXX сейчас
??

--У вас новая встреча XXX
 select b.* 
   from bot.t_meetings a
   full outer join bot.temp_ttt_meetings b
     on a.usertgid = b.usertgid
	and a.uid = b.uid
 where a.usertgid is null;

--Встреча XXX изменила время начала
 select a.* 
   from bot.t_meetings a
   full outer join bot.temp_ttt_meetings b
     on a.usertgid = b.usertgid
	and a.uid = b.uid
 where a.usertgid is not null
   and b.usertgid is not null
   and a.starttime != b.starttime;
	
--У вас отменилась встреча XXX
 select a.* 
   from bot.t_meetings a
   full outer join bot.temp_ttt_meetings b
     on a.usertgid = b.usertgid
	and a.uid = b.uid
 where b.usertgid is null;

