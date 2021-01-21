import json

# Description: Method returns a dictionary of the list of streamers
def openJSON():
    file = open('streamers.json')
    STREAMER_DICTIONARY = json.load(file)
    return STREAMER_DICTIONARY

def writeJSON(dictionary):
    new_json = json.dumps(dictionary, indent=4)
    with open('streamers.json', 'w') as outfile:
        outfile.write(new_json)
