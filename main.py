import asyncio
import logging

import psycopg_pool  # pip install "psycopg[binary]" , pip install psycopg_pool , pip install psycopg
from aiogram import Bot, Dispatcher
from aiogram import F
from aiogram.enums import ContentType
from aiogram.filters import Command, CommandStart
from aiogram.fsm.storage.redis import RedisStorage  # pip install redis
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler  # pip install apscheduler
from apscheduler_di import ContextSchedulerDecorator  # pip install apscheduler-di

from core.settings import settings
from core.filters.iscontact import IsTrueContact
from core.handlers import form
from core.handlers import send_media
from core.handlers.basic import get_start, get_photo, get_hello, get_location, get_inline
from core.handlers.callback import select_macbook
from core.handlers.contact import get_true_contact, get_fake_contact
from core.handlers.pay import order, pre_checkout_query, successful_payment, shiping_check
from core.middlewares.apschedulermiddleware import SchedulerMiddleware
from core.middlewares.countermiddleware import CounterMiddleware
from core.middlewares.dbmiddleware import DbSession
from core.middlewares.example_chat_action_middleware import ExampleChatActionMiddleware
from core.utils.callbackdata import MacInfo
from core.utils.commands import set_commands
from core.utils.statesform import StatesForm

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  # for psycopg


async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(settings.bots.admin_id, text="Bot Started")


async def stop_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text="Bot Stoped")


def create_pool():
    # return await asyncpg.create_pool(user="postgres", password="postgres", database="users",
    #                                  host="127.0.0.1", port=5432, command_timeout=60)  # asyncpg version needs to
    #                                  be async

    return psycopg_pool.AsyncConnectionPool(f"host=127.0.0.1 port=5432 dbname=users user=postgres password=postgres "
                                            f"connect_timeout=60")  # psycopg version


async def start():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s:[%(levelname)s]:%(name)s:"
                               "(%(filename)s).%(funcName)s(%(lineno)d):%(message)s")
    bot = Bot(token=settings.bots.bot_token, parse_mode='HTML')

    pool_connect = create_pool()  # if asyncpg use async

    # Redis Storage

    storage = RedisStorage.from_url('redis://localhost:6379/0')

    # Initialize the Dispatcher
    dp = Dispatcher(storage=storage)

    jobstores = {
        'default': RedisJobStore(jobs_key='dispatched_trips_jobs',
                                 run_times_key='dispatched_trips_running',
                                 host='localhost',
                                 db=2,
                                 port=6379)
    }

    # Register Schedulers
    scheduler = ContextSchedulerDecorator(AsyncIOScheduler(timezone="Europe/Riga", jobstores=jobstores))
    scheduler.ctx.add_instance(bot, declared_class=Bot)
    # scheduler.add_job(apscheduler.send_message_time, trigger='date', run_date=datetime.now() + timedelta(seconds=10))
    # scheduler.add_job(apscheduler.send_message_cron, trigger='cron', hour=datetime.now().hour,
    #                   minute=datetime.now().minute + 1, start_date=datetime.now())
    # scheduler.add_job(apscheduler.send_message_interval, trigger='interval', seconds=60)
    # scheduler.start()

    # Register middlewares
    dp.update.middleware.register(DbSession(pool_connect))
    dp.update.middleware.register(SchedulerMiddleware(scheduler))
    dp.message.middleware.register(CounterMiddleware())
    dp.message.middleware.register(ExampleChatActionMiddleware())
    # dp.update.middleware.register(OfficeHoursMiddleware())

    # Register startup and shutdown procedures
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    # Register commands
    dp.message.register(get_start, CommandStart())
    dp.message.register(get_inline, Command("inline"))
    dp.message.register(order, Command("pay"))
    dp.message.register(form.get_form, Command(commands="form"))
    dp.message.register(send_media.get_audio, Command(commands="audio"), flags={'chat_action': 'upload_document'})
    dp.message.register(send_media.get_document, Command(commands="document"), flags={'chat_action': 'upload_document'})
    dp.message.register(send_media.get_meda_group, Command(commands="mediagroup"),
                        flags={'chat_action': 'upload_photo'})
    dp.message.register(send_media.get_photo, Command(commands="photo"), flags={'chat_action': 'upload_photo'})
    dp.message.register(send_media.get_sticker, Command(commands="sticker"), flags={'chat_action': 'choose_sticker'})
    dp.message.register(send_media.get_video, Command(commands="video"), flags={'chat_action': 'upload_video'})
    dp.message.register(send_media.get_video_note, Command(commands="video_note"),
                        flags={'chat_action': 'upload_video_note'})
    dp.message.register(send_media.get_voice, Command(commands="voice"), flags={'chat_action': 'upload_voice'})

    # Register States
    dp.message.register(form.get_last_name, StatesForm.GET_LAST_NAME)
    dp.message.register(form.get_name, StatesForm.GET_NAME)
    dp.message.register(form.get_age, StatesForm.GET_AGE)

    # Register Messages
    dp.message.register(get_photo, F.photo)
    dp.message.register(get_hello, F.text == "hi")
    dp.message.register(get_true_contact, F.content_type == ContentType.CONTACT, IsTrueContact())
    dp.message.register(get_fake_contact, F.content_type == ContentType.CONTACT)
    dp.message.register(get_location, F.location)

    # Callback registers
    dp.callback_query.register(select_macbook, MacInfo.filter(F.model == "pro"))

    # Additional registers
    dp.message.register(successful_payment, F.content_type == ContentType.SUCCESSFUL_PAYMENT)
    dp.pre_checkout_query.register(pre_checkout_query)
    dp.shipping_query.register(shiping_check)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start())
