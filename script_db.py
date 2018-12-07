# -*- coding: utf-8 -*-
import sqlite3
import parser


def add_base(word):
    """Функция добавления в базу данных транскрипцию и перевод полученую после парсинга сайта."""
    translate = parser.get_url(word)
    conn = sqlite3.connect('words.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO words (eng, transcription, rus, many_rus, properly, wrong) VALUES (?, ?, ?, ?, ?, ?)',
                   (translate[0], translate[1], translate[2], translate[3], 0, 0))
    conn.commit()
    conn.close()
    # cursor.execute("""CREATE TABLE words ('eng','transcription','rus','right','wrong')""")
    # conn.commit()
    # conn.close()


def search_eng_in_db(word):
    """Функция поиска дубликатов в базе перед добавлением в неё новых слов, возращает True если слово есть в базе, и
    False если в ней нет такого слова."""
    word = word.lower()
    conn = sqlite3.connect('words.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT() FROM words WHERE eng = (?)", [word])
    count = cursor.fetchone()[0]
    if not count:
        conn.close()
        return False
    else:
        conn.close()
        return True


def data_sampling():
    """Функция выборки рандомной строки из базы данных.(Позже передалется под алгоритм проверки и выборки)"""
    conn = sqlite3.connect('words.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM words ORDER BY RANDOM() LIMIT 1")
    cut = cursor.fetchone()
    return cut


def search_rus_in_db(word, text):
    """Поиск по русскому слову"""
    conn = sqlite3.connect('words.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM words WHERE eng=? AND rus=?", [word, text])
    count = cursor.fetchone()
    if count:
        return "Верно"
    else:
        text = "Неверно:\n" + search_in_db(word)
        return text


def search_in_db(word):
    conn = sqlite3.connect('words.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM words WHERE eng=?", [word])
    some_rus = cursor.fetchone()[3]
    return some_rus
