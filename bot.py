import os
from dotenv import load_dotenv
import json

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
@bot.command(name='add_streamer')
async def add_streamer_to_list(ctx, streamer_name):
    file = open('streamers.json') ## duplicate code - turn this into a method (???)
    STREAMER_DICTIONARY = json.load(file)

    # add streamer
    STREAMER_DICTIONARY[streamer_name] = [False, False]
    # somewhere here we want to make sure that the name entered is valid

    new_streamer_json = json.dumps(STREAMER_DICTIONARY, indent=4)
    with open('streamers.json', 'w') as outfile:
        outfile.write(new_streamer_json)

    file = open('streamers.json')
    STREAMER_DICTIONARY = json.load(file)
    streamers = sorted(list(STREAMER_DICTIONARY.keys()))

    message = "Added " + streamer_name + " to the list. "
    message = message + "List of streamers: " + ", ".join(streamers)
    await ctx.send(message)

### TO DO: User should be able to remove streamers from the json file

### TO DO: User should be able to get a list of the current streamers they are monitoring
@bot.command(name='streamer_list')
async def get_streamer_list(ctx):
    file = open('streamers.json')
    STREAMER_DICTIONARY = json.load(file)
    streamers = sorted(list(STREAMER_DICTIONARY.keys()))

    message = "List of streamers: " + ", ".join(streamers)
    await ctx.send(message)

### TO DO: User should be able to get a list of the current live streamers

### TO DO: There should be a method that checks 
# if the streamer name entered is valid 
# possibly using the method getChannel(streamer_id) to validate

bot.run(TOKEN)