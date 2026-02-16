from aiogram.fsm.state import State, StatesGroup


class OnboardingStates(StatesGroup):
    choosing_language = State()
    entering_username = State()
    choosing_avatar = State()
    tutorial_step = State()


class StreakStates(StatesGroup):
    searching_friend = State()
    confirming_request = State()


class PetStates(StatesGroup):
    naming = State()
    interacting = State()
    customizing = State()


class ShopStates(StatesGroup):
    browsing = State()
    confirming_purchase = State()


class GiftStates(StatesGroup):
    choosing_friend = State()
    choosing_gift = State()
    adding_message = State()
