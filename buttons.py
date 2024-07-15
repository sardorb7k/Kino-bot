from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

admin_first = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Ha"), KeyboardButton(text="Yo'q, keyinroq")],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

ye_or_no = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Ha, to'gri!"), KeyboardButton(text="Yo'q, xatolik bor!")],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

finish_setup = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Yana qo'shish"), KeyboardButton(text="Tugatish")],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)


kodlarni_qidirish = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='🔎 Kodlarni qidirish', url="t.me/kino_bot_uchun_kanal")]
    ]
)

kanalga_otish = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="👍 Kanalga o'tish", url="t.me/kino_bot_uchun_kanal")]
    ]
)