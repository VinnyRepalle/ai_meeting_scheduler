import requests
import pytz
import re

ZOOM_API_URL = "https://api.zoom.us/v2/users/me/meetings"
ZOOM_JWT_TOKEN = "" 

def is_valid_zoom_passcode(passcode):
   
    return bool(re.fullmatch(r'[\w@\-_*]{1,10}', passcode or ''))

def create_zoom_meeting(title, start_time, passcode=None):
    
    if not is_valid_zoom_passcode(passcode):
        passcode = None  

    headers = {
        "Authorization": f"Bearer {ZOOM_JWT_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "topic": title,
        "type": 2,
        "start_time": start_time.astimezone(pytz.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        "duration": 30,
        "timezone": "Asia/Kolkata",
        "password": passcode,
        "settings": {
            "join_before_host": True,
            "waiting_room": False
        }
    }

    response = requests.post(ZOOM_API_URL, headers=headers, json=payload)

    if response.status_code == 201:
        data = response.json()
        return data.get('join_url'), data.get('password')
    else:
        print("Zoom API Error:", response.status_code, response.text)
        return None, None
