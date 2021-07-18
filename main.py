import pandas as pd
from telebot import types, TeleBot
from datetime import datetime, timedelta

import csv_files
import markups
import vars

TOKEN = ''

bot = TeleBot(TOKEN, parse_mode=None)


def check(call):
    if vars.USER_ID == 0:
        bot.answer_callback_query(call.id, show_alert=True, text="Пожалуйста, повторите вызов /start")
        return


# start bot
@bot.message_handler(commands=['start'])
def send_welcome(message):
    vars.USER_ID = message.from_user.id
    vars.USER_NAME = message.from_user.username

    keyboard = types.ReplyKeyboardMarkup(True)
    keyboard.row('Каталог', 'Корзина')
    # keyboard.add('Заказы') TODO
    link = '"http://risovach.ru/upload/2014/08/mem/tvoe-vyrazhenie-lica_59408464_orig_.jpeg"'
    text1 = 'Привет!🌞\nЭтот бот поможет тебе найти подходящий подарок для близких тебе людей<a href={}>.</a>'.format(
        link)
    bot.send_message(message.chat.id, parse_mode='HTML', text=text1, reply_markup=keyboard)
    csv_files.open_csv_for_basket()


data_for_user = pd.DataFrame()
good2 = pd.DataFrame()


def send_message_basket(message):
    vars.NUMBER_OF_PRODUCT_BASKET = 0
    global data_for_user
    data_for_user = csv_files.data2.loc[csv_files.data2['user_id'] == vars.USER_ID]
    vars.COUNT_IN_BASKET = len(data_for_user.index)

    if vars.USER_ID == 0:
        bot.send_message(chat_id=message.chat.id,
                         text='Пожалуйста, повторите вызов /start')
        return

    if vars.COUNT_IN_BASKET <= 0:
        bot.send_message(chat_id=message.chat.id,
                         text='! Ваша корзина пуста !',
                         reply_markup=markups.empty_basket())
        return

    data_product = data_for_user.iloc[[vars.NUMBER_OF_PRODUCT_BASKET]].iloc[0, 1]

    global good2

    good2 = csv_files.data.loc[csv_files.data['id'] == data_product]

    images = '"{}"'.format(good2.iloc[0, -2])
    link = good2.iloc[0, -1]
    name = good2.iloc[0, 1]
    price = good2.iloc[0, 4]
    description = good2.iloc[0, 2]
    text1 = 'Ваша корзина.\n\nНазвание товара: <a href={}>{}</a>\n\nОписание товара:\n\n{}'.format(images, name,
                                                                                                   description)

    bot.send_message(chat_id=message.chat.id, parse_mode='HTML',
                     text=text1,
                     reply_markup=markups.make_basket(price, link))


def edit_message_basket(call):
    global data_for_user
    if vars.COUNT_IN_BASKET <= 0:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode='HTML',
                              text='! Ваша корзина пуста !',
                              reply_markup=markups.empty_basket())
        return

    data_product = data_for_user.iloc[[vars.NUMBER_OF_PRODUCT_BASKET]].iloc[0, 1]

    global good2
    good2 = csv_files.data.loc[csv_files.data['id'] == data_product]

    description = good2.iloc[0, 2]
    images = '"{}"'.format(good2.iloc[0, -2])
    link = good2.iloc[0, -1]
    name = good2.iloc[0, 1]
    price = good2.iloc[0, 4]

    text1 = 'Ваша корзина.\n\nНазвание товара: <a href={}>{}</a>\n\nОписание товара:\n\n{}'.format(images, name,
                                                                                                   description)

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode='HTML',
                          text=text1,
                          reply_markup=markups.make_basket(price, link))


# button prev product in basket
@bot.callback_query_handler(func=lambda call: call.data == '120')
def query_handler(call):
    vars.NUMBER_OF_PRODUCT_BASKET -= 1
    if vars.NUMBER_OF_PRODUCT_BASKET == -1:
        vars.NUMBER_OF_PRODUCT_BASKET = vars.COUNT_IN_BASKET - 1

    edit_message_basket(call)


# button next product in basket
@bot.callback_query_handler(func=lambda call: call.data == '130')
def query_handler(call):
    vars.NUMBER_OF_PRODUCT_BASKET += 1
    if vars.NUMBER_OF_PRODUCT_BASKET >= vars.COUNT_IN_BASKET:
        vars.NUMBER_OF_PRODUCT_BASKET = 0

    edit_message_basket(call)


# button delete product in basket
@bot.callback_query_handler(func=lambda call: call.data == '195')
def query_handler(call):
    global data_for_user

    product_id_delete = data_for_user.iloc[vars.NUMBER_OF_PRODUCT_BASKET, 1]

    data_for_user.drop(index=vars.NUMBER_OF_PRODUCT_BASKET, inplace=True)
    data_for_user.reset_index(drop=True, inplace=True)

    csv_files.data2.drop(index=csv_files.data2.loc[(csv_files.data2['user_id'] == vars.USER_ID) &
                                                   (csv_files.data2['product_id'] == product_id_delete)].index,
                         inplace=True)

    csv_files.data2.to_csv('result.csv', header=False, index=True)
    # csv_files.data2.reset_index(drop=True, inplace=True)

    vars.COUNT_IN_BASKET -= 1
    if vars.NUMBER_OF_PRODUCT_BASKET >= vars.COUNT_IN_BASKET:
        vars.NUMBER_OF_PRODUCT_BASKET = 0

    edit_message_basket(call)
    # update_result_csv()
    # где-то update_products_csv


# get text from menu
@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'каталог':
        bot.send_message(message.chat.id, 'Выберите раздел, чтобы вывести список товаров:',
                         reply_markup=markups.catalog)
    elif message.text.lower() == 'корзина':
        csv_files.open_csv_for_basket()
        send_message_basket(message)


data_in_section = pd.DataFrame()
good = pd.DataFrame()


def edit_message(call):
    global good
    global data_in_section
    good = data_in_section.iloc[vars.NUMBER_OF_PRODUCT]

    images = '"{}"'.format(good['images'])
    link = good['link']
    name = good['name']
    price = good['price']
    description = good['description']
    text1 = 'Товары.\n\nНазвание товара: <a href={}>{}</a>\n\nОписание товара:\n\n{}'.format(images, name, description)

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode='HTML',
                          text=text1,
                          reply_markup=markups.make_product(price, link))


# после выбора раздела
@bot.callback_query_handler(func=lambda call: (0 < int(call.data) <= 17))
def query_handler(call):
    vars.NUMBER_OF_PRODUCT = 0
    vars.SECTION = int(call.data)

    global data_in_section
    data_in_section = csv_files.data.loc[csv_files.data['section'] == vars.SECTION]
    vars.COUNT_IN_SECTION = len(data_in_section.index)

    edit_message(call)


# button "Назад"
@bot.callback_query_handler(func=lambda call: call.data == '60')
def query_handler(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Выберите раздел, чтобы вывести список товаров:",
                          reply_markup=markups.catalog)


# button prev product
@bot.callback_query_handler(func=lambda call: call.data == '20')
def query_handler(call):
    vars.NUMBER_OF_PRODUCT -= 1
    if vars.NUMBER_OF_PRODUCT == -1:
        vars.NUMBER_OF_PRODUCT = vars.COUNT_IN_SECTION - 1

    edit_message(call)


# button next product
@bot.callback_query_handler(func=lambda call: call.data == '30')
def query_handler(call):
    vars.NUMBER_OF_PRODUCT += 1
    if vars.NUMBER_OF_PRODUCT >= vars.COUNT_IN_SECTION:
        vars.NUMBER_OF_PRODUCT = 0

    edit_message(call)


# button Добавить в корзину
@bot.callback_query_handler(func=lambda call: call.data == '40')
def query_handler(call):
    check(call)

    if len(csv_files.data2.loc[(csv_files.data2['user_id'] == vars.USER_ID) &
                               (csv_files.data2['product_id'] == good['id'])]) == 0:

        add_to_csv(good['id'])
        bot.answer_callback_query(call.id, show_alert=True, text="Товар добавлен в корзину!")
    else:
        bot.answer_callback_query(call.id, show_alert=True, text="Этот товар уже есть в корзине!")


def add_to_csv(product_id):
    df = pd.DataFrame({'USER_ID': [vars.USER_ID], 'PRODUCT_ID': [product_id]})
    df.to_csv('result.csv', mode='a', header=False, index=True)
    csv_files.open_csv_for_basket()


# button Заказать
@bot.callback_query_handler(func=lambda call: call.data == '190')
def query_handler(call):
    text1 = 'Выберите способ получения товара:'

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode='HTML',
                          text=text1,
                          reply_markup=markups.make_order())


# button Заказать
@bot.callback_query_handler(func=lambda call: call.data == '215')
def query_handler(call):
    edit_message_basket(call)


def add_to_orders(product_id, way):
    df = pd.DataFrame(
        {'USER_NAME': [vars.USER_NAME], 'USER_ID': [vars.USER_ID], 'PRODUCT_ID': [product_id], 'WAY': way})
    df.to_csv('orders.csv', mode='a', header=False, index=False)
    csv_files.open_csv_for_basket()


# button Заберу сам с пункта выдачи
@bot.callback_query_handler(func=lambda call: (call.data == '200' or call.data == '210'))
def query_handler(call):
    tomorrow_date = (datetime.now() + timedelta(days=1)).strftime("%d.%m.%Y %H:%M")
    c_date, c_time = tomorrow_date.split()
    way = 'Доставка курьером'
    if call.data == '200':
        way = 'Заберу сам из пункта выдачи'
    add_to_orders(good2.iloc[0, 0], way)
    if call.data == '200':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode='HTML',
                              text=f'Ваш товар будет доставлен {c_date} после {c_time}.\n\nСрок хранения: 5 дней.',
                              reply_markup=markups.prev_step())
        return
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode='HTML',
                          text=f'Ваш товар будет доставлен в течение 3-8 часов. Наш курьер свяжится с Вами через '
                               f'telegram.',
                          reply_markup=markups.prev_step())


bot.polling()
