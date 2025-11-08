import discord
import aiohttp
import asyncio

import os

TOKEN = os.environ['TOKEN']
GUILD_ID = int(os.environ['GUILD_ID'])
COIN = "internet-computer"   # CoinGecko ID for ICP

client = discord.Client(intents=discord.Intents.default())

async def get_price():
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={COIN}&vs_currencies=usd"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            return data[COIN]["usd"]

@client.event
async def on_ready():
    guild = client.get_guild(GUILD_ID)
    bot_member = guild.get_member(client.user.id)
    
    while True:
        price = await get_price()
        await bot_member.edit(nick=f"ICP: ${price}")
        await asyncio.sleep(60)  # update every minute

client.run(TOKEN)
