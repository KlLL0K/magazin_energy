
from aiogram import executor, types
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.dispatcher.filters.state import StatesGroup, State
import handlers
import logging
import config
from loader import dp

logging.basicConfig(level=logging.INFO)

user_message = 'Пользователь'
admin_message = 'Админ'
menu = '/menu'
sos = '/sos'


class CheckoutState(StatesGroup):
    check_cart = State()
    name = State()
    address = State()
    confirm = State()


class ProductState(StatesGroup):
    title = State()
    body = State()
    image = State()
    price = State()
    confirm = State()


class CategoryState(StatesGroup):
    title = State()


class SosState(StatesGroup):
    question = State()
    submit = State()


class AnswerState(StatesGroup):
    answer = State()
    submit = State()


class Admins(StatesGroup):
    admins = State()
    submit = State()


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    if message.from_user.id in config.ADMINS:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row(user_message, admin_message)
    else:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row(menu,sos)
    await message.answer('''Привет! 👋
🤖 Я бот-магазин по продаже товаров любой категории.
🛍️ Чтобы перейти в каталог и выбрать приглянувшиеся товары возпользуйтесь командой /menu или нажмите на кнопку
💰 Пополнить счет можно через Яндекс.кассу, Сбербанк или Qiwi.
❓ Возникли вопросы? Не проблема! Команда или кнопка /sos помогут связаться с админами, которые постараются как можно быстрее откликнуться.
    ''', reply_markup=markup)


@dp.message_handler(text=user_message)
async def user_mode(message: types.Message):
    cid = message.chat.id
    if cid in config.ADMINS:
        config.ADMINS.remove(cid)
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(menu)
    await message.answer('Включен пользовательский режим.', reply_markup=markup)


@dp.message_handler(text=admin_message)
async def admin_mode(message: types.Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(menu,sos)
    cid = message.chat.id
    if cid not in config.ADMINS:
        config.ADMINS.append(cid)

    await message.answer('Включен админский режим.', reply_markup=markup)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)