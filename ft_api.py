from authlib.client import OAuth2Session
import time
import json
import os

def client():
    # SET IN YOUR SHELL'S ENV VARIABLES FT_CLIENT AND FT_SECRET -- (CLIENT ID AND SECRET ID FOR 42 API ACCESS) OR ENTER THEM MANUALLY BELOW INPLACE OF STRINGS
    CLIENT_ENV = 'FT_CLIENT'
    SECRET_ENV = 'FT_SECRET'
    CLIENT_ID = os.environ.get(CLIENT_ENV)
    SECRET_ID = os.environ.get(SECRET_ENV)  
    
    url = "https://api.intra.42.fr"
    session = OAuth2Session(
        client_id=CLIENT_ID,
        client_secret=SECRET_ID
        )
    token = session.fetch_token(
        url+"/oauth/token",
        grant_type='client_credentials',
        scope="public tig"
    ) 
    return session, token

def get_userids_by_logins(session, room):
    page_size = 100
    base_url = "https://api.intra.42.fr/v2/users/?page[size]=" + str(page_size) + "&filter[login]="
    print(f"GET user id: {room.occupants}\n")
    userids = []

    logins = room.occupants
    for user_login in logins:
        base_url += user_login + ","

    response = session.get(base_url)
    time.sleep(0.6)
    if response.status_code == 200:
        user_dict = json.loads(response.content.decode('utf-8'))
        for user in user_dict:
            userids.append(str(user["id"]))
    else:
        print(response)
    room.occupants = userids