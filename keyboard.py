from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from product import *

kb_inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories'),
            InlineKeyboardButton(text='Формула рассчета', callback_data='formulas')
        ]
    ], resize_keyboard=True
)

# kb_shop = InlineKeyboardMarkup(
#     inline_keyboard=[
#         [
#             InlineKeyboardButton(text='Product1', callback_data='product_buying'),
#             InlineKeyboardButton(text='Product2', callback_data='product_buying'),
#             InlineKeyboardButton(text='Product3', callback_data='product_buying'),
#             InlineKeyboardButton(text='Product4', callback_data='product_buying')
#         ]
#     ], resize_keyboard=True
# )
kb_shop = InlineKeyboardMarkup(resize_keyboard=True)
for product in products:
    inline_button_1 = InlineKeyboardButton(text=f'{product[0]}', callback_data='product_buying')
    kb_shop.insert(inline_button_1)

kb_start = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Рассчитать'),
            KeyboardButton(text='Информация')
        ],
        [
            KeyboardButton(text='Регистрация'),
            KeyboardButton(text='Купить')
        ]
    ], resize_keyboard=True
)