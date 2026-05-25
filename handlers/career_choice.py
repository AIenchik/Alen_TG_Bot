from aiogram import Router, types, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.prof_keyboard import make_row_keyboard

router = Router()

available_jobs = [
    'Programmer',
    'Manager',
    'Designer',
    'Marketing specialist'
]

available_grades = [
    'Intern',
    'Junior',
    'Middle',
    'Senior'
]

class CareerChoice(StatesGroup):
    job = State()
    grade = State()


@router.message(Command('HR'))
async def command_hr(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer('Choose a job', reply_markup=make_row_keyboard(available_jobs))
    await state.set_state(CareerChoice.job)

@router.message(CareerChoice.job, F.text.in_(available_jobs))
async def job_chosen(message: types.Message, state: FSMContext):
    await state.update_data(profession=message.text)
    await message.answer('Chose a grade', reply_markup=make_row_keyboard(available_grades))
    await state.set_state(CareerChoice.grade)

@router.message(CareerChoice.job)
async def job_incorrect(message: types.Message):
    await message.answer('Choose a job from buttons', reply_markup=make_row_keyboard(available_jobs))

@router.message(CareerChoice.grade, F.text.in_(available_grades))
async def grade_chosen(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    await message.answer(f"Congratulations now u r a {user_data.get('profession')}, grade: {message.text}",
                         reply_markup=types.ReplyKeyboardRemove()
    )
    await state.clear()

@router.message(CareerChoice.grade)
async def grade_incorrect(message: types.Message):
    await message.answer('Choose a grade from buttons', reply_markup=make_row_keyboard(available_grades))