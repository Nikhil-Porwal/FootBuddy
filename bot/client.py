import discord
from discord.ext import commands

from config import settings

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=settings.command_prefix, intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} ({bot.user.id})")

@bot.command(name="ping")
async def ping(ctx: commands.Context):
    await ctx.send("Pong!")