import requests
import json
import sqlite3
import telebot

import bd_groupes

API_TOKEN = '6549201495:AAHNQdJeKWzcvGowqjZ_9zEC5ZM7qKocims'
bot = telebot.TeleBot(API_TOKEN)
@bot.message_handler(commands=["/start"])
def start(message):
    bot.send_message(message.chat.id, "Куye uhe,j ujdjhz ")

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    msg=""
    data_base = sqlite3.connect('groups1.db', check_same_thread = False)
    sql = data_base.cursor()
    user = sql.execute(f"SELECT * FROM ALL_groups WHERE groupe ='{message.text}'").fetchone()
    url1 = requests.get(f"https://umu.sibadi.org/api/Rasp?idGroup={user[1]}&sdate=2024-02-12")
    raspisanie = json.loads(url1.text)
    proverka = raspisanie['data']['rasp'][0]['день_недели']
    msg= "\n" + raspisanie['data']['rasp'][0]['дата'][:10]+"\n"+ raspisanie['data']['rasp'][0]['день_недели']+"\n"
    for item in raspisanie['data']['rasp']:
        if item['день_недели'] != proverka:
            msg +="\n" + item['дата'][:10]+"\n" +item['день_недели']+"\n"
            proverka = item['день_недели']
            msg+=item['начало']+" "+ item['конец']+" "+ item['дисциплина']+" " +item['преподаватель']+" "+ item['аудитория']+"\n"
        else:
            msg+=item['начало'] + " " + item['конец'] + " " + item['дисциплина'] + " " +item['преподаватель'] + " " + item['аудитория']+"\n"
    bot.send_message(message.chat.id,msg)

bot.infinity_polling()

