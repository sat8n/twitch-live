import json

# Description: Method returns a dictionary of the list of streamers
def open_JSON():
    file = open('streamers.json')
    STREAMER_DICTIONARY = json.load(file)
    return STREAMER_DICTIONARY

# Description: Method writers over the dictionary of streamers with a new one
def write_JSON(dictionary):
    new_json = json.dumps(dictionary, indent=4)
    with open('streamers.json', 'w') as outfile:
        outfile.write(new_json)
