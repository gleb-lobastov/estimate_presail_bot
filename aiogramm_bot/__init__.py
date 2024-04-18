from aiogram import Dispatcher
from aiogram import types
from aiogram.filters import CommandStart, Command

from scenario import scenario_presale, scenario_set_gpt
from utils.errors import BotError, handle_errors

from .classes import AiogramScenarioRunner
from .bot import bot

dp = Dispatcher()
scenario = AiogramScenarioRunner()


async def start_polling():
    await dp.start_polling(bot)


@dp.message(CommandStart())
async def command_start(message: types.Message):
    await message.reply("Для начала работы вызовите команду estimate и следуйте инструкциям")


@dp.message(Command("select_llm_model"))
@handle_errors
async def command_set_gpt(message: types.Message):
    """
    Команда запускает сценарий выбора LLM модели для дальнейшей работы

    Args:
        message (types.Message): Сообщение пользователя

    Returns:
        None
    """
    await scenario.play(scenario_set_gpt, message)


@dp.message(Command("estimate"))
@handle_errors
async def command_estimate(message: types.Message):
    """
    Команда запускает сценарий оценки трудозатрат команды фронтенд-разработки для выполнения технического задания

    Args:
        message (types.Message): Сообщение пользователя

    Returns:
        None
    """
    await scenario.play(scenario_presale, message)


@dp.message()
@handle_errors
async def lookup(message: types.Message):
    """
    Обработчик пользовательского ввода в ходе выполнения сценариев

    Args:
        message (types.Message): Сообщение пользователя

    Returns:
        None
    """
    if message.text == "/stop":
        if scenario.active:
            await message.reply(f'Команда {scenario.command} отменена')
            scenario.stop()
        else:
            await message.reply("Нет активных команд")
    elif scenario.active:
        await scenario.step(message)
    else:
        raise BotError("Неизвестная команда")
