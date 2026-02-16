from config.constants import PetState, PetMood
import math


def calculate_pet_exp_for_level(level: int) -> int:
    return int(100 * (level ** 1.5))


def get_pet_state_emoji(state: PetState) -> str:
    emoji_map = {
        PetState.EGG: "🥚",
        PetState.BABY: "🐣",
        PetState.TEEN: "🐥",
        PetState.ADULT: "🦜",
        PetState.ELDER: "🦅",
        PetState.MYTHIC: "✨🔥🦅"
    }
    return emoji_map.get(state, "🐾")


def get_mood_emoji(mood: PetMood) -> str:
    emoji_map = {
        PetMood.HAPPY: "😊",
        PetMood.NEUTRAL: "😐",
        PetMood.HUNGRY: "😋",
        PetMood.SAD: "😢",
        PetMood.DEPRESSED: "😭"
    }
    return emoji_map.get(mood, "😐")


def check_pet_evolution(level: int, current_state: PetState) -> PetState:
    if level >= 100 and current_state != PetState.MYTHIC:
        return PetState.MYTHIC
    elif level >= 30 and current_state == PetState.ADULT:
        return PetState.ELDER
    elif level >= 10 and current_state == PetState.TEEN:
        return PetState.ADULT
    elif level >= 3 and current_state == PetState.BABY:
        return PetState.TEEN
    
    return current_state
