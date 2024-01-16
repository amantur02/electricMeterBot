from aiogram.fsm.state import StatesGroup, State


class Resident(StatesGroup):
    home_number = State()
    name = State()
