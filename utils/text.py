from datetime import datetime, timedelta
from config import STREAK_COLORS

TEXTS = {
    'en': {
        'welcome_1': "✨ Welcome to *Friendship Flames 2\\.0* ✨",
        'welcome_2': "Where friendships never fade\\.\\.\\. if you keep them alive\\! 🔥",
        'welcome_3': "Every day with friends is a spark\\. Don't let it die\\! 💫",
        'choose_language': "🌍 Choose your language:",
        'enter_nickname': "👤 Please enter your nickname \\(3\\-20 characters\\):",
        'nickname_taken': "😔 This nickname is already taken\\. Try another\\!",
        'nickname_invalid': "❌ Nickname must be 3\\-20 characters, letters, numbers and underscores only\\.",
        'choose_avatar': "🎭 Choose your avatar\\!",
        'tutorial_1': "🎯 *Tutorial Step 1/3*\n\nLight *Friendship Flames* with your friends\\! 🔥\n\nEach day you both interact keeps the flame alive\\.\n\nThe longer the streak, the more magical it becomes\\! ✨",
        'tutorial_2': "🐣 *Tutorial Step 2/3*\n\nAfter 3 days, your flame hatches a *Seriyochik* \\- a magical creature\\!\n\nFeed it, play with it, evolve it\\!\n\nBut if your streak dies\\.\\.\\. so does your pet\\. 😢",
        'tutorial_3': "🎁 *Tutorial Step 3/3*\n\nInvite friends and earn rewards\\!\n\nComplete quests, collect rare pets, climb the leaderboard\\!\n\n*Ready to start your journey?* 🚀",
        'tutorial_button_next': "Next ➡️",
        'tutorial_button_start': "🔥 Let's Go!",
        'bonus_received': "🎉 *Welcome Bonus\\!*\n\n\\+150 🔥 Sparks\n\\+1 🛡️ Flame Shield\n\\+1 🥚 Starter Pet Egg\n\nYour journey begins now\\! ✨",
        'main_menu': "🏠 *Main Menu*\n\nWhat would you like to do?",
        'profile': "👤 *Your Profile*\n\n{avatar} *{nickname}*\n🆔 ID: `{user_id}`\n🌍 Language: {language}\n\n💰 *Resources*\n🔥 Sparks: *{sparks}*\n⭐ Stars: *{stars}*\n⚡ Energy: *{energy}*/100\n\n🔥 *Streaks*\nActive: *{active_streaks}*\nMax streak: *{max_streak}* days\n\n🐣 *Pets*\nOwned: *{pets_count}*\nHighest level: *{max_pet_level}*\n\n👥 *Social*\nReferrals: *{referrals}*\nFriends: *{friends_count}*\n\n📅 Joined: {joined_date}",
        'streaks_list': "🔥 *Your Friendship Flames*\n\n{streaks}\n\n💡 Keep them alive by interacting daily\\!",
        'no_streaks': "😔 You have no active flames yet\\.\n\nLight your first flame with a friend\\! 🔥",
        'streak_item': "{color} *{days}* days with {avatar} *{nickname}*\n⏰ Next check: {time_left}\n",
        'light_flame': "🔥 *Light a New Flame*\n\nSearch for a friend by username or choose from suggestions:",
        'search_friend': "🔍 Enter friend's @username:",
        'friend_not_found': "😔 User not found\\. Make sure they started the bot\\!",
        'flame_request_sent': "📨 Flame request sent to {avatar} *{nickname}*\\!\n\nWaiting for acceptance\\.\\.\\. 🕐",
        'flame_request_received': "🔥 *New Flame Request\\!*\n\n{avatar} *{nickname}* wants to light a flame with you\\!\n\nAccept?",
        'flame_started': "✨ *Flame Ignited\\!* 🔥\n\nYou and {avatar} *{nickname}* started a new friendship flame\\!\n\nKeep it alive every day\\! 💫",
        'flame_extended': "🔥 *Flame Extended\\!*\n\n{color} *Day {days}* with {avatar} *{nickname}*\\!\n\n\\+{sparks} 🔥 Sparks\n\n{milestone}",
        'flame_dying': "⚠️ *Flame Alert\\!*\n\n{color} Your flame with {avatar} *{nickname}* is dying\\!\n\nOnly *{hours}* hours left\\! 🕐\n\nDon't let it fade\\.\\.\\. 😢",
        'flame_died': "💔 *Flame Extinguished*\n\n😢 Your {days}\\-day flame with {avatar} *{nickname}* has died\\.\\.\\.\n\nBut it's not too late\\! You can revive it within 7 days\\.",
        'can_revive': "💫 *Revival Available*\n\n⏰ Time passed: {time_passed}\n💰 Cost: {cost} ⭐ Stars\n❤️ Lives left: {lives}/3\n\nRevive the flame?",
        'revive_success': "✨ *Flame Revived\\!* 🔥\n\nYour flame with {avatar} *{nickname}* burns again\\!\n\n❤️ Lives remaining: {lives}/3",
        'revive_no_lives': "😔 No lives left for this flame\\.\n\nStart a new one to continue your friendship\\! 🔥",
        'pet_hatched': "🎉 *YOUR PET HATCHED\\!* 🥚→{pet}\n\n{pet} *{pet_name}* joined you\\!\n\nFeed and play with it to evolve\\! ✨",
        'pet_profile': "🐣 *Pet Profile*\n\n{pet} *{pet_name}*\n📊 Level: *{level}* {rarity}\n❤️ Mood: {mood}\n⭐ XP: {xp}/{max_xp}\n🎂 Age: {age} days\n\n{items}\n\n💡 Keep your streak alive to keep your pet happy\\!",
        'pet_feed': "🍖 *Fed {pet_name}\\!*\n\n\\+{xp} XP\n\\-30 🔥 Sparks\n\n{pet} is happy\\! ❤️",
        'pet_pet': "🤗 *Petted {pet_name}\\!*\n\n{pet} purrs with joy\\! ❤️\n\nMood improved\\!",
        'pet_evolved': "✨ *EVOLUTION\\!* ✨\n\n{old_pet} → {new_pet}\n\n*{pet_name}* evolved to level {level}\\!\n\nNew abilities unlocked\\! 🎉",
        'shop': "🛒 *Shop*\n\n{items}",
        'shop_item': "{emoji} *{name}*\n{description}\n💰 Price: {price} {currency}\n",
        'purchase_success': "✅ Purchased {emoji} *{name}*\\!\n\nEnjoy\\! ✨",
        'insufficient_funds': "😔 Not enough {currency}\\.\n\nYou need {required}, but have {current}\\.",
        'referral_info': "👥 *Referral Program*\n\n🔗 Your link:\n`{link}`\n\n📊 *Statistics*\nLevel 1: *{ref1}* \\(50\\-600 🔥 each\\)\nLevel 2: *{ref2}* \\(30%\\)\nLevel 3: *{ref3}* \\(15%\\)\n\n💎 Total earned: *{total}* 🔥\n\n🎁 *Bonuses*\n5 refs → Exclusive pet 🐣\n10 refs → Legendary aura ✨\n25 refs → Unique title 👑\n50 refs → VIP status forever 🌟",
        'new_referral': "🎉 *New Referral\\!*\n\n{avatar} *{nickname}* joined via your link\\!\n\n\\+{reward} 🔥 Sparks\n\n{milestone}",
        'leaderboard': "🏆 *Leaderboard*\n\n{leaders}\n\n{your_position}",
        'leader_item': "{medal} *{nickname}* {avatar}\n{stat}: *{value}*\n",
        'quests': "📋 *Daily Quests*\n\n{daily}\n\n📅 *Weekly Quests*\n\n{weekly}",
        'quest_item': "{status} {emoji} *{name}*\n{description}\n🎁 Reward: {reward}\n{progress}\n",
        'quest_completed': "✅ *Quest Completed\\!*\n\n{emoji} *{name}*\n\n{reward}",
        'gift_sent': "🎁 *Gift Sent\\!*\n\nYou sent {emoji} *{name}* to {avatar} *{nickname}*\\!\n\n{effect}",
        'gift_received': "🎁 *Gift Received\\!*\n\n{avatar} *{nickname}* sent you {emoji} *{name}*\\!\n\n{effect}",
        'share_story': "📱 *Share Your Story\\!*\n\n{image}\n\n🔥 *My longest streak: {days} days\\!*\n\nJoin me in Friendship Flames\\! 🔥",
        'minigame_sparks': "✨ *Spark Catcher\\!*\n\nCatch falling sparks\\! Click as many as you can\\!\n\nTime: 15 seconds ⏱️\n\nReady?",
        'minigame_result': "🎮 *Game Over\\!*\n\nYou caught *{sparks}* sparks\\! 🔥\n\n\\+{sparks} to your balance\\!\n\nEnergy: {energy}/100",
    },
    'ru': {
        'welcome_1': "✨ Добро пожаловать в *Огоньки Дружбы 2\\.0* ✨",
        'welcome_2': "Где дружба никогда не угасает\\.\\.\\. если её поддерживать\\! 🔥",
        'welcome_3': "Каждый день с друзьями \\- это искра\\. Не дай ей погаснуть\\! 💫",
        'choose_language': "🌍 Выбери свой язык:",
        'enter_nickname': "👤 Введи свой никнейм \\(3\\-20 символов\\):",
        'nickname_taken': "😔 Этот никнейм уже занят\\. Попробуй другой\\!",
        'nickname_invalid': "❌ Никнейм должен быть 3\\-20 символов, только буквы, цифры и подчёркивания\\.",
        'choose_avatar': "🎭 Выбери свой аватар\\!",
        'tutorial_1': "🎯 *Обучение Шаг 1/3*\n\nЗажигай *Огоньки Дружбы* с друзьями\\! 🔥\n\nКаждый день ваше общение поддерживает огонёк\\.\n\nЧем дольше серия, тем она волшебнее\\! ✨",
        'tutorial_2': "🐣 *Обучение Шаг 2/3*\n\nЧерез 3 дня из огонька вылупится *Серийчик* \\- магическое существо\\!\n\nКорми его, играй с ним, эволюционируй\\!\n\nНо если серия погаснет\\.\\.\\. питомец тоже\\.\\.\\. 😢",
        'tutorial_3': "🎁 *Обучение Шаг 3/3*\n\nПриглашай друзей и получай награды\\!\n\nВыполняй квесты, коллекционируй редких питомцев, возглавляй лидерборд\\!\n\n*Готов начать своё путешествие?* 🚀",
        'tutorial_button_next': "Далее ➡️",
        'tutorial_button_start': "🔥 Поехали!",
        'bonus_received': "🎉 *Приветственный бонус\\!*\n\n\\+150 🔥 Искр\n\\+1 🛡️ Щит огонька\n\\+1 🥚 Стартовое яйцо питомца\n\nТвоё путешествие начинается\\! ✨",
        'main_menu': "🏠 *Главное меню*\n\nЧто хочешь сделать?",
        'profile': "👤 *Твой профиль*\n\n{avatar} *{nickname}*\n🆔 ID: `{user_id}`\n🌍 Язык: {language}\n\n💰 *Ресурсы*\n🔥 Искры: *{sparks}*\n⭐ Звёзды: *{stars}*\n⚡ Энергия: *{energy}*/100\n\n🔥 *Огоньки*\nАктивных: *{active_streaks}*\nМакс\\. серия: *{max_streak}* дней\n\n🐣 *Питомцы*\nВсего: *{pets_count}*\nМакс\\. уровень: *{max_pet_level}*\n\n👥 *Социальное*\nРефералов: *{referrals}*\nДрузей: *{friends_count}*\n\n📅 Регистрация: {joined_date}",
        'streaks_list': "🔥 *Твои Огоньки Дружбы*\n\n{streaks}\n\n💡 Поддерживай их, общаясь каждый день\\!",
        'no_streaks': "😔 У тебя пока нет активных огоньков\\.\n\nЗажги первый огонёк с другом\\! 🔥",
        'streak_item': "{color} *{days}* дн\\. с {avatar} *{nickname}*\n⏰ След\\. проверка: {time_left}\n",
        'light_flame': "🔥 *Зажечь новый огонёк*\n\nИщи друга по username или выбери из предложенных:",
        'search_friend': "🔍 Введи @username друга:",
        'friend_not_found': "😔 Пользователь не найден\\. Убедись, что он запустил бота\\!",
        'flame_request_sent': "📨 Запрос на огонёк отправлен {avatar} *{nickname}*\\!\n\nОжидаем принятия\\.\\.\\. 🕐",
        'flame_request_received': "🔥 *Новый запрос на огонёк\\!*\n\n{avatar} *{nickname}* хочет зажечь огонёк с тобой\\!\n\nПринять?",
        'flame_started': "✨ *Огонёк зажжён\\!* 🔥\n\nТы и {avatar} *{nickname}* зажгли огонёк дружбы\\!\n\nПоддерживайте его каждый день\\! 💫",
        'flame_extended': "🔥 *Огонёк продлён\\!*\n\n{color} *День {days}* с {avatar} *{nickname}*\\!\n\n\\+{sparks} 🔥 Искр\n\n{milestone}",
        'flame_dying': "⚠️ *Внимание\\! Огонёк гаснет\\!*\n\n{color} Твой огонёк с {avatar} *{nickname}* угасает\\!\n\nОсталось всего *{hours}* часов\\! 🕐\n\nНе дай ему погаснуть\\.\\.\\. 😢",
        'flame_died': "💔 *Огонёк погас*\n\n😢 Твой {days}\\-дневный огонёк с {avatar} *{nickname}* погас\\.\\.\\.\n\nНо ещё не поздно\\! Можно воскресить его в течение 7 дней\\.",
        'can_revive': "💫 *Доступно воскрешение*\n\n⏰ Прошло времени: {time_passed}\n💰 Стоимость: {cost} ⭐ Звёзд\n❤️ Жизней осталось: {lives}/3\n\nВоскресить огонёк?",
        'revive_success': "✨ *Огонёк воскрешён\\!* 🔥\n\nТвой огонёк с {avatar} *{nickname}* снова горит\\!\n\n❤️ Жизней осталось: {lives}/3",
        'revive_no_lives': "😔 Жизней больше нет для этого огонька\\.\n\nНачни новый, чтобы продолжить дружбу\\! 🔥",
        'pet_hatched': "🎉 *ПИТОМЕЦ ВЫЛУПИЛСЯ\\!* 🥚→{pet}\n\n{pet} *{pet_name}* присоединился к тебе\\!\n\nКорми и играй с ним, чтобы он эволюционировал\\! ✨",
        'pet_profile': "🐣 *Профиль питомца*\n\n{pet} *{pet_name}*\n📊 Уровень: *{level}* {rarity}\n❤️ Настроение: {mood}\n⭐ Опыт: {xp}/{max_xp}\n🎂 Возраст: {age} дн\\.\n\n{items}\n\n💡 Поддерживай серию, чтобы питомец был счастлив\\!",
        'pet_feed': "🍖 *Покормил {pet_name}\\!*\n\n\\+{xp} Опыта\n\\-30 🔥 Искр\n\n{pet} доволен\\! ❤️",
        'pet_pet': "🤗 *Погладил {pet_name}\\!*\n\n{pet} мурлычет от радости\\! ❤️\n\nНастроение улучшилось\\!",
        'pet_evolved': "✨ *ЭВОЛЮЦИЯ\\!* ✨\n\n{old_pet} → {new_pet}\n\n*{pet_name}* эволюционировал до уровня {level}\\!\n\nНовые способности разблокированы\\! 🎉",
        'shop': "🛒 *Магазин*\n\n{items}",
        'shop_item': "{emoji} *{name}*\n{description}\n💰 Цена: {price} {currency}\n",
        'purchase_success': "✅ Куплено {emoji} *{name}*\\!\n\nНаслаждайся\\! ✨",
        'insufficient_funds': "😔 Недостаточно {currency}\\.\n\nНужно {required}, а у тебя {current}\\.",
        'referral_info': "👥 *Реферальная программа*\n\n🔗 Твоя ссылка:\n`{link}`\n\n📊 *Статистика*\nУровень 1: *{ref1}* \\(50\\-600 🔥 каждый\\)\nУровень 2: *{ref2}* \\(30%\\)\nУровень 3: *{ref3}* \\(15%\\)\n\n💎 Всего заработано: *{total}* 🔥\n\n🎁 *Бонусы*\n5 рефералов → Эксклюзивный питомец 🐣\n10 рефералов → Легендарная аура ✨\n25 рефералов → Уникальный титул 👑\n50 рефералов → VIP статус навсегда 🌟",
        'new_referral': "🎉 *Новый реферал\\!*\n\n{avatar} *{nickname}* присоединился по твоей ссылке\\!\n\n\\+{reward} 🔥 Искр\n\n{milestone}",
        'leaderboard': "🏆 *Таблица лидеров*\n\n{leaders}\n\n{your_position}",
        'leader_item': "{medal} *{nickname}* {avatar}\n{stat}: *{value}*\n",
        'quests': "📋 *Ежедневные квесты*\n\n{daily}\n\n📅 *Недельные квесты*\n\n{weekly}",
        'quest_item': "{status} {emoji} *{name}*\n{description}\n🎁 Награда: {reward}\n{progress}\n",
        'quest_completed': "✅ *Квест выполнен\\!*\n\n{emoji} *{name}*\n\n{reward}",
        'gift_sent': "🎁 *Подарок отправлен\\!*\n\nТы отправил {emoji} *{name}* для {avatar} *{nickname}*\\!\n\n{effect}",
        'gift_received': "🎁 *Подарок получен\\!*\n\n{avatar} *{nickname}* отправил тебе {emoji} *{name}*\\!\n\n{effect}",
        'share_story': "📱 *Поделись историей\\!*\n\n{image}\n\n🔥 *Моя самая длинная серия: {days} дней\\!*\n\nПрисоединяйся к Огонькам Дружбы\\! 🔥",
        'minigame_sparks': "✨ *Ловец искр\\!*\n\nЛови падающие искры\\! Кликай так быстро, как сможешь\\!\n\nВремя: 15 секунд ⏱️\n\nГотов?",
        'minigame_result': "🎮 *Игра окончена\\!*\n\nТы поймал *{sparks}* искр\\! 🔥\n\n\\+{sparks} на твой счёт\\!\n\nЭнергия: {energy}/100",
    }
}


def get_text(lang: str, key: str, **kwargs) -> str:
    text = TEXTS.get(lang, TEXTS['en']).get(key, TEXTS['en'].get(key, f"Missing: {key}"))
    return text.format(**kwargs) if kwargs else text


def get_streak_color(days: int) -> tuple:
    for min_days, max_days, emoji, name in STREAK_COLORS:
        if min_days <= days <= max_days:
            return emoji, name
    return '🔥', 'Flame'


def format_time_left(seconds: int, lang: str = 'en') -> str:
    if seconds <= 0:
        return "expired" if lang == 'en' else "истекло"
    
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    
    if hours > 0:
        return f"{hours}h {minutes}m" if lang == 'en' else f"{hours}ч {minutes}м"
    return f"{minutes}m" if lang == 'en' else f"{minutes}м"


def escape_markdown(text: str) -> str:
    special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in special_chars:
        text = text.replace(char, f'\\{char}')
    return text
