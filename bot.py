# -*- coding: utf-8 -*-
import config
import telebot
from telebot.types import ReplyKeyboardMarkup
import script_db
from datetime import datetime
bot = telebot.TeleBot(config.token, threaded=True)


def log_message(message, answer):
    print("\n ----------------------------")
    print(datetime.now())
    print("Message from {0} {1}. (id = {2} ) \n Text - {3}".format(message.from_user.first_name,
                                                                   message.from_user.last_name,
                                                                   str(message.from_user.id),
                                                                   message.text))
    print(answer)


@bot.message_handler(commands=['start'])
def command_start(message):
    user_markup = ReplyKeyboardMarkup(True, True)
    user_markup.row('/add', '/help')
    bot.send_message(message.from_user.id,
                     "Hello {0} i'm SlameBot.\n"
                     "Full list of commands /help".format(message.from_user.first_name),
                     reply_markup=user_markup)
    log_message(message, 'start')


@bot.message_handler(commands=["help"])
def help_command(message):
    bot.send_message(message.chat.id,
                     "/start -- start working with the bot.\n"
                     "/help -- list of bot commands.\n"
                     "/add -- adding words.\n")
    log_message(message, 'help')


@bot.message_handler(commands=["add"])
def add_command(message):
    answer = "Enter the word"
    msg = bot.send_message(message.chat.id, answer)
    bot.register_next_step_handler(msg, input_word)
    log_message(message, answer)


def input_word(message):
    answer = "Added by"
    wrong = "The word is already in the database!"
    if not script_db.search_eng_in_db(message.text):
        script_db.add_base(message.text)
        bot.send_message(message.from_user.id, "{} - {}".format(answer, message.text))
        log_message(message, answer)
    else:
        bot.send_message(message.from_user.id, wrong)
        log_message(message, wrong)


bot.polling(none_stop=False)
