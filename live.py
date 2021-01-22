import os
from dotenv import load_dotenv

from twitchAPI.twitch import Twitch

load_dotenv()
CLIENT_ID = os.getenv('TWITCH_CLIENT_ID')
SECRET = os.getenv('TWITCH_SECRET')

twitch = Twitch(CLIENT_ID, SECRET)
twitch.authenticate_app([])

# Description: If the name entered is valid, then the method will return the streamer's info (e.g. id, display_name)
# get_user_id(STREAMERS[0])['id'] to get id
def get_user_id(streamer):
    try:
        user_info = twitch.get_users(logins=streamer)
        user_data = user_info['data'][0]
        return user_data
    except:
        return False # no streamers going by the name entered

# Description: this will return a data array (filled if a steamer is live, empty if not live)
def get_live(streamer_id):
    stream_info = twitch.get_streams(user_id=streamer_id)
    return stream_info
