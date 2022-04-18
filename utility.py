import json
import random
import string
import webbrowser
import requests 
from requests.structures import CaseInsensitiveDict

def get_config(path):
    with open(path) as f:
        return json.load(f)

def generate_state(N):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(N))

def get_authcode(client_id, redirect_uri): #+chat%3Aedit
    state = generate_state(15)
    print(f"Input State: {state} \n")
    url = f"https://id.twitch.tv/oauth2/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope=chat%3Aread&state={state}"
    webbrowser.open(url)
    print("Enter URL From Browser: ")
    auth_url = input()
    res_state = auth_url[auth_url.find("&state=") + len("&state=") : ]
    if state != res_state:
        print("STATES DO NOT MATCH")
        exit()
    prefixSpot = auth_url.find("?code=")
    postfixSpot = auth_url.find("&scope=")
    auth_code = auth_url[prefixSpot + len("?code=") : postfixSpot]
    return auth_code

def refresh_authtoken(client_id, client_secret, auth_rtoken):
    url = "https://id.twitch.tv/oauth2/token"

    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/x-www-form-urlencoded"
    data = f"grant_type=refresh_token&refresh_token={auth_rtoken}&client_id={client_id}&client_secret={client_secret}"
    res = requests.post(url, headers=headers, data=data)
    return res.json()

def get_authtoken(client_id, client_secret, auth_code):
    url = "https://id.twitch.tv/oauth2/token"
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/x-www-form-urlencoded"
    data = f"client_id={client_id}&client_secret={client_secret}&code={auth_code}&grant_type=authorization_code&redirect_uri=http://localhost:3000"
    res = requests.post(url, headers=headers, data=data)
    return res.json()

def get_lsdata(channel, client_id, auth_code):
    # https://api.twitch.tv/helix/streams?user_login=afro&user_login=cohhcarnage&user_login=lana_lux'
    url = f"https://api.twitch.tv/helix/streams?user_login={channel}"
    headers = CaseInsensitiveDict()
    headers["Authorization"] = f"Bearer {auth_code}"
    headers["Client-Id"] = f"{client_id}"
    res = requests.get(url, headers=headers)
    lsdata = res.json()
    return lsdata["data"][0]
