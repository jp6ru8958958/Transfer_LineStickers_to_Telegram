const TeleBot = require('telebot');


const token = '978232433:AAEH2TzR6z9OkmmUnsM5McagdeOfcA8CkVc';
const bot = new TeleBot(token);

bot.on('text', (msg) => {
    console.log( '[', msg.from.id, ',', msg.from.first_name, ']:',msg.text);
    msg.reply.text(msg.text);
});

bot.on('/hello', (msg) => {
    return bot.sendMessage(msg.from.id, `Hello, ${ msg.from.first_name }!`);
});

bot.start();