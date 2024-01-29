
 
import asyncio
from telethon import events
from telethon import TelegramClient
import time
import sqlite3
from tkinter import *
import threading
import random

from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP


db = sqlite3.connect('Account.db', timeout=30)
cur = db.cursor() 
 
window = Tk()
 
messages = Text(window)
 
 
input_user = StringVar()
input_field = Entry(window, text=input_user)
 
 
cur.execute(f"SELECT API_ID FROM Account WHERE ID = '{1}'")

api_id = str(cur.fetchone()[0])
time.sleep(1)
cur.execute(f"SELECT API_HASH FROM Account WHERE ID = '{1}'")

api_hash = str(cur.fetchone()[0])
time.sleep(1)
session = "anon31"
 
client = TelegramClient("anon31", api_id, api_hash).start()
client.start()
time.sleep(1)
cur.execute(f"SELECT ID_SOB FROM Account WHERE ID = '{1}'")
id_sob = str(cur.fetchone()[0])
zorro = int(id_sob)
time.sleep(1)

def Enter_pressed(event):
	input_get = input_field.get()
	print(input_get)
	
	print("Зашифровка")
	
	sms = str(input_get)
	chars = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
	smssKa = ""
	for i in range(40):
		smssKa += random.choice(chars)
	print(smssKa)
	
	
	data = sms.encode("utf-8")
	binx = str(smssKa) + ".bin"	
	file_out = open(binx, "wb")
	cur.execute(f"SELECT MY_ID FROM Account WHERE ID = '{1}'")
	my_id = str(cur.fetchone()[0])
	my_key = str(my_id) + ".pem"
	
	recipient_key = RSA.import_key(open(my_key).read())
	session_key = get_random_bytes(16)
	
	cipher_rsa = PKCS1_OAEP.new(recipient_key)
	enc_session_key = cipher_rsa.encrypt(session_key)
	
	cipher_aes = AES.new(session_key, AES.MODE_EAX)
	ciphertext, tag = cipher_aes.encrypt_and_digest(data)
	[ file_out.write(x) for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext) ]
	file_out.close()

	print("Отправка шифровки")
	
	cur.execute(f"SELECT NAME FROM Account WHERE ID = '{1}'")
	name = str(cur.fetchone()[0])
	async def main():
		await client.send_file(name, binx)
	client.loop.run_until_complete(main())
	
	
	messages.insert(INSERT, '%s\n' % input_get)

	input_user.set('')

	return "break"
 
 
frame = Frame(window)
 
frame.pack()
messages.pack()
input_field.pack(side=BOTTOM, fill=X)
input_field.bind("<Return>", Enter_pressed)


def run_bot_events():
	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop)
	loop.run_until_complete(async_run_events(loop))
	
async def async_run_events(loop):
	eventing_client = await TelegramClient("anon32", api_id, api_hash, loop=loop).start()
	

	@eventing_client.on(events.newmessage.NewMessage(from_users=zorro))
	async def handler(event):

		if event.media is not None:
			chars1 = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
			smssKa1 = ""
			for i in range(50):
				smssKa1 += random.choice(chars1)
			print(smssKa1)
			biny = str(smssKa1) + ".bin"
			
			task = eventing_client.loop.create_task(event.download_media(biny))
			await task
			print("Дешефровка!")
			
			file_in = open(biny, "rb")
			private_key = RSA.import_key(open("private.pem").read())
			enc_session_key, nonce, tag, ciphertext = \
				[ file_in.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1) ]
			cipher_rsa = PKCS1_OAEP.new(private_key)
			session_key = cipher_rsa.decrypt(enc_session_key)
			cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
			data2 = cipher_aes.decrypt_and_verify(ciphertext, tag)
			print(data2.decode("utf-8"))
			
			enk = data2.decode("utf-8")
			
			messages.insert(INSERT, '%s\n' % enk)
	await eventing_client.run_until_disconnected()

threading.Thread(target=run_bot_events).start()
window.mainloop()
