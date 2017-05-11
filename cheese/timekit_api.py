from . import models
import requests
from requests.auth import HTTPBasicAuth

base_url = "https://api.timekit.io/v2/"
app_slug = "askpire-877"

def authenticate(user):
    data = {
        'email': user.email,
        'password': user.password
    }
    r = requests.post(base_url + "auth", json=data)
    if r.status_code != 200:
        return False
    data = r.json()['data']
    if user.timekit_token is None:
        user.timekit_token = data['api_token']
    if data['image'] is None:
        user.image = "/static/img/camera.png"
    else:
        user.image = data['image']
    models.db.session.commit()
    return True

def create_user(user):
    headers = {'Timekit-App': app_slug}
    data = {
        'email': user.email,
        'timezone': "America/New_York",
        'first_name': user.first_name,
        'last_name': user.last_name,
        'password': user.password
    }
    r = requests.post(base_url + "users", headers=headers, json=data)
    if r.status_code != 201:
        return "", False
    timekit_token = r.json()['data']['api_token']
    return timekit_token, True

def create_calendar(user):
    headers = {'Timekit-App': app_slug}
    data = {
        'name': "{} {}'s Calendar".format(user.first_name, user.last_name),
        'description': "Schedule an appointment with {} {}.".format(user.first_name, user.last_name),
        'foregroundcolor': "#FFFFFF",
        'backgroundcolor': "#21CFF2"
    }
    r = requests.post(base_url + "calendars",
                      headers=headers,
                      auth=HTTPBasicAuth(user.email, user.timekit_token),
                      json=data)
    if r.status_code != 201:
        return None, False
    data = r.json()['data']
    calendar = models.Calendar(app_slug=app_slug, timekit_id=data['id'], user=user)
    models.db.session.add(calendar)
    models.db.session.commit()
    return calendar, True

def delete_calendar(user):
    calendar = user.calendar
    if calendar is None:
        return False
    headers = {'Timekit-App': app_slug}
    r = requests.delete(base_url + "calendars/" + calendar.timekit_id,
                        headers=headers,
                        auth=HTTPBasicAuth(user.email, user.timekit_token),
                        json=data)
    if r.status_code != 204:
        return False
    models.db.session.delete(user.calendar)
    return True

def get_api_token(user):
    data = {
        'email': user.email,
        'password': user.password
    }
    r = requests.post(base_url + "auth", json=data)
    if r.status_code != 200:
        return None
    api_token = r.json()['data']['api_token']
    return api_token

def get_events(user, start, end):
    headers = {'Timekit-App': app_slug}
    r = requests.get(base_url + "events?start={}&end={}".format(start, end),
                      headers=headers,
                      auth=HTTPBasicAuth(user.email, user.timekit_token))
    if r.status_code != 200:
        print(r.text)
        return None, False
    events = r.json()['data']
    return events, True
