import aiosqlite
from pathlib import Path
from config import settings
import structlog

logger = structlog.get_logger()


async def init_database():
    db_path = Path(settings.DATABASE_PATH)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    async with aiosqlite.connect(db_path) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                avatar TEXT NOT NULL,
                language TEXT DEFAULT 'ru',
                sparks INTEGER DEFAULT 0,
                stars INTEGER DEFAULT 0,
                energy INTEGER DEFAULT 100,
                level INTEGER DEFAULT 1,
                exp INTEGER DEFAULT 0,
                best_streak INTEGER DEFAULT 0,
                total_referrals INTEGER DEFAULT 0,
                referrer_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_action TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_energy_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_premium INTEGER DEFAULT 0,
                is_banned INTEGER DEFAULT 0
            )
        """)
        
        await db.execute("""
            CREATE TABLE IF NOT EXISTS streaks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user1_id INTEGER NOT NULL,
                user2_id INTEGER NOT NULL,
                days INTEGER DEFAULT 0,
                last_extend_user1 TIMESTAMP,
                last_extend_user2 TIMESTAMP,
                expiry TIMESTAMP NOT NULL,
                is_active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                max_days INTEGER DEFAULT 0,
                lives INTEGER DEFAULT 3,
                protected_until TIMESTAMP,
                FOREIGN KEY (user1_id) REFERENCES users(user_id),
                FOREIGN KEY (user2_id) REFERENCES users(user_id),
                UNIQUE(user1_id, user2_id)
            )
        """)
        
        await db.execute("""
            CREATE TABLE IF NOT EXISTS streak_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                from_user_id INTEGER NOT NULL,
                to_user_id INTEGER NOT NULL,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (from_user_id) REFERENCES users(user_id),
                FOREIGN KEY (to_user_id) REFERENCES users(user_id)
            )
        """)
        
        await db.execute("""
            CREATE TABLE IF NOT EXISTS pets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                emoji TEXT NOT NULL,
                rarity TEXT NOT NULL,
                state TEXT DEFAULT 'egg',
                mood TEXT DEFAULT 'happy',
                level INTEGER DEFAULT 1,
                exp INTEGER DEFAULT 0,
                lives INTEGER DEFAULT 3,
                streak_id INTEGER,
                hatched_at TIMESTAMP,
                last_fed TIMESTAMP,
                last_played TIMESTAMP,
                customization TEXT,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (streak_id) REFERENCES streaks(id)
            )
        """)
        
        await db.execute("""
            CREATE TABLE IF NOT EXISTS achievements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                type TEXT NOT NULL,
                name TEXT NOT NULL,
                description TEXT,
                emoji TEXT,
                unlocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        
        await db.execute("""
            CREATE TABLE IF NOT EXISTS quests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                type TEXT NOT NULL,
                name TEXT NOT NULL,
                description TEXT,
                target INTEGER NOT NULL,
                progress INTEGER DEFAULT 0,
                reward_sparks INTEGER DEFAULT 0,
                reward_stars INTEGER DEFAULT 0,
                is_completed INTEGER DEFAULT 0,
                expires_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        
        await db.execute("""
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                item_type TEXT NOT NULL,
                item_id TEXT NOT NULL,
                quantity INTEGER DEFAULT 1,
                acquired_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        
        await db.execute("""
            CREATE TABLE IF NOT EXISTS gifts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                from_user_id INTEGER NOT NULL,
                to_user_id INTEGER NOT NULL,
                gift_type TEXT NOT NULL,
                message TEXT,
                is_opened INTEGER DEFAULT 0,
                sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (from_user_id) REFERENCES users(user_id),
                FOREIGN KEY (to_user_id) REFERENCES users(user_id)
            )
        """)
        
        await db.execute("""
            CREATE TABLE IF NOT EXISTS referral_rewards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                level INTEGER NOT NULL,
                referral_count INTEGER NOT NULL,
                reward_type TEXT NOT NULL,
                reward_value INTEGER NOT NULL,
                claimed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        
        await db.execute("""
            CREATE INDEX IF NOT EXISTS idx_streaks_users ON streaks(user1_id, user2_id)
        """)
        
        await db.execute("""
            CREATE INDEX IF NOT EXISTS idx_streaks_expiry ON streaks(expiry)
        """)
        
        await db.execute("""
            CREATE INDEX IF NOT EXISTS idx_pets_user ON pets(user_id)
        """)
        
        await db.execute("""
            CREATE INDEX IF NOT EXISTS idx_quests_user ON quests(user_id, is_completed)
        """)
        
        await db.commit()
        
    logger.info("database_initialized", path=str(db_path))
