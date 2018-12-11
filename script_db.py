# -*- coding: utf-8 -*-
import sqlite3


def add_base(translate):
    """Функция добавления в базу данных транскрипцию и перевод полученую после парсинга сайта."""
    conn = sqlite3.connect('words.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO words (eng, transcription, many_rus, properly, wrong) VALUES (?, ?, ?, ?, ?)',
                   (translate[0], translate[1], translate[2], 0, 0))
    conn.commit()
    conn.close()
    # cursor.execute("""CREATE TABLE words ('eng','transcription','many_rus','properly','wrong')""")
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
    """Функция выборки рандомной строки из базы данных.(Позже переделается под алгоритм проверки и выборки)"""
    conn = sqlite3.connect('words.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM words ORDER BY RANDOM() LIMIT 1")
    cut = cursor.fetchone()
    conn.close()
    return cut


def search_rus_in_db(word, text):
    """Поиск по русскому слову"""
    conn = sqlite3.connect('words.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM words WHERE eng=?", [word])
    count = cursor.fetchone()
    rus = count[2]
    conn.close()
    if text in rus:
        return "Верно"
    else:
        text = "Неверно:\n" + rus
        return text


def reg_user(users_id, user_name):
    conn = sqlite3.connect('words.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO user_id (chat_id, name) VALUES (?, ?)', (users_id, user_name))
    conn.commit()
    conn.close()


def user_id():
    conn = sqlite3.connect('words.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_id")
    cut = cursor.fetchall()
    conn.close()
    return cut
