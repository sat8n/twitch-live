import os
from dotenv import load_dotenv

import discord
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='test_bot')
async def test(ctx):
    await ctx.send("Test successful.")

### TO DO: User should be able to add streamers to the json file

### TO DO: User should be able to remove streamers from the json file

### TO DO: User should be able to get a list of the current streamers they are monitoring

### TO DO: There should be a method that checks 
# if the streamer name entered is valid 
# possibly using the method getChannel(streamer_id) to validate

bot.run(TOKEN)