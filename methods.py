import json

# Description: Method returns a dictionary of the list of streamers
def openJSON():
    file = open('streamers.json')
    STREAMER_DICTIONARY = json.load(file)
    return STREAMER_DICTIONARY