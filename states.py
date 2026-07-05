from aiogram.fsm.state import State, StatesGroup


class AddTransaction(StatesGroup):
    """Диалог добавления транзакции — шаг за шагом."""
    amount   = State()   # шаг 1: ввод суммы
    type     = State()   # шаг 2: доход или расход
    category = State()   # шаг 3: выбор категории
    note     = State()   # шаг 4: заметка (опционально)
    confirm  = State()   # шаг 5: подтверждение


class CreateFamily(StatesGroup):
    """Диалог создания семейной группы."""
    waiting_name = State()  # ввод названия группы


class JoinFamily(StatesGroup):
    """Диалог входа в группу по коду."""
    waiting_code = State()  # ввод инвайт-кода
