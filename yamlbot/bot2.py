#!# -*- coding: utf-8 -*-
# This module provides quiz game for  Telegram Bot using
# official python-telegram-bot library
# Copyright (C) 2021
# RoboInterativo  <info@robointerativo>
# Aleksey Shilo  <alex.pricker@gmail.com>
# for information use this bot https://web.telegram.org/#/im?p=@robointerativobot
# Данный модуль позволяет заапустить бот викторину в Telegram
# использует официальную библиотеку python-telegram-bot library
# Copyright (C) 2021
# RoboInterativo  <info@robointerativo>
# Алексей Шило  <alex.pricker@gmail.com>
# Для справок используйте бот  https://web.telegram.org/#/im?p=@robointerativobot
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser Public License for more details.
#
# You should have received a copy of the GNU Lesser Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/].
"""
Usage:
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
from gettext import gettext as _
import os
import sys
import logging
from lxml import html
import requests
#import random
import yaml
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import setup








#state_bot = {'tries': 0, 'quest': False, 'q': {}}

user_agent = {'User-agent': 'Mozilla/5.0'}
r = requests.get(headers=user_agent,url='https://vrachi-kostanay.kz/terapevt-kostanay')
h=html.fromstring( r.text)
body=h.getchildren()[1]
blok=body.find_class('blk_box_self')


os.environ.get('TOKEN')
setup.set_up()
LANG = os.environ['LANGUAGE']
print(LANG)
HELP_MESSAGE = _('''
Этот бот позволяет узнать врача и его номер телефона в г. Костанай
Разработан в рамках обучающего курса программирования python,
проекта https://wiki.robointerativo.ru
Автор бота: Алексей Шило AKA Alexpricker, AKA chiefexb,
Актуальная версия бота доступна по ссылке https://github.com/RoboInterativo/armazem-de-robo
Узнать об обучающем проекте можно у бота @roboInterativobot
Доступные команды
/doctor Список врачей
/help эта комманда

Запусти викторину /ask
''')

with open('./config.yml', 'w') as f:

    if os.environ.get('TOKEN') != None:
        config = {'token': os.environ.get('TOKEN')}
        f.write(yaml.dump(config))
        f.close()
    else:

        print(_('''
        Не установлена переменная TOKEN
        для ее установки Набери
        export TOKEN=TOKEN_VALUE
        и попробуй запустить снова.
        '''))
        sys.exit(1)
with open('./config.yml') as f:
    config = yaml.safe_load(f)
    f.close()






logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

def bothelp(update, context):
    """
    Send a message when the command /help is issued.
    Посылает сообщение по комаде /help

    """
    chat_id = update.effective_chat.id

    message = HELP_MESSAGE
    context.bot.send_message(chat_id=chat_id, text=message)


def start(update, context):
    """
    Send a message when the command /start is issued.
    Посылает сообщение по комаде /start
    """
    chat_id = update.effective_chat.id

    context.bot.send_message(chat_id=chat_id, text=HELP_MESSAGE)
    print(update.effective_chat.id)

def doctor(update, context):
    """
    Send a message when the command /doctor is issued.
    Посылает сообщение по комаде /doctor
    """
    chat_id = update.effective_chat.id
    message=etree.dump (blok[0].find_class('blk_text')[0].getchildren()[0].getchildren()[0].getchildren()[0] )
    context.bot.send_message(chat_id=chat_id, text=message)
    print(update.effective_chat.id)







TOKEN = config['token']


UPDATER = Updater(token=TOKEN, use_context=True)
DISPATCHER = UPDATER.dispatcher

START_HANDLER = CommandHandler('start', start)
DOC_HANDLER = CommandHandler('doctor', doctor)
HELP_HANDLER = CommandHandler('help', bothelp)
#MESS_HANDLER = MessageHandler(Filters.regex(''), mess)

DISPATCHER.add_handler(START_HANDLER)
DISPATCHER.add_handler(DOC_HANDLER)
DISPATCHER.add_handler(HELP_HANDLER)
#DISPATCHER.add_handler(MESS_HANDLER)

UPDATER.start_polling()
