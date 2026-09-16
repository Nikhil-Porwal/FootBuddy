import httpx
from datetime import date, timedelta
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

async def get_matches(team_name: str, limit: int = 5) -> list[dict]:
    team_id = TEAM_IDS.get(team_name.lower())
    if team_id is None:
        raise FootballAPIError(f"Unknown team: '{team_name}'")

    today = date.today()
    params = {
        "dateFrom": (today - timedelta(days=14)).isoformat(),
        "dateTo": (today + timedelta(days=14)).isoformat(),
    }

    url = f"{BASE_URL}/teams/{team_id}/matches"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=HEADERS, params=params)

    if response.status_code == 429:
        raise FootballAPIError("Rate limit hit — try again shortly")
    if response.status_code != 200:
        raise FootballAPIError(f"API error {response.status_code}: {response.text}")

    data = response.json()
    matches = data.get("matches", [])
    matches.sort(key=lambda m: m["utcDate"])
    return matches[:limit]

if __name__ == "__main__":
    import asyncio
    import json

    async def main():
        matches = await get_matches("chelsea")
        for m in matches:
            if m["status"] == "FINISHED":
                print(json.dumps(m, indent=2))

    asyncio.run(main())
    
    