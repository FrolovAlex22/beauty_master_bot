import os
from dataclasses import dataclass

# from environs import Env

# from dotenv import load_dotenv

# load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_IDS = os.getenv('ADMIN_IDS')
# DB_USER = os.getenv('DB_USER')
# DB_PASS = os.getenv('DB_PASS')
# DB_HOST = os.getenv('DB_HOST')
# DB_PORT = os.getenv('DB_PORT')
# DB_NAME = os.getenv('DB_NAME')
DATABASE_URL = os.getenv('DATABASE_URL')


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]


@dataclass
class Config:
    tg_bot: TgBot


def load_config() -> Config:
    return Config(
        tg_bot=TgBot(
            token=BOT_TOKEN,
            admin_ids=list(ADMIN_IDS)
        )
    )

# def call_db():
#     DATABASE_URL: str = (
#         f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
#         )
#     return DATABASE_URL