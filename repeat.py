import telebot
import config
import time
import script_db
""" Функция повторения слов из базы данных( тестовые выборки ), должна быть запущена либо под Cron(отложенной задачей)
либо отдельным потоком."""
bot = telebot.TeleBot(config.token, threaded=True)


def repeat_word():
    text = script_db.data_sampling()
    if not text[1]:
        word = text[0] + ' <> ' + text[2]
        bot.send_message(chat_id=500554167, text=word)
    else:
        word = text[0] + ' <> ' + text[1] + ' <> ' + text[2]
        bot.send_message(chat_id=500554167, text=word)


while True:
    repeat_word()
    time.sleep(60)
