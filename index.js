const TeleBot = require('telebot');
const request = require("request");
const cheerio = require("cheerio");
const document = require("document");

const token = 'token';
const bot = new TeleBot(token);

function download_file(url){
    let $a = document.createElement('a');
    $a.setAttribute('href', url);
    $a.setAttribute('download', '');
    let evObj = document.createEvent('MouseEvents');
    evObj.initMouseEvent('click', true, true, window, 0, 0, 0, 0, 0, false, false, true, false, 0, null);
    $a.dispatchEvent(evObj);
};

function Stickers_Info(ID) {
    console.log('\nSticker ID:', ID);
    dl_url = 'dl.stickershop.line.naver.jp/products/0/0/1/' + ID + '/iphone/stickers@2x.zip';
    console.log('Start download ', dl_url);
    download_file(dl_url);
};

bot.on('text', (msg) => {
    console.log( '[', msg.from.id, ',', msg.from.first_name, ']:', msg.text);
    const checkBegin=0, checkLong=42, stickerIdBegin=42, stickerIdLong=7;
    if(msg.text.substr( checkBegin, checkLong) == 'https://store.line.me/stickershop/product/'){
        bot.sendMessage(msg.from.id, 'I get your sticker link, let me check it for you.');
        console.log('Get a line sticker store link');
        let StickerID = msg.text.substr( stickerIdBegin, stickerIdLong);
        Stickers_Info(StickerID);
    }else{
        bot.sendMessage(msg.from.id, 'You can send me the stickers store link to me like: \n https://store.line.me/stickershop/product/xxxxxxxx/xx-xxxx');
    }
});


bot.start();