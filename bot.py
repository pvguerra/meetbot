#!/usr/bin/env python3
import time
import telebot
from telebot import types
import datetime
from enum import Enum


# Commands
# create - Cria um evento
# from - Horário inicial do evento
# to - Horário final do evento

def printDebug(message):
    print(str(message.chat.id) + ": " + message.text)


def read_date(message, offset):  # offset is to ignore commands /from and /to
    # assume input is correct...
    day = int(message.text[offset:(offset + 2)])
    month = int(message.text[(offset + 3):(offset + 5)])
    year = int(message.text[(offset + 6):(offset + 10)])
    hour = int(message.text[(offset + 11):(offset + 13)])
    minute = int(message.text[(offset + 14):(offset + 16)])
    print("Data: " + str(day) + " " + str(month) + " " + str(year) + " " + str(hour) + " " + str(minute))
    return datetime.datetime(year, month, day, hour, minute)


def sendKeyboardButton(bot, id):
    markup = types.InlineKeyboardMarkup()
    itembtna = types.InlineKeyboardButton('Participar', callback_data="Participar")
    markup.add(itembtna)
    bot.send_message(id, "Clique para participar do evento:", reply_markup=markup)


def get_data(id):
    return data[id]


TOKEN = '519608788:AAGg-pw9GFc_SMQvlGgxzMlEsGRsxxxyFZI'
bot = telebot.TeleBot(TOKEN)
stateEnum = Enum('state',
                 'none create delete from_create to_create dur_create from_delete to_delete dur_delete')
states = dict()
data = dict()


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    printDebug(message)
    states[message.chat.id] = stateEnum.none
    bot.send_message(message.chat.id, "Bem-vindo ao Meet LAIS Bot! "
                                      "Digite /create para agendar a reunião.")


@bot.message_handler(commands=['create'])
def create(message):
    printDebug(message)
    states[message.chat.id] = stateEnum.create
    data[message.chat.id] = []
    bot.send_message(message.chat.id,
                     "Ótimo! Agora digite o horário inicial do evento. Exemplo: (/from 01/01/2018 08:00) "
                     "e o horário final (/to 01/01/2018 11:00)... ",
                     parse_mode="Markdown")


@bot.message_handler(commands=['delete'])
def delete(message):
    printDebug(message)
    states[message.chat.id] = stateEnum.delete
    data[message.chat.id] = []
    bot.send_message(message.chat.id,
                     "Ótimo! Agora digite o horário inicial do evento. Exemplo: (/from 01/01/2018 08:00) "
                     "e o horário final (/to 01/01/2018 11:00)... ",
                     parse_mode="Markdown")


@bot.message_handler(commands=['from'])
def from_inp(message):
    printDebug(message)
    if states[message.chat.id] == stateEnum.create:
        states[message.chat.id] = stateEnum.from_create
        d = read_date(message, len("/from "))  # print(d.strftime("%A"))
        data[message.chat.id].append(d)
    elif states[message.chat.id] == stateEnum.delete:
        states[message.chat.id] = stateEnum.from_delete
        d = read_date(message, len("/from "))
        data[message.chat.id].append(d)
    else:
        bot.send_message(message.chat.id, "Error")


@bot.message_handler(commands=['to'])
def to_inp(message):
    printDebug(message)
    if states[message.chat.id] == stateEnum.from_create:
        states[message.chat.id] = stateEnum.to_create
        d = read_date(message, len("/to "))
        data[message.chat.id].append(d)
        data[message.chat.id].append(bot.get_chat_members_count(message.chat.id))
        bot.send_message(message.chat.id, "Evento criado!")
        states[message.chat.id] = stateEnum.none
        sendKeyboardButton(bot, message.chat.id)
    elif states[message.chat.id] == stateEnum.from_delete:
        states[message.chat.id] = stateEnum.to_delete
        d = read_date(message, len("/to "))
        data[message.chat.id].append(d)
    else:
        bot.send_message(message.chat.id, "Error")


@bot.message_handler(func=lambda message: True)
def default(message):
    printDebug(message)


bot.polling()