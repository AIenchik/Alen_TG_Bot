from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from services.chat_gpt import ChatGptService
from prompts.gpt_bot import gpt_role
from states.gpt import GptState
from keyboards.prof_keyboard import make_row_keyboard


router = Router()


@router.message(Command('gpt'))
async def gpt_command(message: types.Message, state: FSMContext):
    photo = types.FSInputFile('images/gpt-4o.jpg')

    await message.answer_photo(
        photo=photo,
        caption='Ты в режиме GPT, задавай вопрос!'
    )
    await state.update_data(previous_messages=[])
    await state.set_state(GptState.gpt)



@router.message(GptState.gpt)
async def gpt_message(
        message: types.Message,
        chat_gpt_service: ChatGptService,
        state: FSMContext
):
    data = await state.get_data()
    previous_messages = data.get('previous_messages', [])
    previous_messages.append(
        {
            'role': 'user',
            'content': message.text
        }
    )
    answer = await chat_gpt_service.ask(
        messages=[
            {
                'role': 'system',
                'content': gpt_role
            },
            *previous_messages
        ]
    )

    previous_messages.append(
        {
            'role': 'assistant',
            'content': answer
        }
    )

    await state.update_data(previous_messages=previous_messages)

    await message.answer(answer, reply_markup=make_row_keyboard(['/start']))