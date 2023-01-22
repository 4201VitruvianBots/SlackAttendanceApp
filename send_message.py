import json
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import argparse
import slack_sdk
import keys

# Slack WebClient setup
SLACK_TOKEN = keys.SLACK_TOKEN
SLACK_TEST_CHANNEL_ID = keys.SLACK_TEST_CHANNEL_ID
SLACK_CHANNEL_ID = keys.SLACK_CHANNEL_ID
client = slack_sdk.WebClient(token=SLACK_TOKEN)
# Google Calendar setup
GOOGLE_CALENDAR_API_KEY = keys.GOOGLE_CALENDAR_API_KEY
calendar_service = build('calendar', 'v3', developerKey=GOOGLE_CALENDAR_API_KEY)
calendar_id = keys.calendar_id

link = "https://calendar.google.com/calendar/u/0/embed?src=c_ee3scrgsfn037jhf3r2epv3kpg@group.calendar.google.com&ctz=America/Los_Angeles"

parser = argparse.ArgumentParser()
parser.add_argument('-d', dest='debug', action='store_true', default=False, help='Start in Debug Mode')
args = parser.parse_args()


def send_slack_post(event_name, start_time, end_time):
    # Send message to Slack using the Web API
    message = f'{event_name} starting five days from now {start_time}-{end_time}. <{link}|Team Calendar>'
    response = ""
    if args.debug:
        response = client.chat_postMessage(channel=SLACK_TEST_CHANNEL_ID, text=message)
    else:
        response = client.chat_postMessage(channel=SLACK_CHANNEL_ID, text=message)
    return response

def get_next_week_events():
    now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    next_week = (datetime.now() + timedelta(days=5)).isoformat() + 'Z'
    events_result = calendar_service.events().list(calendarId=calendar_id, timeMin=now,
                                                   timeMax=next_week, singleEvents=True,
                                                   orderBy='startTime').execute()
    events = events_result.get('items', [])
    if not events:
        print('No upcoming events found.')
    else:
        for event in events:
            start = event['start'].get('dateTime')
            start_time = datetime.fromisoformat(start).strftime("%-m/%d/%y %-I:%M %p")
            end = event['end'].get('dateTime')
            end_time = datetime.fromisoformat(end).strftime("%-I:%M %p")
            event_name = event['summary']
            send_slack_post(event_name, start_time, end_time)
            print("sent message")

if __name__ == '__main__':
    get_next_week_events()

