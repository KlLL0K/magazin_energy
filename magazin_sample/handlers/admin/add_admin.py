from aiogram.dispatcher import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardRemove
from loader import dp
from handlers.user.menu import add_admin
from filters import IsAdmin
from aiogram.utils.callback_data import CallbackData
from magazin_sample.app import Admins

from magazin_sample.keyboards.default.markups import submit_markup, cancel_message, all_right_message

ad_cb = CallbackData('admin', 'action')

@dp.message_handler(IsAdmin(), text=add_admin)
async def get_admin(message: Message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(
        'нажми', callback_data=ad_cb.new(action='add_admin')))
    await message.answer('добавить админа', reply_markup=markup)


@dp.callback_query_handler(IsAdmin(), ad_cb.filter(action='add_admin'))
async def process_answer(query: CallbackQuery, callback_data: dict, state: FSMContext):
    await query.message.answer('Напиши id админа.', reply_markup=ReplyKeyboardRemove())
    await Admins.admins.set()


@dp.message_handler(IsAdmin(), state=Admins.admins)
async def process_submit(message: Message, state: FSMContext):

    async with state.proxy() as data:
        data['admin'] = message.text

    await Admins.next()
    await message.answer('Убедитесь, что не ошиблись в id.', reply_markup=submit_markup())


@dp.message_handler(IsAdmin(), text=cancel_message, state=Admins.submit)
async def process_send_answer(message: Message, state: FSMContext):
    await message.answer('Отменено!', reply_markup=ReplyKeyboardRemove())
    await state.finish()


@dp.message_handler(IsAdmin(), text=all_right_message, state=Admins.submit)
async def process_send_answer(message: Message, state: FSMContext):

    async with state.proxy() as data:
        text = data['admin']
        await message.answer('админ добавлен!', reply_markup=ReplyKeyboardRemove())
        s = open('config.py', 'a+')
        s.truncate(s.tell()-1)
        s.write(f", {text}]")

    await state.finish()

