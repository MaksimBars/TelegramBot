import telebot
import config
import time
import script_db
"""Повторения слов из базы данных( тестовые выборки ), должна быть запущена в Cron."""
bot = telebot.TeleBot(config.token, threaded=True)


def repeat_word():
    """Функция рассылки слов."""
    date = script_db.user_id()
    for i in date:
        user_id = i
        text = script_db.data_sampling()
        if not text[1]:
            word = text[0] + ' -- ' + text[2]
            bot.send_message(chat_id=user_id[0], text=word)
        else:
            word = text[0] + ' -- ' + text[1] + ' -- ' + text[2]
            bot.send_message(chat_id=user_id[0], text=word)


while True:
    repeat_word()
    # усыпляем функцию на 30 минут
    time.sleep(1800)
