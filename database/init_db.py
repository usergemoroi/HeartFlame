import aiosqlite
from config import settings
import structlog

logger = structlog.get_logger()


async def init_database():
    async with aiosqlite.connect(settings.DATABASE_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                nickname TEXT UNIQUE NOT NULL,
                avatar TEXT NOT NULL,
                language TEXT DEFAULT 'en',
                sparks INTEGER DEFAULT 150,
                stars INTEGER DEFAULT 0,
                energy INTEGER DEFAULT 100,
                referrer_id INTEGER,
                referral_level INTEGER DEFAULT 1,
                total_referrals INTEGER DEFAULT 0,
                max_streak INTEGER DEFAULT 0,
                active_streaks INTEGER DEFAULT 0,
                total_sparks_earned INTEGER DEFAULT 0,
                has_shield BOOLEAN DEFAULT 1,
                vip_until INTEGER DEFAULT 0,
                created_at INTEGER NOT NULL,
                last_action INTEGER NOT NULL,
                tutorial_completed BOOLEAN DEFAULT 0,
                onboarding_step INTEGER DEFAULT 0
            )
        """)
        
        await db.execute("""
            CREATE TABLE IF NOT EXISTS streaks (
                streak_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user1_id INTEGER NOT NULL,
                user2_id INTEGER NOT NULL,
                days INTEGER DEFAULT 0,
                created_at INTEGER NOT NULL,
                last_update INTEGER NOT NULL,
                streak_expiry INTEGER NOT NULL,
                status TEXT DEFAULT 'active',
                lives_left INTEGER DEFAULT 3,
                died_at INTEGER DEFAULT 0,
                total_extensions INTEGER DEFAULT 0,
                pet_id INTEGER,
                FOREIGN KEY (user1_id) REFERENCES users(user_id),
                FOREIGN KEY (user2_id) REFERENCES users(user_id),
                UNIQUE(user1_id, user2_id)
            )
        """)
        
        await db.execute("""
            CREATE TABLE IF NOT EXISTS pets (
                pet_id INTEGER PRIMARY KEY AUTOINCREMENT,
                streak_id INTEGER NOT NULL,
                owner_id INTEGER NOT NULL,
                pet_type TEXT NOT NULL,
                pet_emoji TEXT NOT NULL,
                pet_name TEXT NOT NULL,
                level INTEGER DEFAULT 1,
                xp INTEGER DEFAULT 0,
                rarity TEXT DEFAULT 'common',
                mood TEXT DEFAULT 'happy',
                items TEXT DEFAULT '[]',
                created_at INTEGER NOT NULL,
                last_fed INTEGER DEFAULT 0,
                evolution_stage INTEGER DEFAULT 1,
                FOREIGN KEY (streak_id) REFERENCES streaks(streak_id),
                FOREIGN KEY (owner_id) REFERENCES users(user_id)
            )
        """)
        
        await db.execute("""
            CREATE TABLE IF NOT EXISTS flame_requests (
                request_id INTEGER PRIMARY KEY AUTOINCREMENT,
                from_user_id INTEGER NOT NULL,
                to_user_id INTEGER NOT NULL,
                status TEXT DEFAULT 'pending',
                created_at INTEGER NOT NULL,
                FOREIGN KEY (from_user_id) REFERENCES users(user_id),
                FOREIGN KEY (to_user_id) REFERENCES users(user_id),
                UNIQUE(from_user_id, to_user_id)
            )
        """)
        
        await db.execute("""
            CREATE TABLE IF NOT EXISTS gifts (
                gift_id INTEGER PRIMARY KEY AUTOINCREMENT,
                from_user_id INTEGER NOT NULL,
                to_user_id INTEGER NOT NULL,
                gift_type TEXT NOT NULL,
                gift_data TEXT,
                sent_at INTEGER NOT NULL,
                received BOOLEAN DEFAULT 0,
                FOREIGN KEY (from_user_id) REFERENCES users(user_id),
                FOREIGN KEY (to_user_id) REFERENCES users(user_id)
            )
        """)
        
        await db.execute("""
            CREATE TABLE IF NOT EXISTS quests (
                quest_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                quest_type TEXT NOT NULL,
                quest_name TEXT NOT NULL,
                quest_goal INTEGER NOT NULL,
                quest_progress INTEGER DEFAULT 0,
                reward_sparks INTEGER DEFAULT 0,
                reward_stars INTEGER DEFAULT 0,
                reward_item TEXT,
                period TEXT DEFAULT 'daily',
                status TEXT DEFAULT 'active',
                created_at INTEGER NOT NULL,
                completed_at INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        
        await db.execute("""
            CREATE TABLE IF NOT EXISTS shop_items (
                item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                item_type TEXT NOT NULL,
                item_data TEXT NOT NULL,
                purchased_at INTEGER NOT NULL,
                expires_at INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        
        await db.execute("""
            CREATE TABLE IF NOT EXISTS achievements (
                achievement_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                achievement_type TEXT NOT NULL,
                achievement_name TEXT NOT NULL,
                unlocked_at INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        
        await db.execute("""
            CREATE TABLE IF NOT EXISTS notifications (
                notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                notification_type TEXT NOT NULL,
                message TEXT NOT NULL,
                data TEXT,
                created_at INTEGER NOT NULL,
                read BOOLEAN DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        
        await db.execute("""
            CREATE INDEX IF NOT EXISTS idx_streaks_users ON streaks(user1_id, user2_id)
        """)
        
        await db.execute("""
            CREATE INDEX IF NOT EXISTS idx_streaks_status ON streaks(status)
        """)
        
        await db.execute("""
            CREATE INDEX IF NOT EXISTS idx_users_referrer ON users(referrer_id)
        """)
        
        await db.execute("""
            CREATE INDEX IF NOT EXISTS idx_quests_user ON quests(user_id, status)
        """)
        
        await db.commit()
        
        logger.info("Database initialized successfully")


async def get_db():
    return await aiosqlite.connect(settings.DATABASE_PATH)
