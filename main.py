from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram
import logging
import json
import urllib.request
import zipfile
import cv2
import os
from os import listdir
import emoji
from emoji import emojize
import shutil


class bot():
    def start(updater, context):
        print('{{/start}}:({username})'.format(username=updater.effective_chat.username))
        context.bot.send_message(
            chat_id=updater.effective_chat.id,
            text='Just give me the sticker\'s store link!\nExample: https://store.line.me/stickershop/product/0000001/zh-Hant')

    def echo(updater, context):
        print('{{/echo}}:({username}):{text}'.format(username=updater.effective_chat.username, text=updater.message.text))
        if updater.message.text[0:42] == 'https://store.line.me/stickershop/product/':
            ID = updater.message.text[42::]
            ID = ''.join(list(filter(str.isdigit, ID)))
            Sticker_set = sticker_set_process(updater, context, ID)
            print(Sticker_set.ID)
            if Sticker_set.checkExist():
                pass
            else:
                Sticker_set.get_sticker_set()
                Sticker_set.image_transcoding()
                Sticker_set.upload_to_telegram()
                Sticker_set.record_converted_stickers()
        else:
            context.bot.send_message(
                chat_id = updater.effective_chat.id,
                text = 'Wrong input content!\nPlease give me the sticker\'s store link.\nExample: https://store.line.me/stickershop/product/00001/zh-Hant')


class sticker_set_process():
    def __init__(self, updater, context, ID):
        self.updater = updater
        self.context = context
        self.ID = ID
        self.tg_sticker_set_name = 'id{}_by_TLStT_bot'.format(str(self.ID))

    def get_sticker_set(self):
        # Get line sticker set from request.
        print('downloading'+self.ID)
        dl_pkg_link = 'http://dl.stickershop.line.naver.jp/products/0/0/1/{}/iphone/stickers@2x.zip'.format(self.ID)
        try:
            dl_file = urllib.request.urlopen(dl_pkg_link)
            with open('Stickers.zip', 'wb') as ZipFile:
                ZipFile.write(dl_file.read())
                print('{} download finish.'.format())
                self.context.bot.send_message(
                    chat_id = self.updater.effective_chat.id,
                    text = 'Download {} Success!\nJust wait minute for upload to telegram!'.format(self.ID))
                return True
        except:
            print('Download sticker set error.')
            return False

    def image_transcoding(self):
        # Transcoding line's sticker as telegram's spcification.
        with zipfile.ZipFile('Stickers.zip', 'r') as zFile:
        # Extract zip file.
            for fileM in zFile.namelist():
                zFile.extract(fileM, 'Stickers')
            zFile.close()
        img_files = listdir('Stickers')
        amount = 0
        for img_name in img_files:
        # Image resize.
            print(img_name)
            if 'key' not in img_name and 'tab' not in img_name and 'pro' not in img_name:
            # Ignore "productInfo.meta" "tab_on/off@2x.png" "KEY image"
                amount+=1
                image = cv2.imread('Stickers/{}'.format(img_name), cv2.IMREAD_UNCHANGED)
                mag = 512/image.shape[0]
                src = cv2.resize(image, (int(image.shape[1]*mag), 512), interpolation=cv2.INTER_CUBIC)
                if image.shape[0]<=image.shape[1]:
                    mag = 512/image.shape[1]
                    src = cv2.resize(image, (512, int(image.shape[0]*mag)), interpolation=cv2.INTER_CUBIC)
                src[63, 63, :] = [255, 0, 0, 128]
                cv2.imwrite('image{}.png'.format(str(amount)), src, [int(cv2.IMWRITE_PNG_COMPRESSION), 9])
                print('{} finish resize {}'.format(img_name, amount))
        print('All image resize finish!')

    def upload_to_telegram(self):
        sticker_info = json.load(open('Stickers//productInfo.meta'))
        self.eng_name = sticker_info['title']['en']
        if 'zh-Hant' in sticker_info['title']:
            self.tw_name = sticker_info['title']['zh-Hant']
        else:
            self.tw_name = self.eng_name
        default_emj = emoji.emojize(':smile:', use_aliases=True)
        # Get an emoji for upload need.
        print(self.updater.message.from_user.id, self.tg_sticker_set_name, self.tw_name, self.eng_name)
        amount = 0
        img_file = listdir()
        for png_sticker in img_file:
            if '.png' in png_sticker:
                amount+=1
                try:
                    self.context.bot.addStickerToSet(
                        user_id=self.updater.message.from_user.id,
                        name=self.tg_sticker_set_name,
                        emojis=default_emj,
                        png_sticker=open(''+png_sticker, 'rb'))
                except telegram.error.BadRequest:
                    self.context.bot.createNewStickerSet(
                        user_id=self.updater.message.from_user.id,
                        name=self.tg_sticker_set_name,
                        title=self.eng_name,
                        emojis=default_emj,
                        png_sticker=open(''+png_sticker, 'rb'))
                os.remove(png_sticker)
                print('upload '+self.tg_sticker_set_name+' success. ', amount)
        shutil.rmtree('Stickers')
        os.remove('Stickers.zip')
        print('finish!\nhttps://t.me/addstickers/{}'.format(self.tg_sticker_set_name))
        self.context.bot.send_message(
            chat_id=self.updater.effective_chat.id,
            text='{}\nhttps://t.me/addstickers/{}'.format(self.tw_name, self.tg_sticker_set_name))

    def record_converted_stickers(self):
        jsonFile = open('converted_stickers.json', 'r')
        data = json.loads(jsonFile.read())
        data.update({self.ID:self.tw_name})
        jsonFile = open('converted_stickers.json', 'w')
        json.dump(data, jsonFile)
        jsonFile.close()

    def checkExist(self):
        jsonFile = json.load(open('converted_stickers.json'))
        if self.ID in jsonFile:
            self.tg_sticker_link = jsonFile[self.ID]+'\nhttps://t.me/addstickers/{}'.format(self.tg_sticker_set_name)
            self.context.bot.send_message(
                chat_id=self.updater.effective_chat.id,
                text=self.tg_sticker_link,)
            return True
        else:
            return False



def commands(dispatcher, updater):
    start_handler = CommandHandler('start', bot.start)
    echo_handler = MessageHandler(Filters.text, bot.echo)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(echo_handler)
    updater.start_polling()

def bot_setting():
    TOKEN = json.load(open('..//..//Api_Token.json', 'r'))
    updater = Updater(
        token=TOKEN['Telegram']['Transfer_LineStickers_to_Telegram'],
        use_context=True)
    dispatcher = updater.dispatcher
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)
    commands(dispatcher, updater)


if __name__=="__main__":
    bot_setting()

