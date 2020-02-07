from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import json


def start(update, context):
	print(update.effective_chat.username)
	context.bot.send_message(chat_id=update.effective_chat.id, text="Just give me the sticker's store link!\nExample: https://store.line.me/stickershop/product/8751482/zh-Hant")

def echo(update, context):
	if(update.message.text[0:42] == 'https://store.line.me/stickershop/product/'):
		Stickers_ID = update.message.text[42:49]
		Stickers_ID = ''.join(list(filter(str.isdigit, Stickers_ID)))
		downlaoder(update, Stickers_ID)
	else:
		context.bot.send_message(chat_id=update.effective_chat.id, text="Wrong input content!\nPlease give me the sticker's store link.\nExample: https://store.line.me/stickershop/product/00001/zh-Hant")

def downloader(update, Stickers_ID): # downlaod sticker and transfer to tg
	dl_pkg_link = "dl.stickershop.line.naver.jp/products/0/0/1/"+Stickers_ID+"/iphone/stickers@2x.zip"
	


def main():
	TOKEN = json.load(open('..//..//Api_Token.json', 'r'))
	updater = Updater(token=TOKEN['Telegram']['Transfer_LineStickers_to_Telegram'], use_context=True)	#api token set
	dispatcher = updater.dispatcher
	logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)		

	start_handler = CommandHandler('start', start)
	echo_handler = MessageHandler(Filters.text, echo)

	dispatcher.add_handler(start_handler)
	dispatcher.add_handler(echo_handler)
	updater.start_polling()
	

if __name__ == "__main__":
	main()
# dl.stickershop.line.naver.jp/products/0/0/1/8751482/iphone/stickers@2x.zip
