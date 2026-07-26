import sqlite3

db = sqlite3.connect("database.db", check_same_thread=False)
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS hesaplar (
    telegram_id INTEGER,
    username TEXT,
    durum TEXT
)
""")

db.commit()


def hesap_ekle(telegram_id, username):
    cursor.execute(
        "INSERT INTO hesaplar VALUES (?, ?, ?)",
        (telegram_id, username, "aktif")
    )
    db.commit()


def hesaplari_getir(telegram_id):
    cursor.execute(
        "SELECT username FROM hesaplar WHERE telegram_id=?",
        (telegram_id,)
    )
    return cursor.fetchall()


def tum_hesaplar():
    cursor.execute(
        "SELECT telegram_id, username, durum FROM hesaplar"
    )
    return cursor.fetchall()


def durum_guncelle(username, durum):
    cursor.execute(
        "UPDATE hesaplar SET durum=? WHERE username=?",
        (durum, username)
    )
    db.commit()


def hesap_sil(telegram_id, username):
    cursor.execute(
        "DELETE FROM hesaplar WHERE telegram_id=? AND username=?",
        (telegram_id, username)
    )
    db.commit()
