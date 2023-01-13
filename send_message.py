import json
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
<<<<<<< HEAD
import slack_sdk
=======
import slack
>>>>>>> d06169f... First Test

# Slack WebClient setup
SLACK_TOKEN = "xapp-1-A04J98U25HB-4626718325364-4028b5f85c23ed41a59ae36e07c078909e7b74778f86caff488662076713b14f"
SLACK_CHANNEL_ID = "C042W0PRHNX"
<<<<<<< HEAD
client = slack_sdk.WebClient(token=SLACK_TOKEN)
=======
client = slack.WebClient(token=SLACK_TOKEN)
>>>>>>> d06169f... First Test

# Google Calendar setup
GOOGLE_CALENDAR_API_KEY = "AIzaSyD1F7rfyKEY_lHNC4jVektCvb5AtcEs5Io"
calendar_service = build('calendar', 'v3', developerKey=GOOGLE_CALENDAR_API_KEY)
calendar_id = "c_ee3scrgsfn037jhf3r2epv3kpg@group.calendar.google.com"

def send_slack_post(event_name, event_date):
    # Send message to Slack using the Web API
    message = f'Reminder: {event_name} is happening on {event_date}.'
    response = client.chat_postMessage(channel=SLACK_CHANNEL_ID, text=message)
    return response

def get_next_week_events():
    now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    next_week = (datetime.now() + timedelta(days=7)).isoformat() + 'Z'
    events_result = calendar_service.events().list(calendarId=calendar_id, timeMin=now,
                                            timeMax=next_week, singleEvents=True,
                                            orderBy='startTime').execute()
    events = events_result.get('items', [])
    if not events:
        print('No upcoming events found.')
    else:
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            start_time = datetime.fromisoformat(start).strftime("%Y-%m-%d %H:%M:%S")
            event_name = event['summary']
            send_slack_post(event_name, start_time)

if __name__ == '__main__':
    get_next_week_events()
