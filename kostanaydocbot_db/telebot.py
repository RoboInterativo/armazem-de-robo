#!# -*- coding: utf-8 -*-
# This module provides search information about doctors in kostanay for  Telegram Bot using
# official python-telegram-bot library
# Copyright (C) 2021
# RoboInterativo  <info@robointerativo>
# Aleksey Shilo  <alex.pricker@gmail.com>
# for information use this bot https://web.telegram.org/#/im?p=@robointerativobot
# Данный модуль позволяет узнать адреса и телефоны враче в г. Костанай через
#  бот  Telegram
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
import requests
import os
from lxml import etree, html
import urllib3
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
import yaml
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    CallbackContext,
)


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)



LOGGER = logging.getLogger(__name__)

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

# Stages
START_KEYBOARD = range(1)
# Callback data

#         InlineKeyboardButton("⏮", callback_data=str(PAGE1)),
#         InlineKeyboardButton("⏪", callback_data=str(PAGE2)),
#         InlineKeyboardButton("⏩", callback_data=str(PAGE4))


def get_links():
    """
    Represent function for loading information from 'https://vrachi-kostanay.kz
    website , links for button.

    Фунция загружает c 'https://vrachi-kostanay.kz информацию о ссылках,
    она используется в меню бота.

    """
    user_agent = {'User-agent': 'Mozilla/5.0'}
    r = requests.get(headers=user_agent, url='https://vrachi-kostanay.kz')
    h = html.fromstring(r.text)
    body = h.getchildren()[1]
    blok = body.find_class('blk blk_button')
    links = []
    num = 0
    for bl in blok[1:43]:
        d = {}
        link = bl.find_class('btn-new block-content')[0]
        url = urllib3.util.parse_url(link.attrib.get('href'))
        d['path'] = url.path.strip('/')
        d['text'] = link.text
        d['num'] = num
        links.append(d)
        num = num+1
    return links






#⏭⏮⏩⏪⏫⏬◀️🔼🔽➡️⬅️⬆️⬇️
def show_doctor(link):
    """
    Represent function for get info about specific doctor from
     'https://vrachi-kostanay.kz using link argument for get it
    website , links for button.

    Фунция загружает c 'https://vrachi-kostanay.kz информацию о конкретном враче,
    link - переменная ссылка на конретного врача.

    """
    user_agent = {'User-agent': 'Mozilla/5.0'}
    r = requests.get(headers=user_agent, url='https://vrachi-kostanay.kz/{}'.format(link))
    h = html.fromstring(r.text)
    body = h.getchildren()[1]
    doc_score = len(body.find_class('blk_box_self'))
    tel_mes = ''
    for el in range(doc_score):
        blok = body.find_class('blk_box_self')
        a = blok[el].find_class('blk_text')[0].getchildren()[0].getchildren()[0].getchildren()[0]
        b = etree.tostring(a, encoding='UTF-8')
        tel = blok[el].find_class('btn-new block-content')[0]
        telephone = tel.attrib['href'].replace('tel:', '')#.replace('+','%2b')
        t = b.decode('UTF-8').replace(u'</b>', '').replace(u'<b>', '').replace(u'<br/>', '\n')
        t2 = t + '\n' + '\n' + 'Телефон: {}'.format(telephone)
        tel_mes = tel_mes+'\n'+t2

    return tel_mes
        #Здесь хотел сделать строку, которая будет выводить сообщением


def start(update: Update, _: CallbackContext) -> int:
    """Send message on `/start`."""
    # Get user that sent /start and log his name
    user = update.message.from_user
    logger.info(
        'Вас приветствует бот "Врачи Костанай". Выберите специализацию врача:',
        user.first_name
        )




    reply_markup = InlineKeyboardMarkup(LINK_PAGE[0])
    # Send message with text and appended InlineKeyboard
    update.message.reply_text("Start handler, Choose a route", reply_markup=reply_markup)
    # Tell ConversationHandler that we're in state `FIRST` now
    return START_KEYBOARD


def zero_page(update: Update, _: CallbackContext) -> int:
    """Send message on `0 page callback send send page1 of doctors list `."""
    # Get user that sent /start and log his name
    """Отправляет информацию с меню первой страницы, списка враче"""
    query = update.callback_query
    query.answer()


    reply_markup = InlineKeyboardMarkup(LINK_PAGE[0])

    # Send message with text and appended InlineKeyboard
    query.edit_message_text(text="Start handler, Choose a route", reply_markup=reply_markup)
    # Tell ConversationHandler that we're in state `FIRST` now
    return START_KEYBOARD

def pages(update: Update, _: CallbackContext) -> int:
    """Send message to user list menu of doctors , callback_data for ident page """
    # Get user that sent /start and log his name
    """Отправляет меню список врачей.
    callback_data - определяет номер страницы списка
    """
    query = update.callback_query
    query_data = query.data
    query.answer()



    reply_markup = InlineKeyboardMarkup(LINK_PAGE[int(query_data)])
    # Send message with text and appended InlineKeyboard
    query.edit_message_text(text="Start handler, Choose a route", reply_markup=reply_markup)
    # Tell ConversationHandler that we're in state `FIRST` now
    return START_KEYBOARD



def doctor(update: Update, _: CallbackContext) -> int:
    """Send message to user about specific doctor user callback_data for ident """
    # Get user that sent /start and log his name
    """Отправляет информацию об конкретном враче пользователю
    callback_data - определяет ссылку на врача
    """
    query = update.callback_query
    #query.edit_message_text(text="Selected option: {}".format(query.data))
    query_data = query.data
    text = show_doctor(query_data)
    query.answer()


    keyboard = [[InlineKeyboardButton("⏮ Назад", callback_data='start')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    query.edit_message_text(text=text, reply_markup=reply_markup)
    # Tell ConversationHandler that we're in state `FIRST` now
    return START_KEYBOARD

def get_keyboard(links):
    """
    Создает на основе полученнных ссылок get_links() меню разбитое на
    страницы, и список CallbackQueryHandlers для обработки этого меню
    ConversationHandler ом

    Create Menu of docts list  get_links() devided by pages and
    CallbackQueryHandler`s list for ConversationHandler object
    """

    link_page = []
    link_pages = []
    num = 0
    st_keyboard = [CallbackQueryHandler(zero_page, pattern='^' + 'start' + '$')]

    for link in links:
        st_keyboard.append(CallbackQueryHandler(doctor, pattern='^' + link['path'] + '$'))
        if len(link_page) == 10:
            st_keyboard.append(CallbackQueryHandler(pages, pattern='^' + str(num) + '$'))
            if num == 0:
                button = [
                    InlineKeyboardButton("⏩", callback_data=str(num+1))
                    ]
            else:
                button = [
                    InlineKeyboardButton("⏮", callback_data='0'),
                    InlineKeyboardButton("⏪", callback_data=str(num-1)),
                    InlineKeyboardButton("⏩", callback_data=str(num+1))
                    ]

            link_page.append(button)
            link_pages.append(link_page)
            link_page = []
            num = num + 1
        else:
            button = [
                InlineKeyboardButton(link['text'], bcallback_data=link['path'])
                ]
            link_page.append(button)



    if len(link_page) > 0:
        st_keyboard.append(
            CallbackQueryHandler(pages,
                                 pattern='^' + str(num) + '$'))
        button = [
            InlineKeyboardButton("⏮", callback_data='0'),
            InlineKeyboardButton("⏪", callback_data=str(num-1))

            ]

        link_page.append(button)
        link_pages.append(link_page)
        link_page = []
        link_pages.append(link_pages)
    return link_pages, st_keyboard



# TOKEN = '1718699727:AAFDW6A4Pq1iISUmM4CaySbIlah4VrGLYhI'
TOKEN = config['token']
LINK_PAGE, start_keyboard = get_keyboard(get_links())



def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Setup conversation handler with the states FIRST and SECOND
    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            START_KEYBOARD: start_keyboard

        },
        fallbacks=[CommandHandler('start', start)],
    )

    # Add ConversationHandler to dispatcher that will be used for handling updates
    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
