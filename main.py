import sys
import os 
import json
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path +"/modules")

from twitchclient import TwitchClient

def get_config(path):
    with open(path) as f:
        return json.load(f)

config_path = "my_config.json"
config = get_config(config_path)

### Enter desired channel name
channel_name = "jerma985"

twitch_client = TwitchClient(config, channel_name)
twitch_client.start()