from aiogram.fsm.state import StatesGroup, State


# Cоздаем класс, наследуемый от StatesGroup, для группы состояний FSM
class FSMDefaultChoice(StatesGroup):
    choice = State()  # Состояние ожидания выбора подарка или записи на консультацию


class FSMChoiceGift(StatesGroup):
    choice_gift = State()   # Состояние ожидания выбора подарка.

