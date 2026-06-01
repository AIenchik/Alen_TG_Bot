from aiogram import Router, types, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from services.chat_gpt import ChatGptService
from states.talk import TalkState
from prompts.persons import PERSONS
from keyboards.prof_keyboard import make_row_keyboard
from keyboards.inline_keyboard import inline_keyboard_talk
from keyboards.keyboards import kb1

router = Router()

available_persons = [
    'Роберт Дауни Младший',
    'Дональд Трамп',
    'Альберт Эйнштейн'
]


@router.message(Command('talk'))
async def gpt_command(message: types.Message, state: FSMContext):
    photo = types.FSInputFile('images/gpt-4o.jpg')

    await message.answer_photo(
        photo=photo,
        caption='Выбери личность из предложенных, давай пообщаемся!',
        reply_markup=make_row_keyboard(available_persons)
    )
    await state.set_data({'previous_messages': []})
    await state.set_state(TalkState.choice)


@router.message(TalkState.choice, F.text.in_(available_persons))
async def user_choice(message: types.Message, state: FSMContext):
    await state.update_data(chosen_person=message.text)
    data = await state.get_data()
    await message.answer(f'{data.get("chosen_person")}? Хороший выбор! Сейчас его позову.')
    await state.set_state(TalkState.talk)
    await message.answer('Он здесь, пиши первый')


@router.message(TalkState.choice)
async def incorrect_choice(message: types.Message):
    await message.answer('К сожалению его позвать я не могу, выбери из предложенных!',
                         reply_markup=make_row_keyboard(available_persons))


@router.message(TalkState.talk)
async def gpt_message(
        message: types.Message,
        chat_gpt_service: ChatGptService,
        state: FSMContext
):
    data = await state.get_data()
    previous_messages = data.get('previous_messages', [])
    gpt_role = PERSONS[data.get("chosen_person")]
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

    await state.update_data(previous_messages=previous_messages[-10:])

    await message.answer(answer, reply_markup=inline_keyboard_talk)


@router.callback_query(F.data == 'done')
async def end_talk(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(f"""
    Привет, {callback.from_user.first_name}! 👋

    Я GPT-бот 🤖

    Что умею:
    • генерировать случайные факты
    • отвечать на вопросы
    • могу стать известной личностью
    • можем сыграть в викторину

    Выбери действие ниже 👇
    """,
                                  reply_markup=kb1
                                  )
    await callback.answer()
    await state.clear()
