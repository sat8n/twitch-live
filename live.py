import urllib.request
import os
from dotenv import load_dotenv
import json

from twitchAPI.twitch import Twitch

load_dotenv()
CLIENT_ID = os.getenv('TWITCH_CLIENT_ID')
SECRET = os.getenv('TWITCH_SECRET')

twitch = Twitch(CLIENT_ID, SECRET)
twitch.authenticate_app([])

### TO DO: user should be able to modify file this later through commands directed to the discord bot
# reads from the json file
file = open('streamers.json')
STREAMER_DICTIONARY = json.load(file) # streamer: [isLive, notificationSent]

# getUserID(STREAMERS[0])['id'] to get id
def getUserID(streamer):
    try:
        user_info = twitch.get_users(logins=streamer)
        user_data = user_info['data'][0]
        return user_data
    except:
        return False # no streamers going by the name entered

### this is being used by checkStreamers method
# this will return a data array if a steamer is live
def getLive(streamer_id):
    stream_info = twitch.get_streams(user_id=streamer_id)
    return stream_info

# checkStreamers(list(STREAMER_DICTIONARY.keys()))
def checkStreamers(streamers):
    for streamer in streamers:
        streamer_id = getUserID(streamer)['id']
        streamer_info = getLive(streamer_id)
        if streamer_info['data']: # if a streamer is live
            STREAMER_DICTIONARY[streamer][0] = True
            if STREAMER_DICTIONARY[streamer][1] == False: # if notified is false
                print(streamer + " is live") ### change this part to discord bot
                STREAMER_DICTIONARY[streamer][1] = True
        elif not streamer_info['data']: # if a streamer is not live
            if STREAMER_DICTIONARY[streamer][0] == True: # if they were live before
                print(streamer + " has gone offline")
                STREAMER_DICTIONARY[streamer][0] = False # change to false
                STREAMER_DICTIONARY[streamer][1] = False
            else:
                STREAMER_DICTIONARY[streamer][0] = False # keep it at false
                STREAMER_DICTIONARY[streamer][1] = False

### this is where we loop forever
# import schedule
# import time

# def job():
#     print("Checking for live streamers...")
#     STREAMERS = list(STREAMER_DICTIONARY.keys())
#     checkStreamers(STREAMERS)

# schedule.every(1).minutes.do(job)

# while True:
#     schedule.run_pending()
#     time.sleep(1)
