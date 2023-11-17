import uuid

from aiogram import Bot
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, ShippingOption, ShippingQuery

from core.keyboards.inline import get_payment_keyboard

LV_SHIPPING = ShippingOption(
    id='by',
    title='Ship to Latvia',
    prices=[
        LabeledPrice(
            label="Ship Latvia",
            amount=500
        )
    ]
)

RU_SHIPPING = ShippingOption(
    id='ru',
    title='Ship to Russia',
    prices=[
        LabeledPrice(
            label="Ship Russia",
            amount=400
        )
    ]
)

CH_SHIPPING = ShippingOption(
    id='ch',
    title='Ship to China',
    prices=[
        LabeledPrice(
            label="Ship China",
            amount=200
        )
    ]
)

CITIES_SIPPING = ShippingOption(
    id='countries',
    title="Fast shipping",
    prices=[
        LabeledPrice(
            label="Fast Shiping",
            amount=200
        )
    ]
)


async def shiping_check(shipping_query: ShippingQuery, bot: Bot):
    shipping_options = []
    countries = ["LV", "RU", "CH"]
    if shipping_query.shipping_address.country_code not in countries:
        return await bot.answer_shipping_query(shipping_query.id, ok=False,
                                               error_message="We dont ship to that country")
    if shipping_query.shipping_address.country_code == "LV":
        shipping_options.append(LV_SHIPPING)
    if shipping_query.shipping_address.country_code == "RU":
        shipping_options.append(RU_SHIPPING)
    if shipping_query.shipping_address.country_code == "CH":
        shipping_options.append(CH_SHIPPING)

    cities = ["Moskva", "Riga", "Taiwan"]

    if shipping_query.shipping_address.city in cities:
        shipping_options.append(CITIES_SIPPING)

    await bot.answer_shipping_query(shipping_query.id, ok=True, shipping_options=shipping_options)


async def order(message: Message, bot: Bot):
    await bot.send_invoice(
        chat_id=message.chat.id,
        title="Test Product",
        description="Here is some product description",
        payload="Payment through a bot",
        provider_token="381764678:TEST:71412",
        start_parameter=uuid.uuid4().hex,
        currency="rub",
        prices=[
            LabeledPrice(
                label="Secret info",
                amount=60000
            ),
            LabeledPrice(
                label="PVN",
                amount=20000
            ),
            LabeledPrice(
                label="sale",
                amount=-20000
            ),
            LabeledPrice(
                label="Bonus",
                amount=-40000
            ),
        ],
        max_tip_amount=5000,
        suggested_tip_amounts=[1000, 2000, 3000, 4000],
        provider_data=None,
        photo_url="https://shapka-youtube.ru/wp-content/uploads/2021/02/avatarka-dlya-skaypa-dlya-parney.jpg",
        photo_size=100,
        photo_width=800,
        photo_height=450,
        need_name=False,
        need_phone_number=False,
        need_email=False,
        need_shipping_address=False,
        send_phone_number_to_provider=False,
        send_email_to_provider=False,
        is_flexible=True,
        disable_notification=False,
        protect_content=False,
        reply_to_message_id=None,
        allow_sending_without_reply=True,
        reply_markup=get_payment_keyboard(),
        request_timeout=15
    )


async def pre_checkout_query(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    """here you can write some functionality to test if item is in stock or so on."""
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


async def successful_payment(message: Message):
    msg = f"Thanks for payment {message.successful_payment.total_amount // 100} {message.successful_payment.currency}." \
          f"\r\nour manager recived task and will contact you"
    await message.answer(msg)
