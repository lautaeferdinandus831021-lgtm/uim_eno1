"""
DEV ONLY: Auto-create default user on startup.
REMOVE IN PRODUCTION!
"""
import logging
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal
from app.core.security import hash_password
from app.models.user import User
from app.models.config import ApiConfig, BotConfig
from shared.config import settings

logger = logging.getLogger("bgbot.devseed")

DEV_EMAIL = "dev@bgbot.local"
DEV_PASSWORD = "dev123456"


async def seed_dev_user():
    """Create dev user if not exists."""
    async with AsyncSessionLocal() as db:
        try:
            result = await db.execute(select(User).where(User.email == DEV_EMAIL))
            user = result.scalar_one_or_none()

            if not user:
                user = User(
                    email=DEV_EMAIL,
                    name="Dev User",
                    provider="dev",
                    password_hash=hash_password(DEV_PASSWORD),
                )
                db.add(user)
                await db.flush()

                db.add(ApiConfig(user_id=user.id, demo=True))
                db.add(BotConfig(
                    user_id=user.id,
                    config_json=settings.DEFAULT_BOT_CONFIG,
                ))
                await db.commit()
                logger.info(f"Dev user created: {DEV_EMAIL}")
            else:
                logger.info(f"Dev user exists: {DEV_EMAIL}")

        except Exception as e:
            logger.warning(f"Dev seed skipped: {e}")
            await db.rollback()
