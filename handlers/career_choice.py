from aiogram import Router, types
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
    await message.answer('Choose a job', reply_markup=make_row_keyboard(available_jobs))
    await state.set_state(CareerChoice.job)

@router.message(CareerChoice.job)
async def job_chosen(message: types.Message, state: FSMContext):
    await state.update_data(profession=message.text)
    await message.answer('Chose a grade', reply_markup=make_row_keyboard(available_grades))
    await state.set_state(CareerChoice.grade)