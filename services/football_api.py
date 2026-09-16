import httpx
from config import settings

BASE_URL = "https://api.football-data.org/v4"

HEADERS = {"X-Auth-Token": settings.football_api_key}

TEAM_IDS = {
    "arsenal": 57,
    "chelsea": 61,
    "liverpool": 64,
    "man city": 65,
    "man united": 66,
}

class FootballAPIError(Exception):
    pass

async def get_matches(team_name: str, limit: int = 5):
    team_id = TEAM_IDS.get(team_name.lower())
    if team_id is None:
        raise FootballAPIError(f"Unknown team: {team_name}")
    url = f"{BASE_URL}/teams/{team_id}/matches"
    params = {"limit": limit}

    async with httpx.AsyncClient() as client:
        response =  await client.get(url, headers = HEADERS, params = params)

    if response.status_code == 429:
        raise FootballAPIError("Rate limit hit -- try again shortly.")
    if response.status_code != 200:
        raise FootballAPIError(f"API Error: {response.status_code} - {response.text}")

    data = response.json()
    return data.get("matches", [])

if __name__ == "__main__":
    import asyncio

    async def main():
        matches = await get_matches("arsenal")
        for m in matches:
            home = m["homeTeam"]["name"]
            away = m["awayTeam"]["name"]
            status = m["status"]
            print(f"{home} vs {away} — {status}")

    asyncio.run(main())
    
    