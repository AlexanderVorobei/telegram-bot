import asyncio
import random
import requests
from aiogram import Bot, Dispatcher
from aiogram.types import Message, InlineQuery, InputTextMessageContent, InlineQueryResultArticle


token = 'Type here your telegram token'
weather_api_token = 'Type here your api weather token'
bot = Bot(token)
dispatcher = Dispatcher(bot)


@dispatcher.message_handler(commands=['start'])
async def echo(msg: Message):
    return await msg.reply("Привет... " + msg.from_user.full_name + "!")


@dispatcher.message_handler(commands=['bird'])
async def send_bird(msg: Message):
    random_number = random.choice([1, 2, 3, 4, 5, 6, 7])
    bird_filename = 'birds/' + str(random_number) + '.jpg'
    return await msg.reply_photo(open(bird_filename, 'rb').read())


@dispatcher.message_handler(commands=['music'])
async def send_music(msg: Message):
    music = [
        r"music/irina-bilyk-devochka.mp3",
        r"music/khristina-solovijj-trimajj.mp3",
        r"music/loja-rozy-temno-alye.mp3",
        r"music/maksim-kak-letat.mp3",
        r"music/Polin-Gagarina-Propadi-vse-propadom.mp3",
        r"music/sia-chandelier.mp3",
        r"music/slava-i-stas-pekha-ja-i-ty.mp3"
    ]
    random_music = random.choice(music)
    return await msg.reply_audio(open(random_music, 'rb').read())


@dispatcher.message_handler(commands='weather')
async def get_weather(msg: Message):
    try:
        message_text = msg.text
        message_splitted = message_text.split()
        if len(message_splitted) == 2:
            city = message_splitted[1]
        else:
            return await msg.reply("После /weather  введите название города, например Dnipro")
        print("City ", city)
        url = "http://api.openweathermap.org/data/2.5/weather?q="
        url = url + city
        url = url + "&appid=" + weather_api_token
        url = url + "&units=metric"
        responds = requests.get(url).json()
        temperature = str(responds["main"]["temp"])
    except KeyError:
        return await msg.reply("Не нашел такого города(((")
    return await msg.reply("Температура в " + city + ": " + temperature + "°C")


@dispatcher.inline_handler()
async def inline_echo(inline_query: InlineQuery):
    print(inline_query.query)
    city = inline_query.query
    print("City ", city)
    url = "http://api.openweathermap.org/data/2.5/weather?q="
    url = url + city
    url = url + "&appid=" + weather_api_token
    url = url + "&units=metric"
    responds = requests.get(url).json()
    temperature = str(responds["main"]["temp"])
    icon = str(responds["weather"][0]["icon"])
    # text = inline_query.query or 'echo'
    text = "Температура в " + city + ": " + temperature + "°C"
    input_content = InputTextMessageContent("Температура в " + city + ": " + temperature + "°C")
    result_id = "1"
    icon = "http://openweathermap.org/img/wn/" + icon + "@2x.png"
    item = InlineQueryResultArticle(
        id=result_id,
        title=text,
        input_message_content=input_content,
        thumb_url=icon,
    )
    return await bot.answer_inline_query(inline_query.id, results=[item], cache_time=1)

asyncio.run(dispatcher.start_polling())
