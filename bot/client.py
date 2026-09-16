import discord
from discord.ext import commands

from config import settings
from bot.events import register_events

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=settings.command_prefix, intents=intents)

register_events(bot)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} ({bot.user.id})")

@bot.command(name="ping")
async def ping(ctx: commands.Context):
    await ctx.send("Pong!")