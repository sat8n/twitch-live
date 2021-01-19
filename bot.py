import os
from dotenv import load_dotenv
import json

import discord
from discord.ext import commands

import live as twitch
import methods

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='test_bot')
async def test(ctx):
    await ctx.send("Test successful.")

### Description: User should be able to add streamers to the json file
@bot.command(name='add_streamer')
async def add_streamer_to_list(ctx, streamer_name):
    STREAMER_DICTIONARY = methods.openJSON()
    message = ""

    # add streamer
    if twitch.getUserID(streamer_name):
        STREAMER_DICTIONARY[streamer_name] = [False, False]

        new_streamer_json = json.dumps(STREAMER_DICTIONARY, indent=4)
        with open('streamers.json', 'w') as outfile:
            outfile.write(new_streamer_json)

        message = "Added " + streamer_name + " to the list. "
    else:
        message = "Unable to add " + streamer_name + " as there are no streamers going by that name. "

    STREAMER_DICTIONARY = methods.openJSON()
    streamers = sorted(list(STREAMER_DICTIONARY.keys()))
    
    message = message + "List of streamers: " + ", ".join(streamers)
    await ctx.send(message)

### Description: User should be able to remove streamers from the json file
@bot.command(name='remove_streamer')
async def remove_streamer_from_list(ctx, streamer_name):
    STREAMER_DICTIONARY = methods.openJSON()

    # remove streamer
    ## you need to check if the name is actually in the dictionary
    STREAMER_DICTIONARY.pop(streamer_name)

    new_streamer_json = json.dumps(STREAMER_DICTIONARY, indent=4)
    with open('streamers.json', 'w') as outfile:
        outfile.write(new_streamer_json)

    STREAMER_DICTIONARY = methods.openJSON()
    streamers = sorted(list(STREAMER_DICTIONARY.keys()))

    message = "Removed " + streamer_name + " from the list. "
    message = message + "List of streamers: " + ", ".join(streamers)
    await ctx.send(message)

### Description: User should be able to get a list of the current streamers they are monitoring
@bot.command(name='streamer_list')
async def get_streamer_list(ctx):
    STREAMER_DICTIONARY = methods.openJSON()
    streamers = sorted(list(STREAMER_DICTIONARY.keys()))

    message = "List of streamers: " + ", ".join(streamers)
    await ctx.send(message)

### TO DO: User should be able to get a list of the current live streamers

### TO DO: There should be a method that checks 
# if the streamer name entered is valid 
# possibly using the method getChannel(streamer_id) to validate

bot.run(TOKEN)