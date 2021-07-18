from telebot import types
import vars

catalog = types.InlineKeyboardMarkup(row_width=5)

catalog.add(types.InlineKeyboardButton('Маме', callback_data=1))
catalog.add(types.InlineKeyboardButton('Папе', callback_data=2))
catalog.add(types.InlineKeyboardButton('Мужу', callback_data=3))
catalog.add(types.InlineKeyboardButton('Жене', callback_data=4))
catalog.add(types.InlineKeyboardButton('Парню', callback_data=5))
catalog.add(types.InlineKeyboardButton('Девушке', callback_data=6))
catalog.add(types.InlineKeyboardButton('Подруге', callback_data=7))
catalog.add(types.InlineKeyboardButton('Другу', callback_data=8))
catalog.add(types.InlineKeyboardButton('Мальчику', callback_data=9))
catalog.add(types.InlineKeyboardButton('Девочке', callback_data=10))
catalog.add(types.InlineKeyboardButton('Бабушке', callback_data=11))
catalog.add(types.InlineKeyboardButton('Дедушке', callback_data=12))
catalog.add(types.InlineKeyboardButton('Сестре', callback_data=13))
catalog.add(types.InlineKeyboardButton('Брату', callback_data=14))
catalog.add(types.InlineKeyboardButton('Руководителю', callback_data=15))
catalog.add(types.InlineKeyboardButton('Коллеге', callback_data=16))
catalog.add(types.InlineKeyboardButton('Учителю', callback_data=17))


# product
def make_product(price, link):
    product = types.InlineKeyboardMarkup(row_width=1)

    product.add(types.InlineKeyboardButton('Цена: {}'.format(price), callback_data=11))
    btn1 = types.InlineKeyboardButton('⬅', callback_data=20)
    btn2 = types.InlineKeyboardButton('{}/{}'.format(vars.NUMBER_OF_PRODUCT + 1, vars.COUNT_IN_SECTION),
                                      callback_data=25)
    btn3 = types.InlineKeyboardButton('➡', callback_data=30)
    product.row(btn1, btn2, btn3)
    product.add(types.InlineKeyboardButton('Подробнее', url=link, callback_data=50))
    product.add(types.InlineKeyboardButton('Добавить в корзину', callback_data=40))
    product.add(types.InlineKeyboardButton('Назад', callback_data=60))

    return product


def make_basket(price, link):
    basket = types.InlineKeyboardMarkup(row_width=1)

    basket.add(types.InlineKeyboardButton('Цена: {}'.format(price), callback_data=100))
    btn1 = types.InlineKeyboardButton('⬅', callback_data=120)
    btn2 = types.InlineKeyboardButton('{}/{}'.format(vars.NUMBER_OF_PRODUCT_BASKET + 1, vars.COUNT_IN_BASKET),
                                      callback_data=125)
    btn3 = types.InlineKeyboardButton('➡', callback_data=130)
    basket.row(btn1, btn2, btn3)
    basket.add(types.InlineKeyboardButton('Подробнее', url=link, callback_data=185))
    basket.add(types.InlineKeyboardButton('Заказать', callback_data=190))
    basket.add(types.InlineKeyboardButton('Удалить из корзины ❌', callback_data=195))
    basket.add(types.InlineKeyboardButton('Продолжить покупки', callback_data=60))

    return basket


def empty_basket():
    basket = types.InlineKeyboardMarkup(row_width=1)
    basket.add(types.InlineKeyboardButton('Продолжить покупки', callback_data=60))

    return basket


def make_order():
    order = types.InlineKeyboardMarkup(row_width=1)
    order.add(types.InlineKeyboardButton('Заберу сам из пункта выдачи', callback_data=200))
    order.add(types.InlineKeyboardButton('Доставка курьером', callback_data=210))
    order.add(types.InlineKeyboardButton('Назад', callback_data=215))

    return order


def prev_step():
    order = types.InlineKeyboardMarkup(row_width=1)
    order.add(types.InlineKeyboardButton('Назад', callback_data=190))

    return order
