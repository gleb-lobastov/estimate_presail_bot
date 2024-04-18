from aiogram import types

from services.gpt import gpt_controller, AVAILABLE_MODELS, MODEL_DESCRIPTIONS


async def scenario_set_gpt(message):
    await message.answer(
        "Выберите модель GPT и введите её имя: \n\n"
        + ",\n".join([f'{key} — {MODEL_DESCRIPTIONS[key]}' for key in AVAILABLE_MODELS.keys()])
    )
    message = yield types.ContentType.TEXT
    selected_model_name = message.text
    if selected_model_name in AVAILABLE_MODELS:
        success = gpt_controller.select(selected_model_name)
        if not success:
            await message.answer("Ошибка выбора модели")
        elif selected_model_name == 'manual_prompt':
            await message.answer("Выбран ручной режим промптинга")
        else:
            await message.answer(f'Выбрана модель {selected_model_name}')
    else:
        await message.answer("Модель с указанным именем отсутствует в списке")
