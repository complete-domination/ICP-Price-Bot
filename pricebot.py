import discord
import aiohttp
import asyncio
import os

# Env vars
TOKEN = os.environ.get('TOKEN')
GUILD_ID = os.environ.get('GUILD_ID')  # optional; if unset, updates all guilds
COIN = "internet-computer"  # ✅ ICP CoinGecko ID

if not TOKEN:
    raise SystemExit("Missing env var TOKEN")
if GUILD_ID:
    try:
        GUILD_ID = int(GUILD_ID)
    except ValueError:
        raise SystemExit("GUILD_ID must be an integer")

# Intents
intents = discord.Intents.default()
intents.guilds = True
intents.members = True  # also enable "Server Members Intent" in the Dev Portal
client = discord.Client(intents=intents)

update_task = None

# ---- Price fetcher ----
async def get_price_data():
    url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids={COIN}"
    timeout = aiohttp.ClientTimeout(total=10)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                raise RuntimeError(f"CoinGecko HTTP {resp.status}")
            data = await resp.json()
            price = data[0]['current_price']
            change_24h = data[0]['price_change_percentage_24h']
            return price, change_24h

# ---- Per-guild update ----
async de
