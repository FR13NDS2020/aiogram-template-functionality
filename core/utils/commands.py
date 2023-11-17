from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    """default commands in Menu button"""
    commands = [
        BotCommand(
            command='start',
            description='Start bot'
        ),
        BotCommand(
            command='help',
            description='Help'
        ),
        BotCommand(
            command='cancel',
            description="Cancel"
        ),
        BotCommand(
            command='inline',
            description="Inline keyboard"
        ),
        BotCommand(
            command='pay',
            description="buy product"
        ),
        BotCommand(
            command="form",
            description="Start poll"
        ),
        BotCommand(
            command="audio",
            description="Send audio"
        ),
        BotCommand(
            command="document",
            description="Send document"
        ),
        BotCommand(
            command="mediagroup",
            description="Send medagroup"
        ),
        BotCommand(
            command="photo",
            description="Send photo"
        ),
        BotCommand(
            command="sticker",
            description="Send sticker"
        ),
        BotCommand(
            command="video",
            description="Send video"
        ),
        BotCommand(
            command="video_note",
            description="Send videomessage"
        ),
        BotCommand(
            command="voice",
            description="Send voice"
        )
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())
