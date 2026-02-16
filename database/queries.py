import aiosqlite
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List, Tuple
from config import settings
from config.constants import Language, PetRarity, PetState, PetMood, ENERGY_MAX
import json
import structlog

logger = structlog.get_logger()


class Database:
    def __init__(self):
        self.db_path = settings.DATABASE_PATH
    
    async def get_connection(self) -> aiosqlite.Connection:
        conn = await aiosqlite.connect(self.db_path)
        conn.row_factory = aiosqlite.Row
        return conn
    
    async def create_user(
        self,
        user_id: int,
        username: str,
        avatar: str,
        language: Language = Language.RU,
        referrer_id: Optional[int] = None
    ) -> bool:
        try:
            async with await self.get_connection() as db:
                await db.execute(
                    """
                    INSERT INTO users (user_id, username, avatar, language, referrer_id)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (user_id, username, avatar, language.value, referrer_id)
                )
                await db.commit()
            logger.info("user_created", user_id=user_id, username=username)
            return True
        except aiosqlite.IntegrityError:
            return False
    
    async def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        async with await self.get_connection() as db:
            cursor = await db.execute(
                "SELECT * FROM users WHERE user_id = ?",
                (user_id,)
            )
            row = await cursor.fetchone()
            return dict(row) if row else None
    
    async def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        async with await self.get_connection() as db:
            cursor = await db.execute(
                "SELECT * FROM users WHERE username = ? COLLATE NOCASE",
                (username,)
            )
            row = await cursor.fetchone()
            return dict(row) if row else None
    
    async def update_user(self, user_id: int, **fields):
        if not fields:
            return
        
        set_clause = ", ".join([f"{k} = ?" for k in fields.keys()])
        values = list(fields.values()) + [user_id]
        
        async with await self.get_connection() as db:
            await db.execute(
                f"UPDATE users SET {set_clause} WHERE user_id = ?",
                values
            )
            await db.commit()
    
    async def add_sparks(self, user_id: int, amount: int):
        async with await self.get_connection() as db:
            await db.execute(
                "UPDATE users SET sparks = sparks + ? WHERE user_id = ?",
                (amount, user_id)
            )
            await db.commit()
    
    async def add_stars(self, user_id: int, amount: int):
        async with await self.get_connection() as db:
            await db.execute(
                "UPDATE users SET stars = stars + ? WHERE user_id = ?",
                (amount, user_id)
            )
            await db.commit()
    
    async def update_energy(self, user_id: int) -> int:
        async with await self.get_connection() as db:
            cursor = await db.execute(
                "SELECT energy, last_energy_update FROM users WHERE user_id = ?",
                (user_id,)
            )
            row = await cursor.fetchone()
            
            if not row:
                return 0
            
            current_energy = row['energy']
            last_update_str = row['last_energy_update']
            if ' ' in last_update_str and 'T' not in last_update_str:
                last_update_str = last_update_str.replace(' ', 'T')
            last_update = datetime.fromisoformat(last_update_str)
            
            minutes_passed = (datetime.now() - last_update).total_seconds() / 60
            energy_regen = int(minutes_passed)
            
            new_energy = min(current_energy + energy_regen, ENERGY_MAX)
            
            await db.execute(
                "UPDATE users SET energy = ?, last_energy_update = ? WHERE user_id = ?",
                (new_energy, datetime.now(), user_id)
            )
            await db.commit()
            
            return new_energy
    
    async def create_streak_request(self, from_user_id: int, to_user_id: int) -> int:
        async with await self.get_connection() as db:
            cursor = await db.execute(
                """
                INSERT INTO streak_requests (from_user_id, to_user_id, status)
                VALUES (?, ?, 'pending')
                """,
                (from_user_id, to_user_id)
            )
            await db.commit()
            return cursor.lastrowid
    
    async def get_pending_request(self, from_user_id: int, to_user_id: int) -> Optional[Dict]:
        async with await self.get_connection() as db:
            cursor = await db.execute(
                """
                SELECT * FROM streak_requests
                WHERE from_user_id = ? AND to_user_id = ? AND status = 'pending'
                ORDER BY created_at DESC LIMIT 1
                """,
                (from_user_id, to_user_id)
            )
            row = await cursor.fetchone()
            return dict(row) if row else None
    
    async def update_request_status(self, request_id: int, status: str):
        async with await self.get_connection() as db:
            await db.execute(
                "UPDATE streak_requests SET status = ? WHERE id = ?",
                (status, request_id)
            )
            await db.commit()
    
    async def create_streak(self, user1_id: int, user2_id: int) -> int:
        expiry = datetime.now() + timedelta(hours=24)
        async with await self.get_connection() as db:
            cursor = await db.execute(
                """
                INSERT INTO streaks (user1_id, user2_id, expiry, days)
                VALUES (?, ?, ?, 1)
                """,
                (min(user1_id, user2_id), max(user1_id, user2_id), expiry)
            )
            await db.commit()
            return cursor.lastrowid
    
    async def get_streak(self, user1_id: int, user2_id: int) -> Optional[Dict]:
        async with await self.get_connection() as db:
            cursor = await db.execute(
                """
                SELECT * FROM streaks
                WHERE ((user1_id = ? AND user2_id = ?) OR (user1_id = ? AND user2_id = ?))
                AND is_active = 1
                """,
                (min(user1_id, user2_id), max(user1_id, user2_id),
                 min(user1_id, user2_id), max(user1_id, user2_id))
            )
            row = await cursor.fetchone()
            return dict(row) if row else None
    
    async def get_user_streaks(self, user_id: int) -> List[Dict]:
        async with await self.get_connection() as db:
            cursor = await db.execute(
                """
                SELECT s.*, u1.username as user1_name, u1.avatar as user1_avatar,
                       u2.username as user2_name, u2.avatar as user2_avatar
                FROM streaks s
                JOIN users u1 ON s.user1_id = u1.user_id
                JOIN users u2 ON s.user2_id = u2.user_id
                WHERE (s.user1_id = ? OR s.user2_id = ?) AND s.is_active = 1
                ORDER BY s.days DESC
                """,
                (user_id, user_id)
            )
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]
    
    async def extend_streak(self, streak_id: int, user_id: int) -> Tuple[bool, int]:
        async with await self.get_connection() as db:
            cursor = await db.execute(
                "SELECT * FROM streaks WHERE id = ?",
                (streak_id,)
            )
            streak = await cursor.fetchone()
            
            if not streak:
                return False, 0
            
            now = datetime.now()
            
            if streak['user1_id'] == user_id:
                last_extend = streak['last_extend_user1']
                field = 'last_extend_user1'
            else:
                last_extend = streak['last_extend_user2']
                field = 'last_extend_user2'
            
            if last_extend:
                last_extend_dt = datetime.fromisoformat(last_extend)
                if (now - last_extend_dt).total_seconds() < 8 * 3600:
                    return False, 0
            
            both_extended = False
            user1_extended = streak['last_extend_user1']
            user2_extended = streak['last_extend_user2']
            
            if field == 'last_extend_user1':
                user1_extended = now
            else:
                user2_extended = now
            
            if user1_extended and user2_extended:
                user1_dt = datetime.fromisoformat(user1_extended) if isinstance(user1_extended, str) else user1_extended
                user2_dt = datetime.fromisoformat(user2_extended) if isinstance(user2_extended, str) else user2_extended
                
                if (now - user1_dt).total_seconds() < 24 * 3600 and \
                   (now - user2_dt).total_seconds() < 24 * 3600:
                    both_extended = True
            
            new_days = streak['days']
            if both_extended:
                new_days += 1
            
            new_expiry = now + timedelta(hours=24)
            new_max = max(streak['max_days'], new_days)
            
            await db.execute(
                f"""
                UPDATE streaks
                SET {field} = ?, expiry = ?, days = ?, max_days = ?
                WHERE id = ?
                """,
                (now, new_expiry, new_days, new_max, streak_id)
            )
            await db.commit()
            
            return True, new_days
    
    async def expire_streak(self, streak_id: int):
        async with await self.get_connection() as db:
            await db.execute(
                "UPDATE streaks SET is_active = 0 WHERE id = ?",
                (streak_id,)
            )
            await db.commit()
    
    async def create_pet(
        self,
        user_id: int,
        name: str,
        emoji: str,
        rarity: PetRarity,
        streak_id: Optional[int] = None
    ) -> int:
        async with await self.get_connection() as db:
            cursor = await db.execute(
                """
                INSERT INTO pets (user_id, name, emoji, rarity, state, streak_id, hatched_at)
                VALUES (?, ?, ?, ?, 'baby', ?, ?)
                """,
                (user_id, name, emoji, rarity.value, streak_id, datetime.now())
            )
            await db.commit()
            return cursor.lastrowid
    
    async def get_user_pets(self, user_id: int) -> List[Dict]:
        async with await self.get_connection() as db:
            cursor = await db.execute(
                "SELECT * FROM pets WHERE user_id = ? ORDER BY level DESC, exp DESC",
                (user_id,)
            )
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]
    
    async def get_pet(self, pet_id: int) -> Optional[Dict]:
        async with await self.get_connection() as db:
            cursor = await db.execute(
                "SELECT * FROM pets WHERE id = ?",
                (pet_id,)
            )
            row = await cursor.fetchone()
            return dict(row) if row else None
    
    async def update_pet(self, pet_id: int, **fields):
        if not fields:
            return
        
        set_clause = ", ".join([f"{k} = ?" for k in fields.keys()])
        values = list(fields.values()) + [pet_id]
        
        async with await self.get_connection() as db:
            await db.execute(
                f"UPDATE pets SET {set_clause} WHERE id = ?",
                values
            )
            await db.commit()
    
    async def add_achievement(
        self,
        user_id: int,
        type_: str,
        name: str,
        description: str = "",
        emoji: str = "🏆"
    ) -> int:
        async with await self.get_connection() as db:
            cursor = await db.execute(
                """
                INSERT INTO achievements (user_id, type, name, description, emoji)
                VALUES (?, ?, ?, ?, ?)
                """,
                (user_id, type_, name, description, emoji)
            )
            await db.commit()
            return cursor.lastrowid
    
    async def get_user_achievements(self, user_id: int) -> List[Dict]:
        async with await self.get_connection() as db:
            cursor = await db.execute(
                "SELECT * FROM achievements WHERE user_id = ? ORDER BY unlocked_at DESC",
                (user_id,)
            )
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]
    
    async def create_quest(
        self,
        user_id: int,
        type_: str,
        name: str,
        description: str,
        target: int,
        reward_sparks: int = 0,
        reward_stars: int = 0,
        expires_at: Optional[datetime] = None
    ) -> int:
        async with await self.get_connection() as db:
            cursor = await db.execute(
                """
                INSERT INTO quests (user_id, type, name, description, target,
                                    reward_sparks, reward_stars, expires_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (user_id, type_, name, description, target, reward_sparks, reward_stars, expires_at)
            )
            await db.commit()
            return cursor.lastrowid
    
    async def get_user_quests(self, user_id: int, completed: bool = False) -> List[Dict]:
        async with await self.get_connection() as db:
            cursor = await db.execute(
                """
                SELECT * FROM quests
                WHERE user_id = ? AND is_completed = ?
                ORDER BY created_at DESC
                """,
                (user_id, 1 if completed else 0)
            )
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]
    
    async def update_quest_progress(self, quest_id: int, progress: int) -> bool:
        async with await self.get_connection() as db:
            cursor = await db.execute(
                "SELECT target FROM quests WHERE id = ?",
                (quest_id,)
            )
            row = await cursor.fetchone()
            
            if not row:
                return False
            
            is_completed = progress >= row['target']
            
            await db.execute(
                "UPDATE quests SET progress = ?, is_completed = ? WHERE id = ?",
                (progress, 1 if is_completed else 0, quest_id)
            )
            await db.commit()
            
            return is_completed
    
    async def add_inventory_item(self, user_id: int, item_type: str, item_id: str, quantity: int = 1):
        async with await self.get_connection() as db:
            cursor = await db.execute(
                """
                SELECT quantity FROM inventory
                WHERE user_id = ? AND item_type = ? AND item_id = ?
                """,
                (user_id, item_type, item_id)
            )
            row = await cursor.fetchone()
            
            if row:
                await db.execute(
                    """
                    UPDATE inventory SET quantity = quantity + ?
                    WHERE user_id = ? AND item_type = ? AND item_id = ?
                    """,
                    (quantity, user_id, item_type, item_id)
                )
            else:
                await db.execute(
                    """
                    INSERT INTO inventory (user_id, item_type, item_id, quantity)
                    VALUES (?, ?, ?, ?)
                    """,
                    (user_id, item_type, item_id, quantity)
                )
            
            await db.commit()
    
    async def get_inventory(self, user_id: int) -> List[Dict]:
        async with await self.get_connection() as db:
            cursor = await db.execute(
                "SELECT * FROM inventory WHERE user_id = ? ORDER BY acquired_at DESC",
                (user_id,)
            )
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]
    
    async def remove_inventory_item(self, user_id: int, item_type: str, item_id: str, quantity: int = 1) -> bool:
        async with await self.get_connection() as db:
            cursor = await db.execute(
                """
                SELECT quantity FROM inventory
                WHERE user_id = ? AND item_type = ? AND item_id = ?
                """,
                (user_id, item_type, item_id)
            )
            row = await cursor.fetchone()
            
            if not row or row['quantity'] < quantity:
                return False
            
            new_quantity = row['quantity'] - quantity
            
            if new_quantity <= 0:
                await db.execute(
                    """
                    DELETE FROM inventory
                    WHERE user_id = ? AND item_type = ? AND item_id = ?
                    """,
                    (user_id, item_type, item_id)
                )
            else:
                await db.execute(
                    """
                    UPDATE inventory SET quantity = ?
                    WHERE user_id = ? AND item_type = ? AND item_id = ?
                    """,
                    (new_quantity, user_id, item_type, item_id)
                )
            
            await db.commit()
            return True
    
    async def send_gift(self, from_user_id: int, to_user_id: int, gift_type: str, message: str = "") -> int:
        async with await self.get_connection() as db:
            cursor = await db.execute(
                """
                INSERT INTO gifts (from_user_id, to_user_id, gift_type, message)
                VALUES (?, ?, ?, ?)
                """,
                (from_user_id, to_user_id, gift_type, message)
            )
            await db.commit()
            return cursor.lastrowid
    
    async def get_user_gifts(self, user_id: int, opened: bool = False) -> List[Dict]:
        async with await self.get_connection() as db:
            cursor = await db.execute(
                """
                SELECT g.*, u.username as from_username, u.avatar as from_avatar
                FROM gifts g
                JOIN users u ON g.from_user_id = u.user_id
                WHERE g.to_user_id = ? AND g.is_opened = ?
                ORDER BY g.sent_at DESC
                """,
                (user_id, 1 if opened else 0)
            )
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]
    
    async def open_gift(self, gift_id: int):
        async with await self.get_connection() as db:
            await db.execute(
                "UPDATE gifts SET is_opened = 1 WHERE id = ?",
                (gift_id,)
            )
            await db.commit()
    
    async def get_leaderboard(self, order_by: str = "best_streak", limit: int = 100) -> List[Dict]:
        valid_orders = ["best_streak", "total_referrals", "sparks", "level"]
        if order_by not in valid_orders:
            order_by = "best_streak"
        
        async with await self.get_connection() as db:
            cursor = await db.execute(
                f"""
                SELECT user_id, username, avatar, {order_by}, is_premium
                FROM users
                WHERE is_banned = 0
                ORDER BY {order_by} DESC, created_at ASC
                LIMIT ?
                """,
                (limit,)
            )
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]
    
    async def get_referral_count(self, user_id: int) -> int:
        async with await self.get_connection() as db:
            cursor = await db.execute(
                "SELECT COUNT(*) as count FROM users WHERE referrer_id = ?",
                (user_id,)
            )
            row = await cursor.fetchone()
            return row['count'] if row else 0
    
    async def add_referral_reward(
        self,
        user_id: int,
        level: int,
        referral_count: int,
        reward_type: str,
        reward_value: int
    ) -> int:
        async with await self.get_connection() as db:
            cursor = await db.execute(
                """
                INSERT INTO referral_rewards (user_id, level, referral_count, reward_type, reward_value)
                VALUES (?, ?, ?, ?, ?)
                """,
                (user_id, level, referral_count, reward_type, reward_value)
            )
            await db.commit()
            return cursor.lastrowid
    
    async def get_referral_rewards(self, user_id: int) -> List[Dict]:
        async with await self.get_connection() as db:
            cursor = await db.execute(
                "SELECT * FROM referral_rewards WHERE user_id = ? ORDER BY claimed_at DESC",
                (user_id,)
            )
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]
