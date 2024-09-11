import os
from dataclasses import dataclass


BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_IDS = os.getenv('ADMIN_IDS')
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
