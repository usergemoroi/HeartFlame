from typing import Dict, Any
from config.constants import Language

_user_languages: Dict[int, Language] = {}

TRANSLATIONS: Dict[Language, Dict[str, str]] = {
    Language.RU: {
        # Онбординг
        "welcome_1": "✨ **Привет\\!** Добро пожаловать в мир **Огоньков Дружбы**\\! 🔥",
        "welcome_2": "Здесь каждая дружба — это пламя, которое нужно поддерживать каждый день\\! 💫",
        "welcome_3": "Зажигай огоньки с друзьями, выращивай милых существ и создавай незабываемые серии\\! 🌈",
        "choose_language": "🌍 Выбери язык / Choose language:",
        "language_set": "✅ Язык установлен: Русский",
        "ask_username": "Как тебя называть? Введи свой ник:",
        "username_taken": "😔 Этот ник уже занят. Попробуй другой:",
        "username_set": "✨ Отлично, **{}**! Теперь выбери аватарку:",
        "avatar_chosen": "🎨 Прекрасный выбор! Твой аватар: {}",
        "tutorial_1": "📚 **Шаг 1/3**: Найди друга и зажги с ним огонёк! Он должен принять твоё предложение. Обе стороны должны продлевать огонёк каждые 24 часа.",
        "tutorial_2": "📚 **Шаг 2/3**: После 3 дней серии у тебя вылупится милый серийчик 🥚→🐣! Корми его, играй с ним, развивай!",
        "tutorial_3": "📚 **Шаг 3/3**: Зови друзей по реферальной ссылке — получай искры 🔥, редких питомцев и эксклюзивные награды!",
        "onboarding_complete": "🎉 **Поздравляем!**\n\nТы получил:\n• 150 искр 🔥\n• 1 Щит огонька 🛡️\n• Яйцо серийчика 🥚\n\nГотов начать? Жми /menu!",
        
        # Меню
        "menu": "🏠 **Главное меню**\n\nВыбери действие:",
        "btn_profile": "👤 Профиль",
        "btn_streaks": "🔥 Огоньки",
        "btn_friends": "👥 Друзья",
        "btn_pet": "🐾 Питомец",
        "btn_shop": "🛒 Магазин",
        "btn_quests": "⚔️ Квесты",
        "btn_top": "🏆 Топ",
        "btn_referrals": "🎁 Рефералы",
        
        # Профиль
        "profile": "👤 **Твой профиль**\n\n"
                   "{avatar} **{username}**\n"
                   "🆔 ID: `{user_id}`\n\n"
                   "🔥 Искры: **{sparks}**\n"
                   "⭐ Звёзды: **{stars}**\n"
                   "⚡ Энергия: **{energy}/{max_energy}**\n\n"
                   "🔥 Активных огоньков: **{active_streaks}**\n"
                   "📈 Лучшая серия: **{best_streak} дней**\n"
                   "🎯 Уровень: **{level}**\n"
                   "👥 Приглашено друзей: **{referrals}**\n\n"
                   "{achievements}",
        "no_achievements": "_Пока нет достижений_",
        
        # Огоньки
        "streaks_list": "🔥 **Твои огоньки** ({count})\n\n{streaks_text}",
        "streak_item": "{color} **{friend_name}** — {days} дней\n   ⏰ До гашения: {time_left}\n",
        "no_streaks": "У тебя пока нет активных огоньков 😢\n\nЗажги свой первый огонёк с другом!",
        "btn_new_streak": "➕ Зажечь огонёк",
        "btn_extend_all": "⚡ Продлить все",
        "btn_suggest_friends": "💡 Кого зажечь?",
        "search_friend": "🔍 Введи @username друга:",
        "user_not_found": "❌ Пользователь не найден. Попроси друга сначала запустить бота!",
        "cant_streak_yourself": "😅 Нельзя зажечь огонёк с самим собой!",
        "streak_already_exists": "🔥 У вас уже есть активный огонёк с этим другом!",
        "streak_request_sent": "📨 Запрос отправлен **{name}**! Ожидай подтверждения...",
        "streak_request": "🔥 **{from_name}** хочет зажечь с тобой огонёк!\n\nПринимаешь предложение?",
        "streak_accepted": "🎉 **{name}** принял предложение! Огонёк зажжён! 🔥\n\nНе забывай продлевать его каждый день!",
        "streak_rejected": "😢 **{name}** отклонил предложение...",
        "btn_accept": "✅ Принять",
        "btn_reject": "❌ Отклонить",
        "extend_success": "✨ Огонёк продлён! +{sparks} искр 🔥",
        "extend_all_success": "🎊 Все огоньки продлены! +{sparks} искр 🔥\n\nТы поддержал {count} дружб!",
        "extend_cooldown": "⏳ Можно продлевать раз в 8 часов. Следующее продление через: {time}",
        "streak_expired": "💔 **Огонёк погас...**\n\nТвоя серия с **{friend_name}** ({days} дней) прервалась 😢\n\nСерийчик очень расстроен... Восстанови огонёк за {price} ⭐ или начните заново.",
        "streak_milestone": "🎉 **ВЕХА!** 🎉\n\nТвоя серия с **{friend_name}** достигла **{days} дней**!\n\n🎁 Награда:\n{rewards}",
        
        # Питомец
        "pet_status": "🐾 **Твой серийчик**\n\n"
                      "{emoji} **{name}**\n"
                      "🎭 Состояние: {state}\n"
                      "😊 Настроение: {mood}\n"
                      "⭐ Уровень: {level}\n"
                      "📊 Опыт: {exp}/{next_exp}\n"
                      "❤️ Жизни: {lives}/3\n\n"
                      "{status_text}",
        "no_pet": "🥚 У тебя пока нет серийчика!\n\nЗажги огонёк и держи его 3 дня — тогда вылупится твой первый питомец! 💫",
        "btn_feed": "🍖 Покормить (30 🔥)",
        "btn_pet": "🤗 Погладить",
        "btn_play": "🎮 Играть",
        "btn_dance": "💃 Потанцевать",
        "btn_customize": "✨ Кастомизация",
        "feed_success": "🍖 Ням-ням! Серийчик доволен! +{exp} опыта",
        "not_enough_sparks": "😢 Недостаточно искр!",
        "pet_success": "🤗 Серийчику приятно! Настроение улучшилось!",
        "pet_evolved": "🌟 **ЭВОЛЮЦИЯ!** 🌟\n\n{old} → {new}\n\nТвой серийчик стал сильнее!",
        
        # Магазин
        "shop": "🛒 **Магазин**\n\nТвои ресурсы:\n🔥 Искры: {sparks}\n⭐ Звёзды: {stars}\n\nВыбери категорию:",
        "btn_boosts": "⚡ Бусты",
        "btn_pets_shop": "🥚 Питомцы",
        "btn_customization": "✨ Кастомизация",
        "btn_gifts": "🎁 Подарки",
        "item_bought": "✅ Куплено: {item}!",
        
        # Рефералы
        "referrals": "🎁 **Реферальная система**\n\n"
                     "Твоя ссылка:\n`{link}`\n\n"
                     "👥 Приглашено: **{count}**\n"
                     "🔥 Заработано искр: **{earned}**\n\n"
                     "**Награды:**\n{rewards}",
        "referral_joined": "🎉 По твоей ссылке присоединился **{name}**!\n\n+{reward} 🔥",
        
        # Квесты
        "quests": "⚔️ **Квесты**\n\n{quests_text}",
        "quest_completed": "✅ Квест выполнен: {name}\n\n🎁 +{reward}",
        
        # Топ
        "leaderboard": "🏆 **Топ игроков**\n\n{list}",
        
        # Общее
        "back": "◀️ Назад",
        "next": "▶️",
        "prev": "◀️",
        "loading": "⏳ Загрузка...",
        "error": "❌ Произошла ошибка. Попробуй позже.",
    },
    
    Language.EN: {
        # Onboarding
        "welcome_1": "✨ **Hello\\!** Welcome to **Friendship Flames**\\! 🔥",
        "welcome_2": "Here every friendship is a flame that needs to be maintained daily\\! 💫",
        "welcome_3": "Light up flames with friends, grow cute creatures and create unforgettable streaks\\! 🌈",
        "choose_language": "🌍 Choose language / Выбери язык:",
        "language_set": "✅ Language set: English",
        "ask_username": "What should we call you? Enter your nickname:",
        "username_taken": "😔 This nickname is taken. Try another:",
        "username_set": "✨ Great, **{}**! Now choose your avatar:",
        "avatar_chosen": "🎨 Great choice! Your avatar: {}",
        "tutorial_1": "📚 **Step 1/3**: Find a friend and light a flame with them! They must accept your offer. Both sides must extend the flame every 24 hours.",
        "tutorial_2": "📚 **Step 2/3**: After 3 days of streak, your cute pet will hatch 🥚→🐣! Feed it, play with it, develop it!",
        "tutorial_3": "📚 **Step 3/3**: Invite friends with referral link — get sparks 🔥, rare pets and exclusive rewards!",
        "onboarding_complete": "🎉 **Congratulations!**\n\nYou received:\n• 150 sparks 🔥\n• 1 Flame Shield 🛡️\n• Pet egg 🥚\n\nReady to start? Press /menu!",
        
        # Menu
        "menu": "🏠 **Main Menu**\n\nChoose action:",
        "btn_profile": "👤 Profile",
        "btn_streaks": "🔥 Flames",
        "btn_friends": "👥 Friends",
        "btn_pet": "🐾 Pet",
        "btn_shop": "🛒 Shop",
        "btn_quests": "⚔️ Quests",
        "btn_top": "🏆 Top",
        "btn_referrals": "🎁 Referrals",
        
        # Profile
        "profile": "👤 **Your Profile**\n\n"
                   "{avatar} **{username}**\n"
                   "🆔 ID: `{user_id}`\n\n"
                   "🔥 Sparks: **{sparks}**\n"
                   "⭐ Stars: **{stars}**\n"
                   "⚡ Energy: **{energy}/{max_energy}**\n\n"
                   "🔥 Active flames: **{active_streaks}**\n"
                   "📈 Best streak: **{best_streak} days**\n"
                   "🎯 Level: **{level}**\n"
                   "👥 Friends invited: **{referrals}**\n\n"
                   "{achievements}",
        "no_achievements": "_No achievements yet_",
        
        # Streaks
        "streaks_list": "🔥 **Your flames** ({count})\n\n{streaks_text}",
        "streak_item": "{color} **{friend_name}** — {days} days\n   ⏰ Until expires: {time_left}\n",
        "no_streaks": "You don't have active flames yet 😢\n\nLight your first flame with a friend!",
        "btn_new_streak": "➕ New flame",
        "btn_extend_all": "⚡ Extend all",
        "btn_suggest_friends": "💡 Who to light?",
        "search_friend": "🔍 Enter friend's @username:",
        "user_not_found": "❌ User not found. Ask your friend to start the bot first!",
        "cant_streak_yourself": "😅 Can't light a flame with yourself!",
        "streak_already_exists": "🔥 You already have an active flame with this friend!",
        "streak_request_sent": "📨 Request sent to **{name}**! Waiting for confirmation...",
        "streak_request": "🔥 **{from_name}** wants to light a flame with you!\n\nDo you accept?",
        "streak_accepted": "🎉 **{name}** accepted! Flame is lit! 🔥\n\nDon't forget to extend it daily!",
        "streak_rejected": "😢 **{name}** rejected the offer...",
        "btn_accept": "✅ Accept",
        "btn_reject": "❌ Reject",
        "extend_success": "✨ Flame extended! +{sparks} sparks 🔥",
        "extend_all_success": "🎊 All flames extended! +{sparks} sparks 🔥\n\nYou maintained {count} friendships!",
        "extend_cooldown": "⏳ Can extend once per 8 hours. Next extension in: {time}",
        "streak_expired": "💔 **Flame expired...**\n\nYour streak with **{friend_name}** ({days} days) was broken 😢\n\nPet is very sad... Restore flame for {price} ⭐ or start over.",
        "streak_milestone": "🎉 **MILESTONE!** 🎉\n\nYour streak with **{friend_name}** reached **{days} days**!\n\n🎁 Reward:\n{rewards}",
        
        # Pet
        "pet_status": "🐾 **Your Pet**\n\n"
                      "{emoji} **{name}**\n"
                      "🎭 State: {state}\n"
                      "😊 Mood: {mood}\n"
                      "⭐ Level: {level}\n"
                      "📊 Experience: {exp}/{next_exp}\n"
                      "❤️ Lives: {lives}/3\n\n"
                      "{status_text}",
        "no_pet": "🥚 You don't have a pet yet!\n\nLight a flame and keep it for 3 days — then your first pet will hatch! 💫",
        "btn_feed": "🍖 Feed (30 🔥)",
        "btn_pet": "🤗 Pet",
        "btn_play": "🎮 Play",
        "btn_dance": "💃 Dance",
        "btn_customize": "✨ Customize",
        "feed_success": "🍖 Yum-yum! Pet is happy! +{exp} experience",
        "not_enough_sparks": "😢 Not enough sparks!",
        "pet_success": "🤗 Pet is pleased! Mood improved!",
        "pet_evolved": "🌟 **EVOLUTION!** 🌟\n\n{old} → {new}\n\nYour pet became stronger!",
        
        # Shop
        "shop": "🛒 **Shop**\n\nYour resources:\n🔥 Sparks: {sparks}\n⭐ Stars: {stars}\n\nChoose category:",
        "btn_boosts": "⚡ Boosts",
        "btn_pets_shop": "🥚 Pets",
        "btn_customization": "✨ Customization",
        "btn_gifts": "🎁 Gifts",
        "item_bought": "✅ Bought: {item}!",
        
        # Referrals
        "referrals": "🎁 **Referral System**\n\n"
                     "Your link:\n`{link}`\n\n"
                     "👥 Invited: **{count}**\n"
                     "🔥 Earned sparks: **{earned}**\n\n"
                     "**Rewards:**\n{rewards}",
        "referral_joined": "🎉 **{name}** joined via your link!\n\n+{reward} 🔥",
        
        # Quests
        "quests": "⚔️ **Quests**\n\n{quests_text}",
        "quest_completed": "✅ Quest completed: {name}\n\n🎁 +{reward}",
        
        # Top
        "leaderboard": "🏆 **Top Players**\n\n{list}",
        
        # Common
        "back": "◀️ Back",
        "next": "▶️",
        "prev": "◀️",
        "loading": "⏳ Loading...",
        "error": "❌ An error occurred. Try later.",
    },
}


def get_text(key: str, user_id: int = 0, **kwargs) -> str:
    lang = _user_languages.get(user_id, Language.RU)
    text = TRANSLATIONS.get(lang, TRANSLATIONS[Language.RU]).get(key, key)
    
    if kwargs:
        try:
            return text.format(**kwargs)
        except (KeyError, ValueError):
            return text
    return text


def set_user_language(user_id: int, language: Language):
    _user_languages[user_id] = language
