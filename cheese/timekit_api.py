import arrow
import requests

from requests.auth import HTTPBasicAuth
from . import models

base_url = "https://api.timekit.io/v2/"
app_slug = "askpire-877"
utc_format = "YYYY-MM-DDTHH:mm:ssZZ"
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

def get_events(user):
    headers = {'Timekit-App': app_slug}
    start = arrow.utcnow()
    end = start.shift(months=1)
    start = start.format(utc_format)
    end = end.format(utc_format)
    start = start.replace("+", "%2B");
    end = end.replace("+", "%2B");
    r = requests.get(base_url + "events?start={}&end={}".format(start, end),
                     headers=headers,
                     auth=HTTPBasicAuth(user.email, user.timekit_token))
    if r.status_code != 200:
        print(r.text)
        return None, False
    data = r.json()['data']
    events = []
    for e in data:
        event = {}
        if models.Consultant.query.filter_by(user_id=user.id).first() is None:
            event['title'] = "Meeting with {}".format(e['what'].split(" x ")[0])
        else:
            event['title'] = "Meeting with {}".format(e['what'].split(" x ")[1])
        start = arrow.get(e['start'], utc_format)
        end = arrow.get(e['end'], utc_format)
        event['id'] = e['id']
        event['date'] = start.format("MM/DD/YYYY")
        event['start_time'] = start.format("HH:mm")
        event['end_time'] = end.format("HH:mm")
        event['status'] = arrow.get(e['start'], utc_format).humanize(arrow.utcnow())
        event['skype'] = e['description'].split("Skype username: ")[1].rstrip()
        events.append(event)
    return events, True
