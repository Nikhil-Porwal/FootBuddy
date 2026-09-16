import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class settings:
    discord_token: str
    football_api_key: str
    command_prefix: str = "!"
def load_settings() -> settings:
    token = os.getenv("DISCORD_TOKEN")
    api_key = os.getenv("FOOTBALL")

    if not token:
        raise RuntimeError("DISCORD_TOKEN is missing from .env")
    if not api_key:
        raise RuntimeError("FOOTBALL is missing from .env")

    return settings(discord_token = token, football_api_key = api_key)

settings = load_settings()
