----'/absolute/path/to/directory-with-init-scripts':/docker-entrypoint-initdb.d 


CREATE SCHEMA bot
    AUTHORIZATION ctitpbotusr;





-- Table: bot.t_issue

DROP TABLE IF EXISTS bot.t_issue;

CREATE TABLE IF NOT EXISTS bot.t_issue
(
    id bigserial,
    project text,
    caseid bigint,
    updatedon date,
    assignedto text,
    priority text,
    url text
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS bot.t_issue
    OWNER to ctitpbotusr;
	
-- Table: bot.t_meetings

DROP TABLE IF EXISTS bot.t_meetings;

CREATE TABLE IF NOT EXISTS bot.t_meetings
(
    id bigserial,
	uid text,
	usertgid bigint,
	useremail text,
    starttime timestamp,
    summary text,
    descr text,
    url text,
    lastmodify timestamp,
	notif_morning integer default 0,
	notif_before15 integer default 0,
	notif_start integer default 0
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS bot.t_meetings
    OWNER to ctitpbotusr;
	
-- Table: bot.t_users

DROP TABLE IF EXISTS bot.t_users;

CREATE TABLE IF NOT EXISTS bot.t_users
(
    id bigserial,
    firstname text,
    lastname text,
    department text,
    phone text,
    email text,
    caldav text,
    caldavpass text,
    ical text,
    tgid bigint,
    notifycalendar integer,
    notifyissue integer
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS bot.t_users
    OWNER to ctitpbotusr;
	

INSERT INTO bot.t_users(
	firstname, lastname, department, phone, email, caldav, caldavpass, tgid, ical)
	VALUES 
('Даниловский Данила', 'Данила', 'Производство - L1', '+7 (989) 703-25-89', 'danilovskiy.d@ctitp.ru', 'https://caldav.yandex.ru/calendars/danilovskiy.d%40ctitp.ru/events-20022809/', 'okwghoogryeccxbl', 346573500, 'https://calendar.yandex.ru/export/ics.xml?private_token=9d2dbd13461f5deee01443ddbc3c207c83c5f084&tz_id=Europe/Moscow'),
('Кольцов Александр', 'Александр', 'Производство - L1', '+7 (988) 543-85-67', 'koltsov.a@ctitp.ru', '', '', null, null),
('Леонтьев Дмитрий', 'Дмитрий', 'Производство - L1', '+7 (988) 586-17-34', 'leontiev.d@ctitp.ru', '', '', null, null),
('Бессараб Михаил', 'Михаил', 'Производство - L2', '+7 (985) 410-89-81', 'bessarab.m@ctitp.ru', '', '', null, null),
('Гриднев Сергей', 'Сергей', 'Производство - L2', '+7 (995) 777-08-56', 'gridnev.s@ctitp.ru', '', '', null, null),
('Жаркова Любовь', 'Любовь', 'Производство - L2', '+7 (916) 332-81-66', 'zharkova.l@ctitp.ru', '', '', null, null),
('Китцель Виталий', 'Виталий', 'Производство - L2', '+7 (926) 901-41-71', 'kittsel.v@ctitp.ru', '', '', null, null),
('Осипатов Кирилл', 'Кирилл', 'Производство - L2', '+7 (968) 591-83-23', 'osipatov.k@ctitp.ru ', '', '', null, null),
('Сайфуллин Расиль', 'Расиль', 'Производство - L2', '+7 (926) 726-69-11', 'sayfullin.r@ctitp.ru', '', '', null, null),
('Самойлова Мария', 'Мария', 'Производство - L2', '+7 (915) 262-87-91', 'samoylova.m@ctitp.ru', '', '', null, null),
('Трошкин Василий', 'Василий', 'Производство - L2', '+7 (985) 776-50-13', 'troshkin.v@ctitp.ru', '', '', null, null),
('Даровских Светлана', 'Светлана', 'Продажи', '+7 (925) 150-54-56', 'darovskikh.s@ctitp.ru', '', '', null, null),
('Казарян Марина', 'Марина', 'Продажи', '+7 (985) 364-27-21', 'kazarian.m@ctitp.ru', '', '', null, null),
('Кулаков Алексей', 'Алексей', 'Продажи', '+7 (903) 726-82-70', 'kulakov.a@ctitp.ru', '', '', null, null),
('Максименко Валерия', 'Валерия', 'Продажи', '+7 (985) 226-78-63', 'maksimenko.v@ctitp.ru', '', '', null, null),
('Михайлов Григорий', 'Григорий', 'Продажи', '+7 (985) 922-72-49', 'gmikhaylov@ctitp.ru', '', '', null, null),
('Терещенко Ирина', 'Ирина', 'Продажи', '+7 (964) 579-36-71', 'tereshchenko.i@ctitp.ru', '', '', null, null),
('Баранов Роман', 'Роман', 'Управление', '+7 (926) 203-89-12', 'baranov.r@ctitp.ru', '', '', null, null),
('Баранова Мария', 'Мария', 'Управление', '+7 (968) 989-32-84', 'baranova.m@ctitp.ru', 'https://caldav.yandex.ru/calendars/baranova.m%40ctitp.ru/events-18753872/', 'lbrytwddgfatwvnr', 286411705, ''),
('Голубева Анастасия', 'Анастасия', 'Управление', '+7 (967) 125-11-25', 'golubeva.a@ctitp.ru', 'https://caldav.yandex.ru/calendars/golubeva.a%40ctitp.ru/events-19375089/', 'ghxjpvbshgmkimga', '451263955', 'https://calendar.yandex.ru/export/ics.xml?private_token=b3164e87636db27ae756446badcaa4624c83cd3a&tz_id=Europe/Moscow'),
('Жерневская Елена', 'Елена', 'Управление', '+7 (918) 502-04-16', 'jernevskaya.e@ctitp.ru', '', '', null, null),
('Клименков Александр', 'Александр', 'Управление', '+7 (926) 266-34-34', 'klimenkov.a@ctitp.ru', '', '', null, null),
('Мальцев Алексей', 'Алексей', 'Управление', '+7 (900) 123-45-82', 'maltsev.a@ctitp.ru', 'https://caldav.yandex.ru/calendars/maltsev.a%40ctitp.ru/events-19753766/', 'fofwbunmmfhaxgxu', 402431402, 'https://calendar.yandex.ru/export/ics.xml?private_token=90d229232bd61cc1f96b488b8e90c7e7e55fdd1e&tz_id=Europe/Moscow'),
('Полиров Дмитрий', 'Дмитрий', 'Управление', '+7 (916) 981-35-20', 'polirov.d@ctitp.ru', 'https://caldav.yandex.ru/calendars/polirov.d%40ctitp.ru/events-19645967/', 'qaqcdjpfdhaxlele', 218714164, 'https://calendar.yandex.ru/export/ics.xml?private_token=1b7045e10143310036584ad9a94fd29d07f39d98&tz_id=Europe/Moscow'),
('Телятников Филипп', 'Филипп', 'Управление', '+7 (967) 096-77-59', 'pt@ctitp.ru', '', '', null, null);


-- Table: bot.t_notifications

-- DROP TABLE IF EXISTS bot.t_notifications;

CREATE TABLE IF NOT EXISTS bot.t_notifications
(
    id bigserial,
    sendtime timestamp without time zone,
    iscomplete integer,
    usertgid bigint,
    message text,
	url text
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS bot.t_notifications
    OWNER to ctitpbotusr;


