import requests
import json
import sqlite3
import telebot
from telebot import types
import bd_groupes
import raspisanie
from datetime import date
import datetime
API_TOKEN = '6549201495:AAHNQdJeKWzcvGowqjZ_9zEC5ZM7qKocims'
bot = telebot.TeleBot(API_TOKEN)
@bot.message_handler(commands=["start", "update"])
def start(message):
    if message.text == '/start':
        keyboard = types.InlineKeyboardMarkup()
        button_institut = [types.InlineKeyboardButton(text="Исэиу", callback_data="Isy"),
                           types.InlineKeyboardButton(text="Атнист", callback_data="Atnist"),
                           types.InlineKeyboardButton(text="Адпгс", callback_data="Adpgs")]
        keyboard.add(button_institut[0], button_institut[1], button_institut[2])
        bot.send_message(message.chat.id, "Привет, это бот для расписания Сибади\nВыбери свой институт: ",
                         reply_markup=keyboard)
    elif message.text == '/update':
        bd_groupes.base()
        bot.send_message(message.chat.id, "Базы данных групп успешно обновлены!")

@bot.callback_query_handler(func=lambda call: call.data in ['Isy' , 'Atnist', 'Adpgs'])
def isy(call):
    if call.data == 'Isy':
        keyboard = types.InlineKeyboardMarkup()
        for data in range(1,6):
            keyboard.add(types.InlineKeyboardButton(text=f"{data}", callback_data="isy"+"|"+f"{data}"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='Выберите свой курс: ', reply_markup=keyboard)
    if call.data == 'Atnist':
        keyboard = types.InlineKeyboardMarkup()
        for data in range(1,6):
            keyboard.add(types.InlineKeyboardButton(text=f"{data}", callback_data="atnist"+"|"+f"{data}"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='Выберите свой курс: ', reply_markup=keyboard)
    if call.data == 'Adpgs':
        keyboard = types.InlineKeyboardMarkup()
        for data in range(1,7):
            keyboard.add(types.InlineKeyboardButton(text=f"{data}", callback_data="adpgs"+"|"+f"{data}"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='Выберите свой курс: ', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: '|' in call.data )
def print_raspisamie(call):
    data_base = sqlite3.connect('groups1.db', check_same_thread=False)
    sql = data_base.cursor()
    user = sql.execute(f"SELECT * FROM '{call.data.split('|')[0]}' WHERE kurs ='{int(call.data[-1:])}'").fetchall()
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    for data in user:
        keyboard.add(types.InlineKeyboardButton(text=f"{data[0]}", callback_data=f"{data[0]}"+"="))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='Выберите свою группу: ', reply_markup=keyboard)
@bot.callback_query_handler(func=lambda call: call.data[-1:] == '=')
def print_raspisanie(call):
    try:
        call.data = call.data[:-1]
        datetoday=datetime.date.today().weekday()
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add("Завтра")
        data_base = sqlite3.connect('groups1.db', check_same_thread=False)
        sql = data_base.cursor()
        user_groupe_id = sql.execute(f"SELECT * FROM ALL_groups WHERE groupe ='{call.data}'").fetchone()
        one_day = raspisanie.raspisanie(user_groupe_id[1], datetime.date.today())
        print(one_day)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,text=one_day[datetoday])

    except:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="Расписания на эту неделю нет:)")

bot.infinity_polling()