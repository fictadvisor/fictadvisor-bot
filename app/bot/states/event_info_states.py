from aiogram.fsm.state import State, StatesGroup


class AddEventInfoStates(StatesGroup):
    text = State()
    approve = State()
