import sqlite3
from telethon import TelegramClient
import time
import subprocess
import sys


db = sqlite3.connect('Account.db', timeout=30)
cur = db.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS Account (
    ID INTEGER PRIMARY KEY,
    API_ID TEXT,
    API_HASH TEXT,
    NAME TEXT,
    ID_SOB TEXT,
    MY_ID TEXT
)""")

db.commit()


def console_picture():
    print("  _____          _                           _         ")
    time.sleep(0.5)
    print(" |_   _|  _ __  (_)   __ _   _ __     __ _  | |   ___  ")
    time.sleep(0.5)
    print("   | |   | '__| | |  / _` | | '_ \   / _` | | |  / _ \ ")
    time.sleep(0.5)
    print("   | |   | |    | | | (_| | | | | | | (_| | | | |  __/ ")
    time.sleep(0.5)
    print("   |_|   |_|    |_|  \__,_| |_| |_|  \__, | |_|  \___| ")
    time.sleep(0.5)
    print("                                     |___/             ")
    time.sleep(0.5)
console_picture()
print("Добро пожаловать в треугольный Gram! ")
print("Важно: ")
print("Должны быть установлены все зависимости")
print("В процессе конфигурирования нужно создать 2 клиента, поэтому логиниться придеться дважды")
print("По завершению диалога все файлы можно удалить скриптом delete.py")
print("==============================")
print("Видео инструкция: https://www.youtube.com/watch?v=LADJTDajw0E")
print("==============================")
print("Нажми Enter чтобы запустить...")
input()

api_id = input("Введи свой Api_id: ")
api_hash = input("Введи свой Api_hash: ")
name = input("Введи ник собеседника? ")
id_sob = "1"
my_id = "1"

cur.execute(f"SELECT API_ID FROM Account WHERE API_ID = '{api_id}'")
if cur.fetchone() is None:
    cur.execute("""INSERT INTO Account(API_ID, API_HASH, NAME, ID_SOB, MY_ID) VALUES (?,?,?,?,?);""", (api_id, api_hash, name, id_sob, my_id))
    db.commit()
    print("Зарегистрированно!")
    #for value in cur.execute("SELECT * FROM Account"):
        #print(value)

z = 1

while(True):
	session = "anon3" + str(z)
	client = TelegramClient(session, api_id, api_hash)
	client.start()
	print("Аккаунт: " + str(z) + " Вход выполнен успешно!")
	z = z+1
	if z == 3:
		print("Aккаунты активированы!")
		break
		

