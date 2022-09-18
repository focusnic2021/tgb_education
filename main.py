import asyncio
import logging
import datetime
from aiogram import Bot, Dispatcher, types, html
from aiogram.dispatcher.filters import CommandObject
from config_reader import config
from db_operation import db_new_user        # db_insert_user

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
# Для записей с типом Secret* необходимо вызывать метод get_secret_value(),
# чтобы получить настоящее содержимое вместо '*******'
bot = Bot(token=config.bot_token.get_secret_value(), parse_mode="HTML")
# Диспетчер
dp = Dispatcher()


def protocol(event_mesaage):
    """Заносит в файл лога принятое сообщение. Сама определяется с датой - либо новый файл, либо дописывает в существующий
    """
    try:
        # открыть файл-протокол, занести сведения:
        file_name = f"{datetime.datetime.now().strftime('%Y%m%d')}.log"
        f = open(file_name, 'a')
        f.write(event_mesaage)
    finally:
        f.close()
    # ...def protocol(event_mesaage)


# Хэндлер на команду /help
@dp.message(commands=["help"])
async def cmd_start(message: types.Message):
    await message.answer("/start - сообщение-приветствие нового пользователя\n"
                         "/help - этот экран")


@dp.message(commands=['start'])
async def start_command(message: types.Message):
    # внести сообщение о событии в протокол и БД:
    event_msg = f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')};" \
                f"{message.from_user.id};" \
                f"{message.from_user.first_name} {message.from_user.last_name};" \
                f"command={message.text};\n"
    # запись в лог-файл:
    protocol(event_msg)
    # запись в БД:
    (result_code, result_text) = db_new_user((
        message.from_user.id,
        message.from_user.first_name,
        message.from_user.last_name,
        datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ))
    print(f"start_command: {result_code = }, {result_text=}")

    # приветствовать пользователя:
    # await message.answer(f"Привет, {message.from_user.first_name} {message.from_user.last_name}!")
    if result_code==0:
        await message.answer(f"Привет, {result_text}!")
    else:
        # запись в лог-файл:
        event_msg = f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')};" \
                    f"{message.from_user.id};" \
                    f"{message.from_user.first_name} {message.from_user.last_name};" \
                    f"ERROR={result_code=} {result_text};\n"
        protocol(event_msg)
        await message.answer(f"Непонятная ошибка, {result_code = }!")
    # ...async def start_command(message: types.Message)



# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

