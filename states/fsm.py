from aiogram.fsm.state import State, StatesGroup


class OnboardingStates(StatesGroup):
    choosing_language = State()
    entering_nickname = State()
    choosing_avatar = State()
    tutorial_step_1 = State()
    tutorial_step_2 = State()
    tutorial_step_3 = State()


class FlameStates(StatesGroup):
    searching_friend = State()
    confirming_request = State()


class PetStates(StatesGroup):
    viewing_pet = State()
    feeding_pet = State()
    customizing_pet = State()


class ShopStates(StatesGroup):
    browsing = State()
    confirming_purchase = State()


class GiftStates(StatesGroup):
    choosing_friend = State()
    choosing_gift = State()
    confirming_gift = State()


class MiniGameStates(StatesGroup):
    spark_catcher = State()
    playing = State()
