import os
from datetime import datetime as dt
import discord
from discord.ext import commands

TOKEN = os.getenv('TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

TIME_SK = 0
TIME_SH = 0
TIME_ORG = 0

client = discord.Client()

@client.event
async def on_ready():
    guild = client.guilds
    # for guild in client.guilds:
    #     if guild.name == GUILD:
    #         break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    
    
client.run(TOKEN)