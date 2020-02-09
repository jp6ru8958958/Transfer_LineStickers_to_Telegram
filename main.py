from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import json
import urllib.request
import zipfile
import cv2
import numpy as np
import os
from os import listdir


def start(update, context):
	print(update.effective_chat.username)
	context.bot.send_message(chat_id=update.effective_chat.id, text='Just give me the sticker\'s store link!\nExample: https://store.line.me/stickershop/product/8751482/zh-Hant')

def echo(update, context):
	if(update.message.text[0:42] == 'https://store.line.me/stickershop/product/'):
		Stickers_ID = update.message.text[42::]
		Stickers_ID = ''.join(list(filter(str.isdigit, Stickers_ID)))
		print(Stickers_ID)
		if(downloader(Stickers_ID)):
			context.bot.send_message(chat_id=update.effective_chat.id, text='Download '+Stickers_ID+' Success!\nJust wait minute for upload to telegram!')
			image_transcoding()
		else:
			print('Download error.')
			context.bot.send_message(chat_id=update.effective_chat.id, text='Something error!\nPlease try other sticker link.')
	else:
		context.bot.send_message(chat_id=update.effective_chat.id, text='Wrong input content!\nPlease give me the sticker\'s store link.\nExample: https://store.line.me/stickershop/product/00001/zh-Hant')

def downloader(Stickers_ID):
	dl_pkg_link = 'http://dl.stickershop.line.naver.jp/products/0/0/1/'+Stickers_ID+'/iphone/stickers@2x.zip'
	try:
		dl_file = urllib.request.urlopen(dl_pkg_link)
		with open('Stickers.zip', 'wb') as ZipFile:
			ZipFile.write(dl_file.read())
			print(Stickers_ID+' download finish.')
			return True
	except:
		return False
	
def image_transcoding():
	with zipfile.ZipFile('Stickers.zip', 'r') as zFile:
		for fileM in zFile.namelist():
			zFile.extract(fileM, 'Stickers')
		zFile.close()
	img_files = listdir('Stickers')
	amount=0
	for img_name in img_files:
		if 'key' not in img_name and 'tab' not in img_name and 'pro' not in img_name:
			amount+=1
			print(img_name+' finish resize ', amount)
			image=cv2.imread('Stickers/'+img_name, cv2.IMREAD_UNCHANGED)
			if image.shape[0]>=image.shape[1]:
				mag = 512/image.shape[0]
				src=cv2.resize(image, ( int(image.shape[1]*mag), 512), interpolation=cv2.INTER_CUBIC)
				src[ 63, 63, :] = [ 255, 0, 0, 128]
				cv2.imwrite('image'+str(amount)+'.png', src, [int(cv2.IMWRITE_PNG_COMPRESSION), 9])
			else:
				mag = 512/image.shape[1]
				src=cv2.resize(image, ( 512, int(image.shape[0]*mag)), interpolation=cv2.INTER_CUBIC)
				src[ 63, 63, :] = [ 255, 0, 0, 128]
				cv2.imwrite('image'+str(amount)+'.png', src, [int(cv2.IMWRITE_PNG_COMPRESSION), 9])

def main():
	TOKEN = json.load(open('..//..//Api_Token.json', 'r'))
	updater = Updater(token=TOKEN['Telegram']['Transfer_LineStickers_to_Telegram'], use_context=True)
	dispatcher = updater.dispatcher
	logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)		
	start_handler = CommandHandler('start', start)
	echo_handler = MessageHandler(Filters.text, echo)
	dispatcher.add_handler(start_handler)
	dispatcher.add_handler(echo_handler)
	updater.start_polling()
	

if __name__ == "__main__":
	main()

