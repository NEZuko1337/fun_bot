import sqlite3 as sq
import random

db = sq.connect("words.db")
cur = db.cursor()


async def db_start():
    cur.execute("CREATE TABLE IF NOT EXISTS words(user_id INTEGER, word TEXT, photo TEXT)")
    db.commit()


async def fill_words_or_photos(user_id, word, photo):
    if word is None:
        word = ""
    if photo is None:
        photo = ""
    cur.execute(f"INSERT INTO words VALUES(?, ?, ?)", (user_id, word, photo))
    db.commit()


def size_of_db():
    data = cur.execute("select count(*) from words")
    results = cur.fetchone()[0]
    return results


async def delete_profile(user_id):
    usr_id = cur.execute(f"SELECT user_id FROM words WHERE user_id=={user_id}").fetchone()
    if usr_id:
        cur.execute(f"DELETE FROM words WHERE user_id == {user_id}")
        db.commit()


async def delete_db():
    cur.execute("DELETE FROM words")
    db.commit()


def get_all_images():
    query = (
        "SELECT photo FROM words WHERE photo != ''"
    )
    stmt = cur.execute(query).fetchall()
    arr_with_photos = set()
    for elem in stmt:
        x = ''.join(elem)
        arr_with_photos.add(x)
    return list(arr_with_photos)


def get_all_words():
    query = (
        "SELECT word FROM words WHERE word != ''"
    )
    cool_words = []
    stmt = cur.execute(query).fetchall()
    for elem in stmt:
        x = ''.join(elem)
        cool_words.append(x.split(" "))

    last_arr_with_words = set()
    for el in cool_words:
        for j in range(len(el)):
            last_arr_with_words.add(el[j])

    return list(last_arr_with_words)
