import json
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import argparse
import slack_sdk

# Slack WebClient setup
SLACK_TOKEN = "xoxb-15895572898-4645905684388-exEHKdo8GRa2vCpo3RcSlCHO"
SLACK_TEST_CHANNEL_ID = "D04KM43AMU0"
SLACK_CHANNEL_ID = "C042W0PRHNX"
client = slack_sdk.WebClient(token=SLACK_TOKEN)
# Google Calendar setup
GOOGLE_CALENDAR_API_KEY = "AIzaSyD1F7rfyKEY_lHNC4jVektCvb5AtcEs5Io"
calendar_service = build('calendar', 'v3', developerKey=GOOGLE_CALENDAR_API_KEY)
calendar_id = "c_ee3scrgsfn037jhf3r2epv3kpg@group.calendar.google.com"

parser = argparse.ArgumentParser()
parser.add_argument('-d', dest='debug', action='store_true', default=False, help='Start in Debug Mode')
args = parser.parse_args()

def send_slack_post(event_name, event_date):
    # Send message to Slack using the Web API
        message = f'Reminder: {event_name} is happening on {event_date}.'
        response = '' ''
        if args.debug:
                response = client.chat_postMessage(channel=SLACK_TEST_CHANNEL_ID, text=message)
        else:
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
                    print("sent message")

if __name__ == '__main__':
    get_next_week_events()

