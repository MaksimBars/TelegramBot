import sqlite3
import parser


def add_base(word):
    translate = parser.get_url(word)
    conn = sqlite3.connect('words.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO words (eng, transcription, rus, right, wrong) VALUES (?, ?, ?, ?, ?)',
                   (translate[0], translate[1], translate[2], 0, 0))
    conn.commit()
    conn.close()
    # cursor.execute("""CREATE TABLE words ('eng','transcription','rus','right','wrong')""")
    # conn.commit()
    # conn.close()


def search_in_db(word):
    pass


def data_sampling(word):
    pass
