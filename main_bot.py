import asyncio
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from config import bot_token
import random
import requests
from bs4 import BeautifulSoup


#Create
dp = Dispatcher()
bot = Bot(token=bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

#Погода
def pogoda(name_city, api_key):
  url = f'https://api.openweathermap.org/data/2.5/weather?q={name_city},643&appid={api_key}&units=metric&lang=ru'
  resp = requests.get(url)
  
  if resp.status_code == 200:
      response = resp.json()
      #print(response)
      temp = response['main']['temp']
      weather_city = response['weather'][0]['description']
      return f'Температура в {name_city} - {temp} градусов по цельсию, погода - {weather_city}'
  else:
    return 'Ошибка в названии города'



#Start
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Привет! @{message.from_user.username}")

#Сommans(Описание команд)
@dp.message(Command('commands'))
async def command_start_handler(message: Message) -> None:
    text = 'Я могу многое, например:\n' \
    '1) Подсказать погоду в любом общеизвестном городе(/weather *Название города*);\n' \
    '2) Сыграть с тобой в "Орел и решка"(/random);\n' \
    '3) Рассказать тебе случайный факт(/fact);\n' \
    '4) Я ещё обязательно придумаю что я смогу сделать)..'
    await message.answer(text)

#Орел и решка
@dp.message(Command('random'))
async def command_start_handler(message: Message) -> None:
    if random.randint(1,2) == 1:
        await message.answer('Орел')
    else:
        await message.answer('Решка')

#Прогноз погоды
@dp.message(Command('weather'))
async def command_start_handler(message: Message) -> None:
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer('Пожалуйста, укажите название города после команды.')
        return
    
    city = parts[1]
    text = pogoda(city, '049bf2bb33d6686e88da9baa3b8cfb3c')
    
    if text == 'Ошибка в названии города':
        await message.answer('Перепроверьте название города')
        return
    
    await message.answer(text)

#Факт
@dp.message(Command('fact'))
async def command_start_handler(message: Message) -> None:
        url = "https://randstuff.ru/fact/"
        response = requests.get(url)
        site = response.text
        soup = BeautifulSoup(site, "lxml")
        facts = soup.find('td')
        fact = facts.text.strip()
        await message.answer(fact)

#Эхо(дубль сообщения пользователя)
@dp.message()
async def echo_handler(message: Message) -> None:
    try:
        await message.answer('Я тоже так могу:')
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")

async def main() -> None:
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())