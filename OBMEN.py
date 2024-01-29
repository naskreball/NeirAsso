from telethon import sync, events
import time
from telethon import TelegramClient
from Crypto.PublicKey import RSA
import os
import asyncio
import sqlite3

db = sqlite3.connect('Account.db', timeout=30)
cur = db.cursor()

cur.execute(f"SELECT API_ID FROM Account WHERE ID = '{1}'")

api_id = str(cur.fetchone()[0])
time.sleep(1)
cur.execute(f"SELECT API_HASH FROM Account WHERE ID = '{1}'")

api_hash = str(cur.fetchone()[0])
time.sleep(1)
session = "anon31"

client = TelegramClient(session, api_id, api_hash)
client.start()

myself = client.get_me()
my = str(myself.id) + ".pem"
k = str(myself.id)
cur.execute(f'UPDATE Account SET MY_ID = ? WHERE ID = ?', (k, 1))
db.commit()
time.sleep(1)
#print(my)

cur.execute(f"SELECT NAME FROM Account WHERE ID = '{1}'")
name = str(cur.fetchone()[0])
time.sleep(1)
def func():
	print("Генерируем ключи шифрования")
	key = RSA.generate(2048)
	private_key = key.export_key()
	file_out = open("private.pem", "wb")
	file_out.write(private_key)
	file_out.close()

	public_key = key.publickey().export_key()
	file_out = open("receiver.pem", "wb")
	file_out.write(public_key)
	file_out.close()
	
print("Получаем ID собеседника!")
entity = client.get_dialogs()
entity = client.get_entity(name)

#print(entity.id)

id_Friend = entity.id
m = str(id_Friend)
time.sleep(1)
cur.execute(f'UPDATE Account SET ID_SOB = ? WHERE ID = ?', (m, 1))
db.commit()
time.sleep(1)
print("Зарегистрированно!")



func()

os.rename("receiver.pem", m + ".pem")

z = str(id_Friend) + ".pem"
print("Производим обмен открытыми ключами")
client.send_file(name, z)

time.sleep(3)
c = 0
while(True):
	print("Отправляем ключь")
	cur.execute(f"SELECT NAME FROM Account WHERE ID = '{1}'")
	name1 = str(cur.fetchone()[0])
	client.send_file(name1, z)
	print("Ключь отправлен")
	msgs = client.get_messages(name, limit=4)
	for msg in msgs:
		if msg.media is not None:
			client.download_media(message=msg)
			for my1 in os.listdir():
				if my1.endswith(my):
					print("Ключ Скачан!")
					c = c + 1
	if c == 0:
		print("Ожидаем ключь от собеседника, ждем 40 секунд")
		time.sleep(40)
	else:
		print("ОБМЕН КЛЮЧАМИ ПРОИЗВЕДЕН!")
		break

loop = asyncio.get_event_loop()
async def main():
    for char in 'НАЧИНАЕМ ЗАШИФРОВАННУЮ ПЕРЕПИСКУ!!!\n':
        print(char, end='', flush=True)
        await asyncio.sleep(0.1)

loop.run_until_complete(main())


