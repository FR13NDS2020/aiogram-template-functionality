from aiogram.types import Message, FSInputFile, InputMediaPhoto, InputMediaVideo
from aiogram import Bot


async def get_audio(message: Message, bot: Bot):
    audio = FSInputFile(path=r"C:\Users\FR13NDS\Documents\Programming\test_data\media\Libercio Feeling Alright.mp3",
                        filename="Audio.mp3")
    await bot.send_audio(message.chat.id, audio=audio)


async def get_document(message: Message, bot: Bot):
    document = FSInputFile(path=r"C:\Users\FR13NDS\Documents\Programming\test_data\media\functional_requirements.pdf",
                           filename="document.pdf")
    await bot.send_document(message.chat.id, document=document, caption='Its document')


async def get_meda_group(message: Message, bot: Bot):
    photo1_mg = InputMediaPhoto(type="photo", media=FSInputFile(
        r"C:\Users\FR13NDS\Documents\Programming\test_data\media\wallpaperflare.jpg"),
                                caption="Its mediagroup")
    photo2_mg = InputMediaPhoto(type="photo", media=FSInputFile(
        r"C:\Users\FR13NDS\Documents\Programming\test_data\media\wallpaperflare2.jpg"))
    video_mg = InputMediaVideo(type="video", media=FSInputFile(
        r"C:\Users\FR13NDS\Documents\Programming\test_data\media\feeling alright - libercio.mp4"))

    media = [photo1_mg, photo2_mg, video_mg]

    await bot.send_media_group(message.chat.id, media)


async def get_photo(message: Message, bot: Bot):
    photo = FSInputFile(path=r"C:\Users\FR13NDS\Documents\Programming\test_data\media\wallpaperflare.jpg",
                        filename="photo.jpg")
    await bot.send_photo(message.chat.id, photo, caption="Photo image")


async def get_sticker(message: Message, bot: Bot):
    sticker = FSInputFile(path=r"C:\Users\FR13NDS\Documents\Programming\test_data\media\sticker.png",
                          filename="Sticker")
    await bot.send_sticker(message.chat.id, sticker)


async def get_video(message: Message, bot: Bot):
    video = FSInputFile(
        path=r"C:\Users\FR13NDS\Documents\Programming\test_data\media\feeling alright - libercio.mp4")
    await bot.send_video(message.chat.id, video)


async def get_video_note(message: Message, bot: Bot):
    video_note = FSInputFile(path=r"C:\Users\FR13NDS\Documents\Programming\test_data\media\video note.mp4")
    await bot.send_video_note(message.chat.id, video_note)


async def get_voice(message: Message, bot: Bot):
    voice = FSInputFile(path=r"C:\Users\FR13NDS\Documents\Programming\test_data\media\Libercio Feeling Alright.mp3")
    await bot.send_voice(message.chat.id, voice)
