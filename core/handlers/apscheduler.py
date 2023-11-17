from aiogram import Bot


async def send_message_time(bot: Bot):
    await bot.send_message(784098836, f"this message is send after some seconds of bot start time")


async def send_message_cron(bot: Bot):
    await bot.send_message(784098836, f"This message will be send each day in specified day")


async def send_message_interval(bot: Bot):
    await bot.send_message(784098836, f"This message will be send with specified interval of time")


async def send_message_middleware(bot: Bot, chat_id: int):
    await bot.send_message(chat_id, f"Middleware sent message")
