# -*- coding: utf-8 -*-
import config
import telebot
from telebot.types import ReplyKeyboardMarkup
import script_db
from datetime import datetime
import threading
import parser

bot = telebot.TeleBot(config.token, threaded=True)


def log_message(message, answer):
    print("\n ----------------------------")
    print(datetime.now())
    print("Сообщение от {0} {1}. (id = {2} ) \n Текст сообщения - {3}".format(message.from_user.first_name,
                                                                              message.from_user.last_name,
                                                                              str(message.from_user.id),
                                                                              message.text))
    print('Ответ бота:', answer)


@bot.message_handler(commands=['start'])
def command_start(message):
    """Команда start запускает бота и вызывает выпадающие кнопки."""
    user_markup = ReplyKeyboardMarkup(True, True)
    user_markup.row('/add', '/help')
    bot.send_message(message.from_user.id,
                     "Привет {0} я SlameBot.\n"
                     "Чтобы увидеть полный список команд введи /help".format(message.from_user.first_name),
                     reply_markup=user_markup)
    log_message(message, 'start')


@bot.message_handler(commands=["reg"])
def reg(message):
    """Регистрируем юзера для рассылки"""
    user_name = message.from_user.first_name
    user_id = message.from_user.id
    script_db.reg_user(user_id, user_name)
    bot.send_message(message.chat.id, "Вы добавлены в базу для рассылки слов")


@bot.message_handler(commands=["help"])
def help_command(message):
    """Команда help  показывает доступные команды."""
    bot.send_message(message.chat.id,
                     "/start -- для запуска бота, а также вызова клавиатуры.\n"
                     "/help -- список команд бота.\n"
                     "/add -- для добавления слова в словарь.\n"
                     "/rep -- для повторения слова.")
    log_message(message, 'help')


@bot.message_handler(commands=["add"])
def add_command(message):
    """Команда для добавления слов."""
    answer = "Введи слово"
    msg = bot.send_message(message.chat.id, answer)
    bot.register_next_step_handler(msg, input_word)
    log_message(message, answer)


def input_word(message):
    """Обрабатывает английское слово после ввода в чат."""
    answer = "Добавлено слово"
    wrong = "Такое слово уже присутствует в словаре!"
    if not script_db.search_eng_in_db(message.text):
        translate = parser.get_url(message.text)
        if not translate[0]:
            error = translate[1]
            bot.send_message(message.from_user.id, error)
            log_message(message, error)
        else:
            script_db.add_base(parser.get_url(message.text))
            bot.send_message(message.from_user.id, "{} - {}".format(answer, message.text))
            log_message(message, answer)
    else:
        bot.send_message(message.from_user.id, wrong)
        log_message(message, wrong)


temp_word = []


@bot.message_handler(commands=["rep"])
def repeat_word(message):
    """Команда  повторения слова."""
    text = script_db.data_sampling()[0]
    msg = bot.send_message(message.chat.id, "Введите перевод слова: " + text)
    bot.register_next_step_handler(msg, search_repeat)
    temp_word.append(text)
    log_message(message, text)


def search_repeat(message):
    """Обработчик введённого слова при повторении."""
    word = temp_word[0]
    message_text = message.text.lower()
    x = script_db.search_rus_in_db(word, message_text)
    bot.send_message(message.from_user.id, x)
    temp_word.clear()
    log_message(message, x)


threading.Thread(bot.polling(none_stop=True)).start()
threading.Thread(repeat_word).start()
