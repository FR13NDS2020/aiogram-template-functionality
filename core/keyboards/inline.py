from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.utils.callbackdata import MacInfo

select_macbook = InlineKeyboardMarkup(inline_keyboard=[

    [
        InlineKeyboardButton(
            text="Macbook Air 13 M1 2020",
            callback_data="apple_air_13_m1_2020"
        )
    ],
    [
        InlineKeyboardButton(
            text="Macbook Pro 14 M1 pro 2021",
            callback_data="apple_pro_14_m1_2021"
        )
    ],
    [
        InlineKeyboardButton(
            text="Macbook Pro 16 M2 2022",
            callback_data="apple_pro_16_m2_2022"
        )
    ],
    [
        InlineKeyboardButton(
            text="link",
            url="https://google.com"
        )
    ],
    [
        InlineKeyboardButton(
            text="profile",
            url="tg://user?id=784098836"
        )
    ],
])


def get_inline_keyboard():
    builder = InlineKeyboardBuilder()

    builder.button(text="Macbook Air 13 M1 2020", callback_data=MacInfo(model="air", size=13, chip="m1", year=2020))
    builder.button(text="Macbook Pro 14 M1 pro 2021", callback_data=MacInfo(model="pro", size=14, chip="m1", year=2021))
    builder.button(text="Macbook Pro 16 M2 2022", callback_data=MacInfo(model="pro", size=16, chip="m2", year=2022))
    builder.button(text="link", url="https://google.com")
    builder.button(text="profile", url="tg://user?id=784098836")

    builder.adjust(3)
    return builder.as_markup()


def get_payment_keyboard():
    builder = InlineKeyboardBuilder()

    builder.button(text="Pay for the order", pay=True)
    builder.button(text="Link", url="https://google.com")

    return builder.as_markup()
