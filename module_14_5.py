from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboard import *
from product import *
from crud_functions import *
import os
import asyncio

from aiogram.contrib.fsm_storage.memory import MemoryStorage

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет, я бот, помогающий здоровью!', reply_markup=kb_start)


@dp.message_handler(text=['Информация'])
async def set_age(message):
    await message.answer('Я бот, помогающий здоровью!')


@dp.message_handler(text=['Рассчитать'])
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb_inline)


@dp.message_handler(text=['Купить'])
async def get_buying_list(message):
    for product in products_list:
        with open('image/file1.jpg', 'rb') as img_file:
            await message.answer_photo(img_file,
                                       f'Название: {product[1]} | Описание: {product[2]} | Цена: {product[3]}')
    await message.answer('Выберите продукт для покупки:', reply_markup=kb_shop)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('10 x вес(кг) + 6.25 х рост(см) - 5 х возраст(г) + 5')
    await call.answer()


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()
    await call.answer()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age_text=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_growth(message, state):
    await state.update_data(growth_text=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def set_growth(message, state):
    await state.update_data(weight_text=message.text)
    data = await state.get_data()
    calories_norm = 10 * float(data['weight_text']) + 6.25 * float(data['growth_text']) - 5 * float(
        data['age_text']) + 5
    await message.answer(f'Ваша норма калорий в день: {calories_norm}')
    await state.finish()


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()


@dp.message_handler(text='Регистрация')
async def sing_up(message):
    await message.answer('Введите имя пользователя(только латинский алфавит):')
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    check = is_included(message.text)
    if not check:
        RegistrationState.username = message.text
        await message.answer('Введите свой email:')
        await RegistrationState.email.set()
    else:
        await message.answer('Пользователь существует, введите другое имя')
        await state.finish()
        await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    RegistrationState.email = message.text
    await message.answer('Введите свой возраст:')
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    RegistrationState.age = message.text
    add_user(RegistrationState.username, RegistrationState.email, RegistrationState.age)
    await state.finish()


products_list = get_all_products()
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
