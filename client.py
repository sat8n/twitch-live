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

    async def on_ready(self):
        print(f'{self.user.name} has connected to Discord!')

    async def check_streamers_live(self):
        await self.wait_until_ready()

        channel = self.get_channel(CHANNEL)
        while not self.is_closed():
            ### every 60 seconds, read the json file
            # for each key, if isLive == true and isNotified == false then notify the user
            STREAMER_LIST = methods.openJSON()
            for streamer in STREAMER_LIST:
                if (STREAMER_LIST[streamer][0] and not STREAMER_LIST[streamer][1]): # isLive == true and isNotified == false
                    STREAMER_LIST[streamer][1] = True
                    methods.writeJSON(STREAMER_LIST)
                    await channel.send(streamer + " is live")
                elif (STREAMER_LIST[streamer][1] and not STREAMER_LIST[streamer][0]): # isLive == false and isNotified == true
                    STREAMER_LIST[streamer][1] = False
                    methods.writeJSON(STREAMER_LIST)
                    await channel.send(streamer + " has gone offline")

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

### TO DO: a method that reads the JSON and returns whether or not to notify the user(?)

client = TwitchLive()
client.run(TOKEN)