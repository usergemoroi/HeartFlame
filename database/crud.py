import aiosqlite
import json
from typing import Optional, List, Dict, Any
from database.init_db import get_db
from utils.time import get_current_timestamp, get_streak_expiry
import random
from config import PET_TYPES, REFERRAL_REWARDS


async def create_user(
    user_id: int,
    username: Optional[str],
    nickname: str,
    avatar: str,
    language: str,
    referrer_id: Optional[int] = None
) -> bool:
    try:
        db = await get_db()
        now = get_current_timestamp()
        
        await db.execute("""
            INSERT INTO users (
                user_id, username, nickname, avatar, language,
                referrer_id, created_at, last_action
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (user_id, username, nickname, avatar, language, referrer_id, now, now))
        
        await db.commit()
        await db.close()
        return True
    except Exception as e:
        print(f"Error creating user: {e}")
        return False


async def get_user(user_id: int) -> Optional[Dict[str, Any]]:
    db = await get_db()
    db.row_factory = aiosqlite.Row
    
    cursor = await db.execute("""
        SELECT * FROM users WHERE user_id = ?
    """, (user_id,))
    
    row = await cursor.fetchone()
    await db.close()
    
    if row:
        return dict(row)
    return None


async def get_user_by_username(username: str) -> Optional[Dict[str, Any]]:
    db = await get_db()
    db.row_factory = aiosqlite.Row
    
    cursor = await db.execute("""
        SELECT * FROM users WHERE username = ? COLLATE NOCASE
    """, (username,))
    
    row = await cursor.fetchone()
    await db.close()
    
    if row:
        return dict(row)
    return None


async def get_user_by_nickname(nickname: str) -> Optional[Dict[str, Any]]:
    db = await get_db()
    db.row_factory = aiosqlite.Row
    
    cursor = await db.execute("""
        SELECT * FROM users WHERE nickname = ? COLLATE NOCASE
    """, (nickname,))
    
    row = await cursor.fetchone()
    await db.close()
    
    if row:
        return dict(row)
    return None


async def update_user(user_id: int, **kwargs) -> bool:
    db = await get_db()
    
    updates = []
    values = []
    
    for key, value in kwargs.items():
        updates.append(f"{key} = ?")
        values.append(value)
    
    values.append(user_id)
    
    await db.execute(f"""
        UPDATE users SET {', '.join(updates)} WHERE user_id = ?
    """, values)
    
    await db.commit()
    await db.close()
    return True


async def update_user_sparks(user_id: int, delta: int) -> int:
    db = await get_db()
    
    cursor = await db.execute("""
        SELECT sparks FROM users WHERE user_id = ?
    """, (user_id,))
    
    row = await cursor.fetchone()
    new_sparks = max(0, row[0] + delta)
    
    await db.execute("""
        UPDATE users SET sparks = ?, total_sparks_earned = total_sparks_earned + ?
        WHERE user_id = ?
    """, (new_sparks, max(0, delta), user_id))
    
    await db.commit()
    await db.close()
    return new_sparks


async def create_flame_request(from_user_id: int, to_user_id: int) -> bool:
    try:
        db = await get_db()
        now = get_current_timestamp()
        
        await db.execute("""
            INSERT OR REPLACE INTO flame_requests (from_user_id, to_user_id, status, created_at)
            VALUES (?, ?, 'pending', ?)
        """, (from_user_id, to_user_id, now))
        
        await db.commit()
        await db.close()
        return True
    except Exception as e:
        print(f"Error creating flame request: {e}")
        return False


async def get_pending_request(from_user_id: int, to_user_id: int) -> Optional[Dict[str, Any]]:
    db = await get_db()
    db.row_factory = aiosqlite.Row
    
    cursor = await db.execute("""
        SELECT * FROM flame_requests 
        WHERE from_user_id = ? AND to_user_id = ? AND status = 'pending'
    """, (from_user_id, to_user_id))
    
    row = await cursor.fetchone()
    await db.close()
    
    if row:
        return dict(row)
    return None


async def accept_flame_request(from_user_id: int, to_user_id: int) -> bool:
    db = await get_db()
    now = get_current_timestamp()
    
    user1_id = min(from_user_id, to_user_id)
    user2_id = max(from_user_id, to_user_id)
    
    expiry = get_streak_expiry(now)
    
    await db.execute("""
        INSERT INTO streaks (
            user1_id, user2_id, days, created_at, last_update, streak_expiry, status
        ) VALUES (?, ?, 1, ?, ?, ?, 'active')
    """, (user1_id, user2_id, now, now, expiry))
    
    await db.execute("""
        UPDATE flame_requests SET status = 'accepted' 
        WHERE from_user_id = ? AND to_user_id = ?
    """, (from_user_id, to_user_id))
    
    await db.execute("""
        UPDATE users SET active_streaks = active_streaks + 1 WHERE user_id IN (?, ?)
    """, (user1_id, user2_id))
    
    await db.commit()
    await db.close()
    return True


async def get_user_streaks(user_id: int, status: str = 'active') -> List[Dict[str, Any]]:
    db = await get_db()
    db.row_factory = aiosqlite.Row
    
    cursor = await db.execute("""
        SELECT s.*, 
               CASE 
                   WHEN s.user1_id = ? THEN s.user2_id 
                   ELSE s.user1_id 
               END as friend_id,
               u.nickname as friend_nickname,
               u.avatar as friend_avatar
        FROM streaks s
        JOIN users u ON (
            CASE 
                WHEN s.user1_id = ? THEN s.user2_id 
                ELSE s.user1_id 
            END = u.user_id
        )
        WHERE (s.user1_id = ? OR s.user2_id = ?) AND s.status = ?
        ORDER BY s.days DESC
    """, (user_id, user_id, user_id, user_id, status))
    
    rows = await cursor.fetchall()
    await db.close()
    
    return [dict(row) for row in rows]


async def extend_streak(streak_id: int) -> Dict[str, Any]:
    db = await get_db()
    now = get_current_timestamp()
    expiry = get_streak_expiry(now)
    
    cursor = await db.execute("""
        SELECT days, user1_id, user2_id FROM streaks WHERE streak_id = ?
    """, (streak_id,))
    
    row = await cursor.fetchone()
    old_days = row[0]
    new_days = old_days + 1
    user1_id, user2_id = row[1], row[2]
    
    await db.execute("""
        UPDATE streaks 
        SET days = ?, last_update = ?, streak_expiry = ?, total_extensions = total_extensions + 1
        WHERE streak_id = ?
    """, (new_days, now, expiry, streak_id))
    
    for uid in [user1_id, user2_id]:
        await db.execute("""
            UPDATE users SET max_streak = MAX(max_streak, ?) WHERE user_id = ?
        """, (new_days, uid))
    
    await db.commit()
    await db.close()
    
    return {'old_days': old_days, 'new_days': new_days}


async def get_streak_by_users(user1_id: int, user2_id: int) -> Optional[Dict[str, Any]]:
    db = await get_db()
    db.row_factory = aiosqlite.Row
    
    uid1 = min(user1_id, user2_id)
    uid2 = max(user1_id, user2_id)
    
    cursor = await db.execute("""
        SELECT * FROM streaks WHERE user1_id = ? AND user2_id = ? AND status = 'active'
    """, (uid1, uid2))
    
    row = await cursor.fetchone()
    await db.close()
    
    if row:
        return dict(row)
    return None


async def kill_streak(streak_id: int) -> bool:
    db = await get_db()
    now = get_current_timestamp()
    
    cursor = await db.execute("""
        SELECT user1_id, user2_id FROM streaks WHERE streak_id = ?
    """, (streak_id,))
    
    row = await cursor.fetchone()
    user1_id, user2_id = row[0], row[1]
    
    await db.execute("""
        UPDATE streaks SET status = 'dead', died_at = ? WHERE streak_id = ?
    """, (now, streak_id))
    
    await db.execute("""
        UPDATE users SET active_streaks = active_streaks - 1 WHERE user_id IN (?, ?)
    """, (user1_id, user2_id))
    
    await db.commit()
    await db.close()
    return True


async def revive_streak(streak_id: int) -> bool:
    db = await get_db()
    now = get_current_timestamp()
    expiry = get_streak_expiry(now)
    
    cursor = await db.execute("""
        SELECT lives_left, user1_id, user2_id FROM streaks WHERE streak_id = ?
    """, (streak_id,))
    
    row = await cursor.fetchone()
    lives = row[0] - 1
    user1_id, user2_id = row[1], row[2]
    
    if lives < 0:
        await db.close()
        return False
    
    await db.execute("""
        UPDATE streaks 
        SET status = 'active', lives_left = ?, last_update = ?, streak_expiry = ?, died_at = 0
        WHERE streak_id = ?
    """, (lives, now, expiry, streak_id))
    
    await db.execute("""
        UPDATE users SET active_streaks = active_streaks + 1 WHERE user_id IN (?, ?)
    """, (user1_id, user2_id))
    
    await db.commit()
    await db.close()
    return True


async def create_pet(streak_id: int, owner_id: int) -> Dict[str, Any]:
    db = await get_db()
    now = get_current_timestamp()
    
    rarity_roll = random.random()
    if rarity_roll < 0.01:
        rarity = 'mythic'
    elif rarity_roll < 0.05:
        rarity = 'legendary'
    elif rarity_roll < 0.15:
        rarity = 'epic'
    elif rarity_roll < 0.35:
        rarity = 'rare'
    else:
        rarity = 'common'
    
    pet_emoji = random.choice(PET_TYPES[rarity])
    pet_name = f"Seriyochik_{random.randint(1000, 9999)}"
    
    cursor = await db.execute("""
        INSERT INTO pets (
            streak_id, owner_id, pet_type, pet_emoji, pet_name, 
            rarity, created_at, last_fed
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (streak_id, owner_id, rarity, pet_emoji, pet_name, rarity, now, now))
    
    pet_id = cursor.lastrowid
    
    await db.execute("""
        UPDATE streaks SET pet_id = ? WHERE streak_id = ?
    """, (pet_id, streak_id))
    
    await db.commit()
    await db.close()
    
    return {
        'pet_id': pet_id,
        'pet_emoji': pet_emoji,
        'pet_name': pet_name,
        'rarity': rarity
    }


async def get_pet(pet_id: int) -> Optional[Dict[str, Any]]:
    db = await get_db()
    db.row_factory = aiosqlite.Row
    
    cursor = await db.execute("""
        SELECT * FROM pets WHERE pet_id = ?
    """, (pet_id,))
    
    row = await cursor.fetchone()
    await db.close()
    
    if row:
        return dict(row)
    return None


async def get_user_pets(user_id: int) -> List[Dict[str, Any]]:
    db = await get_db()
    db.row_factory = aiosqlite.Row
    
    cursor = await db.execute("""
        SELECT * FROM pets WHERE owner_id = ? ORDER BY level DESC, xp DESC
    """, (user_id,))
    
    rows = await cursor.fetchall()
    await db.close()
    
    return [dict(row) for row in rows]


async def feed_pet(pet_id: int, xp_gain: int) -> bool:
    db = await get_db()
    now = get_current_timestamp()
    
    await db.execute("""
        UPDATE pets SET xp = xp + ?, last_fed = ? WHERE pet_id = ?
    """, (xp_gain, now, pet_id))
    
    await db.commit()
    await db.close()
    return True


async def update_pet(pet_id: int, **kwargs) -> bool:
    db = await get_db()
    
    updates = []
    values = []
    
    for key, value in kwargs.items():
        updates.append(f"{key} = ?")
        values.append(value)
    
    values.append(pet_id)
    
    await db.execute(f"""
        UPDATE pets SET {', '.join(updates)} WHERE pet_id = ?
    """, values)
    
    await db.commit()
    await db.close()
    return True


async def create_quest(user_id: int, quest_type: str, quest_name: str, 
                      goal: int, reward_sparks: int, period: str = 'daily') -> bool:
    db = await get_db()
    now = get_current_timestamp()
    
    await db.execute("""
        INSERT INTO quests (
            user_id, quest_type, quest_name, quest_goal, 
            reward_sparks, period, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (user_id, quest_type, quest_name, goal, reward_sparks, period, now))
    
    await db.commit()
    await db.close()
    return True


async def get_user_quests(user_id: int, status: str = 'active') -> List[Dict[str, Any]]:
    db = await get_db()
    db.row_factory = aiosqlite.Row
    
    cursor = await db.execute("""
        SELECT * FROM quests WHERE user_id = ? AND status = ? ORDER BY created_at DESC
    """, (user_id, status))
    
    rows = await cursor.fetchall()
    await db.close()
    
    return [dict(row) for row in rows]


async def update_quest_progress(quest_id: int, progress: int) -> bool:
    db = await get_db()
    
    cursor = await db.execute("""
        SELECT quest_goal FROM quests WHERE quest_id = ?
    """, (quest_id,))
    
    row = await cursor.fetchone()
    goal = row[0]
    
    if progress >= goal:
        now = get_current_timestamp()
        await db.execute("""
            UPDATE quests SET quest_progress = ?, status = 'completed', completed_at = ?
            WHERE quest_id = ?
        """, (progress, now, quest_id))
    else:
        await db.execute("""
            UPDATE quests SET quest_progress = ? WHERE quest_id = ?
        """, (progress, quest_id))
    
    await db.commit()
    await db.close()
    return progress >= goal


async def get_leaderboard(stat: str, limit: int = 10) -> List[Dict[str, Any]]:
    db = await get_db()
    db.row_factory = aiosqlite.Row
    
    stat_map = {
        'streak': 'max_streak',
        'sparks': 'total_sparks_earned',
        'referrals': 'total_referrals'
    }
    
    column = stat_map.get(stat, 'max_streak')
    
    cursor = await db.execute(f"""
        SELECT user_id, nickname, avatar, {column} as value
        FROM users 
        ORDER BY {column} DESC 
        LIMIT ?
    """, (limit,))
    
    rows = await cursor.fetchall()
    await db.close()
    
    return [dict(row) for row in rows]


async def get_user_rank(user_id: int, stat: str) -> int:
    db = await get_db()
    
    stat_map = {
        'streak': 'max_streak',
        'sparks': 'total_sparks_earned',
        'referrals': 'total_referrals'
    }
    
    column = stat_map.get(stat, 'max_streak')
    
    cursor = await db.execute(f"""
        SELECT COUNT(*) FROM users 
        WHERE {column} > (SELECT {column} FROM users WHERE user_id = ?)
    """, (user_id,))
    
    row = await cursor.fetchone()
    await db.close()
    
    return row[0] + 1


async def process_referral(referrer_id: int, new_user_id: int, level: int = 1) -> int:
    db = await get_db()
    
    await db.execute("""
        UPDATE users SET total_referrals = total_referrals + 1 WHERE user_id = ?
    """, (referrer_id,))
    
    cursor = await db.execute("""
        SELECT total_referrals FROM users WHERE user_id = ?
    """, (referrer_id,))
    
    row = await cursor.fetchone()
    total_refs = row[0]
    
    reward = 50
    for threshold, ref_reward in REFERRAL_REWARDS:
        if total_refs <= threshold:
            reward = ref_reward
            break
    
    await db.execute("""
        UPDATE users SET sparks = sparks + ? WHERE user_id = ?
    """, (reward, referrer_id))
    
    await db.commit()
    await db.close()
    
    return reward


async def send_gift(from_user_id: int, to_user_id: int, gift_type: str, gift_data: str = "") -> bool:
    db = await get_db()
    now = get_current_timestamp()
    
    await db.execute("""
        INSERT INTO gifts (from_user_id, to_user_id, gift_type, gift_data, sent_at)
        VALUES (?, ?, ?, ?, ?)
    """, (from_user_id, to_user_id, gift_type, gift_data, now))
    
    await db.commit()
    await db.close()
    return True


async def get_user_gifts(user_id: int, received: bool = False) -> List[Dict[str, Any]]:
    db = await get_db()
    db.row_factory = aiosqlite.Row
    
    cursor = await db.execute("""
        SELECT g.*, u.nickname as sender_nickname, u.avatar as sender_avatar
        FROM gifts g
        JOIN users u ON g.from_user_id = u.user_id
        WHERE g.to_user_id = ? AND g.received = ?
        ORDER BY g.sent_at DESC
    """, (user_id, 1 if received else 0))
    
    rows = await cursor.fetchall()
    await db.close()
    
    return [dict(row) for row in rows]


async def mark_gift_received(gift_id: int) -> bool:
    db = await get_db()
    
    await db.execute("""
        UPDATE gifts SET received = 1 WHERE gift_id = ?
    """, (gift_id,))
    
    await db.commit()
    await db.close()
    return True
