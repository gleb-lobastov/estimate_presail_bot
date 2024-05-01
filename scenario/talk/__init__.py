from aiogram import F, types

from services.gpt import gpt_controller

TEXT_INPUT_TYPE = F.content_type == types.ContentType.TEXT


async def scenario_talk(message):
    """
    Arguments:
        message: Сообщение пользователя

    Return:
        None

    Description:
        Переключает бота в режим прямого общения с выбранной gpt моделью
        Функциональность не задокументирована и доступна только админу :)
        Остановка командой /stop
    """
    await message.answer("Задайте системное сообщение")
    system_message = (yield TEXT_INPUT_TYPE).text
    async with (gpt_controller.current(answer=message.answer, system_message=system_message) as gpt):
        await message.answer("Системное сообщение: " + gpt.system_message)
        while True:
            user_input = (yield TEXT_INPUT_TYPE).text
            gpt_resp = await gpt.prompt(user_input)
            await message.answer(gpt_resp)
