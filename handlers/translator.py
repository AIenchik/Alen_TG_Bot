from aiogram import Router, types, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from services.chat_gpt import ChatGptService
from states.translator import TranslatorState
from prompts.persons import PERSONS
from keyboards.prof_keyboard import make_row_keyboard
from keyboards.inline_keyboard import inline_keyboard_translator
from keyboards.keyboards import kb1

router = Router()

available_languages = [
    'Английский',
    'Китайский',
    'Немецкий',
    'Японский'
]

@router.message(Command('translate'))
async def command_translate(message: types.Message, state: FSMContext):
    await state.clear()
    photo = types.FSInputFile('images/gpt-4o.jpg')

    await message.answer_photo(
        photo=photo,
        caption='Выбери язык из предложенных ниже, и я переведу на него твой текст',
        reply_markup=make_row_keyboard(available_languages)
    )
    await state.set_state(TranslatorState.choose_language)

@router.message(TranslatorState.choose_language, F.text.in_(available_languages))
async def language_choose(message: types.Message, state: FSMContext):
    await state.set_data({'language': message.text, 'current_text': ''})
    await message.answer(f'Ты выбрал {message.text} язык, пиши свой текст ниже, и я все сделаю!')
    await state.set_state(TranslatorState.translate)

@router.message(TranslatorState.choose_language)
async def incorrect_language(message: types.Message):
    await message.answer(f'На {message.text} я не смогу перевести, выбери из предложенных!')

@router.message(TranslatorState.translate)
async def translator(message: types.Message, state: FSMContext, chat_gpt_service: ChatGptService):
    await state.update_data({'current_text': message.text})
    data = await state.get_data()
    answer = await chat_gpt_service.ask(
        messages=[
            {
                'role': 'system',
                'content': f'Переведи этот текст {message.text}, на этот язык {data.get("language")}, дай ответ на {data.get("language")} языке, не на русском.'
            },
        ]
    )
    await message.answer(answer, reply_markup=inline_keyboard_translator)

@router.callback_query(F.data == "another_language")
async def another_language(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer('Окей, давай поменяем язык перевода, правила те же, выбери из доступных ниже!',
                         reply_markup=make_row_keyboard(available_languages))
    await state.set_state(TranslatorState.choose_language)
    await callback.answer()

@router.callback_query(F.data == "done")
async def end_translation(callback: types.CallbackQuery, state: FSMContext):
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