from aiogram import Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta

from core.utils.statesform import StatesForm
from core.handlers.apscheduler import send_message_middleware


async def get_form(message: Message, state: FSMContext):
    await message.answer(f"{message.from_user.first_name}, Start filling anket. Write your name")
    await state.set_state(StatesForm.GET_NAME)


async def get_name(message: Message, state: FSMContext):
    await message.answer(f"Your name:\r\n{message.text}\r\nNow enter your female")
    await state.update_data(name=message.text)
    await state.set_state(StatesForm.GET_LAST_NAME)


async def get_last_name(message: Message, state: FSMContext):
    await message.answer(f"Your female: {message.text}\r\nNow type your age")
    await state.update_data(last_name=message.text)
    await state.set_state(StatesForm.GET_AGE)


async def get_age(message: Message, state: FSMContext, apscheduler: AsyncIOScheduler):
    await message.answer(f"Your age: {message.text}")
    context_data = await state.get_data()
    await message.answer(f"Saved data in States machine: \r\n {str(context_data)}")
    name = context_data.get('name')
    last_name = context_data.get('last_name')
    data_user = f"Formed data: \r\nname: {name}\r\nlast_name: {last_name}\r\nage: {message.text}"
    await message.answer(data_user)
    await state.clear()
    apscheduler.add_job(send_message_middleware, trigger="date", run_date=datetime.now() + timedelta(seconds=50),
                        kwargs={'chat_id': message.from_user.id})
