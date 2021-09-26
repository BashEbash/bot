import telebot
from telebot import types
import os
import pymssql
import queue
import pickle
import yadisk

y = yadisk.YaDisk(token="AQAAAABXH-1JAAdmYN2iytj6skTGoCH2rFS_DA4")
token = '1831498169:AAF98sMy_R_LcjLZb9GEhXWeiAuaEVriPgI'
bot = telebot.TeleBot(token)

messages_russian = ['Давай тебя зарегистрируем, введи свое имя',  # 0
                    'Сколько тебе лет?',  # 1
                    'Где ты живешь?(Город)',  # 2
                    'Расскажи что нибудь о себе, или кого хочешь найти.(Хобби, подругу и тд.)',  # 3
                    'Пришли свое фото',  # 4
                    'Женский',  # 5
                    'Мужской',  # 6
                    'Введи свой пол',  # 7
                    'Кого ты ищешь?',  # 8
                    'Женщина',  # 9
                    'Мужчина',  # 10
                    'Имя: ',  # 11
                    'Возраст: ',  # 12
                    'Город: ',  # 13
                    'Описание: ',  # 14
                    'Да',  # 15
                    'Нет, изменить данные',  # 16
                    'Всё правильно?',  # 17
                    'Ладно, введём данные ещё раз, введи своё имя',  # 18
                    'Пришли фотографию!',  # 19
                    'Введи число!',  # 20
                    'Вижу ты уже зарегистрирован, не желаешь приступить к просмотру анкет?',  # 21
                    'Хочешь начать просмотр анкет?',  # 22
                    'Да',  # 23
                    'Не хочу смотреть анкеты']  # 24

# date_buttons = ['❤', '❌', '⛔', '1. ', '2. ']
date_buttons = ['1', '2', '3', '1. ', '2. ']

#connection = pymssql.connect(server='mssql-2017.labs.wmi.amu.edu.pl', user='dbad_s464866', password='d104t2Y75N',
    #                         database='dbad_s464866')

#cursor = connection.cursor()

class User(object):
    def __init__(self, language, chat_id, username, name, age, city, description, photo, sex, find_sex, status):
        self.language = language
        self.chat_id = chat_id
        self.username = username
        self.name = name
        self.age = age
        self.city = city
        self.description = description
        self.photo = photo
        self.sex = sex
        self.find_sex = find_sex
        self.status = status
    def set_atribute(self, atribute, change):
        self.__dict__[atribute] = change


def user_exists(chat_id):
    return os.path.exists(str(chat_id))


def add_user(chat_id, user_atr):
    users = dict()
    user = User(user_atr[0], user_atr[1], user_atr[2],
                user_atr[3], user_atr[4], user_atr[5],
                user_atr[6], user_atr[7], user_atr[8],
                user_atr[9], "register")
    users.update(chat_id = user)
    with open('users', "wb") as file:
        pickle.dump(users, file)
    print(f"user {chat_id} succefully added")


def get_user(chat_id):
    with open('users', "rb") as file:
        users = pickle.load(file)
    user = users[chat_id]
    print(f"user {chat_id} get succefully")
    return user


def get_from_db1(querry, stage):
    if stage == 1:
        q = queue.Queue()
        print(querry)
        cursor.execute(querry)
        # connection.commit()
        row = cursor.fetchone()
        # print(row[0])
        while row:
            q.put(row[0])
            row = cursor.fetchone()
        return q
    elif stage == 2:
        cursor.execute(querry)
        row = cursor.fetchone()

        return row


def set_atribute(atribute, change, chat_id):
    with open('users', "rb") as file:
        users = pickle.load(file)
    users[chat_id].set_attribute(atribute, change)
    with open('users', "wb") as file:
        pickle.dump(users, file)

def get_atribute(atribute, chat_id):
    with open('users', "rb") as file:
        users = pickle.load(file)
    return users[chat_id].__getattribute__(atribute)


def start_dates(message, lang_messages, mode):
    try:
        if message.text == lang_messages[23]:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button1 = types.KeyboardButton(date_buttons[0])
            button2 = types.KeyboardButton(date_buttons[1])
            button3 = types.KeyboardButton(date_buttons[2])
            markup.add(button1, button2, button3)
            find_alg(message, mode, None, None, lang_messages)

        elif message.text == lang_messages[24]:
        # change_status('wait_menu', message.chat.id)
            return
    except:
        pass


def find_alg(message, mode, user_find_atr, users_chat_id, lang_messages):
    try:
        if mode == 1:
            chat_id = str(message.chat.id)
            user_city = get_atribute("city", chat_id)
            user_find_gender = get_atribute("find_gender", chat_id)
            users_chat_id = get_from_db1(
            f"SELECT * FROM dbo.find_profiles({str(chat_id)}, N'{user_find_atr[0]}', '{user_find_atr[1]}');", 1)
            find_alg(message, 2, user_find_atr, users_chat_id, lang_messages)
        elif mode == 2:

            if not users_chat_id.empty():
                user = users_chat_id.get()
                user_info = get_from_db1(f"select * from Users where chat_id = {user}", 2)
                photo = open(user_exists(f"select photo from Users where chat_id = {user}"), 'rb')
                bot.send_photo(message.chat.id, photo, caption=lang_messages[11] + user_info[2] + '\n' +
                                                               lang_messages[12] + str(user_info[3]) + '\n' +
                                                               lang_messages[13] + user_info[4] + '\n' +
                                                               lang_messages[14] + user_info[5] + '\n')
            # if message == None:
                bot.register_next_step_handler(message, start_find, user, mode, user_find_atr, users_chat_id, lang_messages)
                if message.text == date_buttons[0]:
                    print('chuj')
                elif message.text == date_buttons[1]:
                    print('chuj')

                elif message.text == date_buttons[2]:
                    pass
                else:
                    pass
            else:
                bot.send_message(message.chat.id, 'Больше нет анкет для тебя:(, соси письку Настюша)))))')
    except:
        pass
#start verification
@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.username is None:
        photo = open('warning.jpg', 'rb')
        bot.send_photo(message.chat.id, photo, caption='Please set your nickname up and write me /start again')
        bot.register_next_step_handler(message, start)
    else:
        if user_exists(str(message.chat.id)):
            language = get_atribute("language", message.chat.id)
            if language == 'russian':
                lang_messages = messages_russian
                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
                button1 = types.KeyboardButton(lang_messages[23])
                button2 = types.KeyboardButton(lang_messages[24])
                markup.add(button1, button2)

                bot.send_message(message.chat.id, lang_messages[21], reply_markup=markup)
                bot.register_next_step_handler(message, start_dates, lang_messages, 1)


            elif language == 'polish':
                return
            else:
                return
        else:
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            button1 = types.KeyboardButton('Русский')
            button2 = types.KeyboardButton('Polski')
            button3 = types.KeyboardButton('English')
            markup.add(button1, button2, button3)
            bot.send_message(message.chat.id, 'Hello {0.first_name}, choose language please!'.format(message.from_user),
                             reply_markup=markup)


# registration process
@bot.message_handler(content_types=['text'])
def start_reg(message):
    user_atr = []
    lang_messages = []
    if message.chat.type == 'private':
        if message.text.lower() == 'русский':
            lang_messages = messages_russian
            user_atr.append('russian')
            bot.send_message(message.chat.id, lang_messages[0])
            bot.register_next_step_handler(message, add_name, lang_messages, user_atr)

        elif message.text.lower() == 'polski':
            bot.send_message(message.chat.id, 'Ten jezyk jest na etapie opracowania')
            return
        elif message.text.lower() == 'english':
            bot.send_message(message.chat.id, 'This language at the development stage')
            return

@bot.message_handler(content_types=['text'])
def add_name(message, lang_messages, user_atr):
    user_atr.append(message.chat.id)
    user_atr.append(message.from_user.username)
    user_atr.append(message.text)
    bot.send_message(message.chat.id, lang_messages[1])
    bot.register_next_step_handler(message, add_age, lang_messages, user_atr)

@bot.message_handler(content_types=['text'])
def add_age(message, lang_messages, user_atr):
    if not ((str(message.text)).isdigit()):
        bot.send_message(message.chat.id, lang_messages[20])
        bot.register_next_step_handler(message, add_age, lang_messages, user_atr)
    else:
        user_atr.append(message.text)
        bot.send_message(message.chat.id, lang_messages[2])
        bot.register_next_step_handler(message, add_city, lang_messages, user_atr)

@bot.message_handler(content_types=['text'])
def add_city(message, lang_messages, user_atr):
    user_atr.append(message.text)
    bot.send_message(message.chat.id, lang_messages[3])
    bot.register_next_step_handler(message, add_description, lang_messages, user_atr)

@bot.message_handler(content_types=['text'])
def add_description(message, lang_messages, user_atr):
    user_atr.append(message.text)
    bot.send_message(message.chat.id, lang_messages[4])
    bot.register_next_step_handler(message, add_photo, lang_messages, user_atr)

@bot.message_handler(content_types=['photo'])
def add_photo(message, lang_messages, user_atr):
    if message.content_type != 'photo':
        bot.send_message(message.chat.id, lang_messages[19])
        bot.register_next_step_handler(message, add_photo, lang_messages, user_atr)
    else:
        fileID = message.photo[-1].file_id
        file_info = bot.get_file(fileID)
        downloaded_file = bot.download_file(file_info.file_path)
        filename, file_extension = os.path.splitext(file_info.file_path)
        chat_id = str(message.chat.id)


        path = chat_id + file_extension
        user_atr.append(path)
        with open(path, 'wb') as new_file:
            new_file.write(downloaded_file)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton(lang_messages[5])
        button2 = types.KeyboardButton(lang_messages[6])
        markup.add(button1, button2)
        bot.send_message(message.chat.id, lang_messages[7], reply_markup=markup)
        bot.register_next_step_handler(message, add_sex, lang_messages, user_atr)

@bot.message_handler(content_types=['text'])
def add_sex(message, lang_messages, user_atr):
    if message.text == lang_messages[5]:
        user_atr.append('woman')
    elif message.text == lang_messages[6]:
        user_atr.append('man')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton(lang_messages[9])
    button2 = types.KeyboardButton(lang_messages[10])
    markup.add(button1, button2)
    bot.send_message(message.chat.id, lang_messages[8], reply_markup=markup)
    bot.register_next_step_handler(message, add_findsex, lang_messages, user_atr)

@bot.message_handler(content_types=['text'])
def add_findsex(message, lang_messages, user_atr):
    if message.text == lang_messages[9]:
        user_atr.append('woman')
    elif message.text == lang_messages[10]:
        user_atr.append('man')
    print(user_atr)

    photo = open(user_atr[7], 'rb')
    bot.send_photo(message.chat.id, photo, caption=lang_messages[11] + user_atr[3] + '\n' +
                                                   lang_messages[12] + user_atr[4] + '\n' +
                                                   lang_messages[13] + user_atr[5] + '\n' +
                                                   lang_messages[14] + user_atr[6] + '\n')
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button1 = types.KeyboardButton(lang_messages[15])
    button2 = types.KeyboardButton(lang_messages[16])
    markup.add(button1, button2)
    bot.send_message(message.chat.id, lang_messages[17], reply_markup=markup)
    bot.register_next_step_handler(message, accept_data, lang_messages, user_atr)

@bot.message_handler(content_types=['text'])
def accept_data(message, lang_messages, user_atr):
    if message.text == lang_messages[15]:
        add_user(message.chat.id, user_atr)
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        button1 = types.KeyboardButton(lang_messages[23])
        button2 = types.KeyboardButton(lang_messages[24])
        markup.add(button1, button2)
        bot.send_message(message.chat.id, lang_messages[22], reply_markup=markup)
        bot.register_next_step_handler(message, start_dates, lang_messages, user_atr)


    elif message.text == lang_messages[16]:
        language = user_atr[0]
        user_atr.clear()
        user_atr.append(language)
        bot.send_message(message.chat.id, lang_messages[18])
        bot.register_next_step_handler(message, add_name, lang_messages, user_atr)


@bot.message_handler(content_types=['text'])
def start_find(message, user, mode, user_find_atr, users_chat_id, lang_messages):
    if message.text == date_buttons[0]:
        print('lol')
        add_to_dbase(f"insert into Viewes values ({message.chat.id}, {user}, 'like')")
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        button = types.KeyboardButton('Посмотреть')
        markup.add(button)
        bot.send_message(user, 'Тебя лайкнули!', reply_markup=markup)
        find_alg(message, mode, user_find_atr, users_chat_id, lang_messages)
    elif message.text == date_buttons[1]:
        add_to_dbase(f"insert into Viewes values ({message.chat.id}, {user}, 'dislike')")
        find_alg(message, mode, user_find_atr, users_chat_id, lang_messages)
    elif message.text == date_buttons[2]:
        add_to_dbase(f"insert into Viewes values ({message.chat.id}, {user}, 'exit_menu')")
        pass
    elif message.text == 'Посмотреть':

        pass
        bot.send_message(message.chat.id, 'ban')


bot.polling(none_stop=True)