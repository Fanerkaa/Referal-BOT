import telebot
from telebot import types
import config

bot = telebot.TeleBot(config.token)
invite_dict = {}
bot_username = "Fanerka"

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("ПРОВЕРИТЬ")
    markup.add(btn1)
    chat_id = message.chat.id
    url = f't.me/{bot_username}?start={chat_id}'
    referral = message.text.split(' ')[1] if len(message.text.split(' ')) > 1 else None
    if referral and referral.isdigit():
        referrer_id = int(referral)
        if chat_id != referrer_id:
            if referrer_id not in invite_dict:
                invite_dict[referrer_id] = []
            if chat_id not in invite_dict[referrer_id]:
                invite_dict[referrer_id].append(chat_id)
            if len(invite_dict[referrer_id]) >= 3:
                bot.send_message(referrer_id, 'Поздравляю вы стали участником розыгрыша.\nВыполнено условие: 3 пользователя перешли по ссылке')
            else:
                bot.send_message(referrer_id, f'Ссылка активна. Перешло {len(invite_dict[referrer_id])} пользователей')
    invite_count = len(invite_dict.get(chat_id, []))
    bot.send_message(chat_id,
                     f'{config.con} \n\nСпонсор: [Группа](Ссылка) \n\nВаша универсальная ссылка: {url} \nПриглашённых друзей: {invite_count}/3',
                     parse_mode='Markdown', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def func(message):
    if message.text == "ПРОВЕРИТЬ":
        chat_id = message.chat.id
        url = f't.me/{bot_username}?start={chat_id}'
        invite_count = len(invite_dict.get(chat_id, []))
        bot.send_message(chat_id,
                         f'{config.con} \n\nСпонсор: [Группа](Ссылка) \n\nВаша универсальная ссылка: {url} \nПриглашённых друзей: {invite_count}/3',
                         parse_mode='Markdown')

# обработчик перехода по ссылке
@bot.message_handler(commands=['start'])
def handle_start(message):
    ref_chat_id = message.text.split(' ')[-1].split('=')[-1]
    if ref_chat_id.isdigit() and int(ref_chat_id) != message.chat.id:
        if message.chat.id not in invite_dict.get(int(ref_chat_id), []):
            invite_dict[int(ref_chat_id)] = invite_dict.get(int(ref_chat_id), []) + [message.chat.id]
    chat_id = message.chat.id
    url = f't.me/{bot_username}?start={chat_id}'
    invite_count = len(invite_dict.get(chat_id, []))
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("ПРОВЕРИТЬ")
    markup.add(btn1)
    bot.send_message(chat_id,
                     f'{config.con} \n\nСпонсор: [Группа](Ссылка) \n\nВаша универсальная ссылка: {url} \nПриглашённых друзей: {invite_count}/3',
                     parse_mode='Markdown', reply_markup=markup)

bot.polling(none_stop=True)