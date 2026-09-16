import discord
from discord.ext import commands

from services.football_api import get_matches, FootballAPIError


def build_match_embed(team_name: str, matches: list[dict]) -> discord.Embed:
    embed = discord.Embed(
        title = f"Matches for {team_name.title()}",
        color = discord.Color.blue(),
    )

    for match in matches[:5]:
        home = match["homeTeam"]["name"]
        away = match["awayTeam"]["name"]
        status = match["status"]
        utc_date = match["utcDate"]

        score = match.get("score", {}).get("fullTime", {})
        home_score = score.get("home")
        away_score = score.get("away")

        if home_score is not None and away_score is not None:
            score_str = f"{home_score} - {away_score}"
        else:
            score_str = "vs"

        embed.add_field(
            name = f"{home} {score_str} {away}",
            value = f"Status: `{status}` • {utc_date[:10]}",
            inline = False
        )
    return embed

def register_events(bot: commands.Bot):
    @bot.command(name = "match")
    async def match(ctx: commands.Context, *, team: str):
        try:
            matches = await get_matches(team)
        except FootballAPIError:
            await ctx.send(f" Team not found: `{team}`")
            return
        if not matches:
            await ctx.send(f"No matches found for **{team.title()}**.")
            return
        embed = build_match_embed(team, matches)
        await ctx.send(embed=embed)
