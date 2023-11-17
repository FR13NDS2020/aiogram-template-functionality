from datetime import datetime
from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject


def office_hours() -> bool:
    return datetime.now().weekday() in (0, 1, 2, 3, 4) and datetime.now().hour in ([i for i in (range(9, 19))])


class OfficeHoursMiddleware(BaseMiddleware):
    """
        Here bot is not reacting to any updates with bot in specified time.
    """

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        if not office_hours():
            return await handler(event, data)

        # await event.answer("Bot currently is not working please wait for working hours")
