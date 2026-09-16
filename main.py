from bot.client import bot
from config import settings

def main():
    bot.run(settings.discord_token)

if __name__ == "__main__":
    main()