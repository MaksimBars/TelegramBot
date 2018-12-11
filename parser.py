# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

"""Парсер для получения транскрипции и перевода слова, запаковано в лист для удобства добавления в базу данных. """
base_url = 'https://wooordhunt.ru/word/'  # шаблонная ссылка


def get_url(word):
    word = word.lower()
    url = base_url + word  # генерируем ссылку
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    rus_word = soup.find('span', {'class': "t_inline_en"})  # получаем перевод слова
    transcription = soup.find('span', {'class': "transcription"})  # получаем транскрипцию
    error = soup.find('div', id="word_not_found")
    if not rus_word and not transcription:
        error_text = error.text
        error_date = None
        return error_date, error_text
    else:
        if not transcription:
            phrase = soup.find('div', {'class': "block phrases"}).find_all('i')  # получаем фразу
            phrase_string = phrase[0].text
            return [word, None, phrase_string]  # пакуем в лист без транскрипции
        else:
            return [word, transcription.text, rus_word.text]  # пакуем в лист , с транскрипцией
