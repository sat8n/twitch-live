import os
from dotenv import load_dotenv

import discord
import asyncio

import methods
import live as twitch

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL = os.getenv('CHANNEL_ID')

class TwitchLive(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.check_streamers_live())

    async def check_streamers_live(self):
        await self.wait_until_ready()
        channel = self.get_channel(CHANNEL)
        twitch_url = "https://www.twitch.tv/"

        while not self.is_closed():
            # every 60 seconds, we want to check for live streamers
            #STREAMER_LIST = methods.openJSON()
            STREAMER_LIST = check_live_streamers_and_update(methods.openJSON())

            for streamer in STREAMER_LIST:
                # isLive == true and isNotified == false
                if (STREAMER_LIST[streamer][0] and not STREAMER_LIST[streamer][1]):
                    STREAMER_LIST[streamer][1] = True
                    methods.writeJSON(STREAMER_LIST)

                    message = "🟢 " + streamer + " is live! " + twitch_url + streamer
                    await channel.send(message)
                elif (STREAMER_LIST[streamer][1] and not STREAMER_LIST[streamer][0]): # isLive == false and isNotified == true
                    STREAMER_LIST[streamer][1] = False
                    methods.writeJSON(STREAMER_LIST)

                    message = "🔴 " + streamer + " has gone offline."
                    await channel.send(message)

            await asyncio.sleep(60) # runs every 60 seconds

### Description: this method uses the Twitch API to check if a streamer is live, and updates the JSON file accordingly
### streamer_list = { 'name': [isLive, isNotified] }
def check_live_streamers_and_update(streamer_list):
    for streamer in streamer_list:
        streamer_id = twitch.getUserID(streamer)['id']
        streamer_info = twitch.getLive(streamer_id)

        # if a streamer is live
        if streamer_info['data']:
            streamer_list[streamer][0] = True # set isLive to true
        elif not streamer_info['data']: # if not live
            streamer_list[streamer][0] = False # set isLive to false
    
    # update the json file
    methods.writeJSON(streamer_list)
    return streamer_list

### TO DO: a method that reads the JSON and returns whether or not to notify the user(?)

client = TwitchLive()

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # add streamer
    if message.content.startswith('?add'):
        streamer = message.content.split()[1]
        STREAMER_LIST = methods.openJSON()
        client_message = "Unable to add " + streamer + "."

        if twitch.getUserID(streamer):
            # we want to use the streamer's display name in the dictionary
            streamer = twitch.getUserID(streamer)['display_name']
            STREAMER_LIST[streamer] = [False, False]
            methods.writeJSON(STREAMER_LIST)
            client_message = "Added " + streamer + " to the list."
        
        await message.channel.send(client_message)

    # remove streamer
    if message.content.startswith('?rm'):
        streamer = message.content.split()[1]
        STREAMER_LIST = methods.openJSON()
        client_message = "Unable to remove " + streamer + "."

        if twitch.getUserID(streamer):
            streamer = twitch.getUserID(streamer)['display_name']

            if streamer in STREAMER_LIST:
                STREAMER_LIST.pop(streamer)
                methods.writeJSON(STREAMER_LIST)
                client_message = "Removed " + streamer + " from the list."

        await message.channel.send(client_message)

    # list the available commands
    if message.content.startswith('?commands'):
        list_of_commands = [
            "Commands:",
            "?add <name>: Description",
            "?rm <name>: Description",
            "?list: Description",
            "?live: Description"
        ]

        client_message = '\n'.join(list_of_commands)
        await message.channel.send(client_message)

client.run(TOKEN)