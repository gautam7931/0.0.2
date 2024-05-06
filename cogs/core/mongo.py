import config

from discord.ext import commands
from motor.motor_asyncio import AsyncIOMotorClient


class Mongo(commands.Cog):
    """For database operations."""

    def __init__(self, bot):
        self.bot = bot
        self.client = AsyncIOMotorClient(config.DATABASE_URI, tz_aware=True)

    @property
    def db(self):
        return self.client[config.DATABASE_NAME]

    async def get_prefix(self, guild, default="?"):
        if guild is None:
            return default

        entry = await self.db.guild.find_one_and_update(
            {"_id": guild.id},
            {"$setOnInsert": {"_id": guild.id, "prefix": default}},
            upsert=True,
            return_document=True,
        )

        return entry["prefix"]

    async def reserve_id(self, name, reserve=1):
        entry = await self.db.counter.find_one_and_update(
            {"_id": name},
            {"$inc": {"next": reserve}},
            upsert=True,
            return_document=True,
        )

        return entry["next"]


async def setup(bot):
    await bot.add_cog(Mongo(bot))
