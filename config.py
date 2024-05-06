import os


BOT_PREFIX = os.environ["BOT_PREFIX"]

DATABASE_URI = os.environ["DATABASE_URI"]
DATABASE_NAME = os.environ["DATABASE_NAME"]

REDIS_URI = os.environ["REDIS_URI"]
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
