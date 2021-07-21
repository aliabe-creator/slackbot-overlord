'''
Created on Jul 19, 2021

@author: Private
'''

import slack
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter
from dotenv import load_dotenv
import os
import json

load_dotenv()

signing = os.environ.get("signing")
slack_token = os.environ.get("slack")
ws_location = os.environ.get("location")

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(signing, '/slack3/events', app) #NEW ENDPOINT!
client = slack.WebClient(token = slack_token)

bot_id = client.api_call("auth.test")['user_id']

client.conversations_open(users='U01EJSDGX50')
client.chat_postMessage(channel='D028FNW5JH4', text='Bot is now online!')

channel_id = ''

#sends a welcome message to anyone who joins
@slack_event_adapter.on('team_join')
def welcome(event_data):
    user_id = event_data['event']['user']['id'] #get user id of person that just joined
    
    client.conversations_open(users = user_id) #opens convo
    d = client.conversations_list(exclude_archived = True, types = 'im') #needs next page too
    
    #find the convo id that was just opened
    arr = d.get('channels')
    for channel in arr:
        u = channel.get('user')
        if (u == user_id):
            i = channel.get('id')
            client.chat_postMessage(channel = i, blocks = [{
                                                                "type": "divider"
                                                            },
                                                            {
                                                                "type": "section",
                                                                "text": {
                                                                    "type": "mrkdwn",
                                                                    "text": ":wave: *Welcome* to the _" + ws_location + "_, or at least our Slack workspace :joy:. \n\n Feel free to introduce yourself in #general, hope you have a great time here! :tada:"
                                                                }
                                                            },
                                                            {
                                                                "type": "divider"
                                                            }])

@slack_event_adapter.on('app_mention')
def wave(payload):
    client.reactions_add(channel = payload['event']['channel'], name = 'wave', timestamp = payload['event']['ts']) #add wave reaction to message
    
#help menu
@app.route('/slack3/help', methods = ['POST'])
def list_commands():
    global channel_id
    
    data = request.form
    channel_id = data.get('channel_id')
    
    client.chat_postMessage(channel = channel_id, blocks = [{
            "type": "divider"
        },
        {
            "type": "input",
            "element": {
                "type": "static_select",
                "placeholder": {
                    "type": "plain_text",
                    "text": "Select a page",
                    "emoji": True
                },
                "options": [
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "About R2",
                            "emoji": True
                        },
                        "value": "about"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "Commands - Socials",
                            "emoji": True
                        },
                        "value": "socials"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "Commands - Events",
                            "emoji": True
                        },
                        "value": "events"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "Commands - Utilities",
                            "emoji": True
                        },
                        "value": "utils"
                    }
                ],
                "action_id": "static_select-action"
            },
            "label": {
                "type": "plain_text",
                "text": "Welcome to the help menu! Use the menu below to select which page you want to view.",
                "emoji": True
            }
        }])
    
    return Response(), 200

@app.route('/slack3/block', methods = ['POST'])
def blocks():
    data = request.form
    raw = data.get('payload') #get only payload json
    payload = json.loads(raw)
    
    option = payload['actions'][0]['selected_option']['value']
    
    if (option == 'about'):
        client.chat_postMessage(channel = channel_id, blocks = [{
            "type": "divider"
        },
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "About",
                "emoji": True
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": ":wave: Hey, I'm R2D2! Nice to meet you. I'm what you call a 'bot.' I have a couple of subprocesses that you might see around these parts..."
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "<@U028JHBH0D9> _is the informant. As of right now, he can tell jokes and fetch news from a variety of different sources._"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "<@U0288EPFK9U> _is the one that keeps everyone on track. He works with the Google Calendar API to schedule and post events._"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "<@U027UKYKMKJ> _is the chatty one. He won't hesitate to tell everyone when there's a new SLP video hot off the editing block._"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Check out the other pages for more details!*"
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": "*Technical info*: developed and maintained by <@U01EJSDGX50>, written in Python, hosted on Oracle Cloud. See the code here: https://github.com/aliabe-creator."
                }
            ]
        }])
        
    if (option == 'socials'):
        client.chat_postMessage(channel = channel_id, blocks = [{
            "type": "divider"
        },
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "R2D2 - Socials' Command List",
                "emoji": True
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "_None yet :cry:, feel free to suggest commands!_"
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": "*Technical info*: developed and maintained by <@U01EJSDGX50>, written in Python, hosted on Oracle Cloud. See the code here: https://github.com/aliabe-creator."
                }
            ]
        }])
        
    if (option == 'events'):
        client.chat_postMessage(channel = channel_id, blocks = [{
            "type": "divider"
        },
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "R2D2 - Events' Command List",
                "emoji": True
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "`/postevent link_to_event` | _Prettyformats existing event's attributes. *Posts without confirmation*. Command use restricted to admins._"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "`/addevent event_name` | _Launches the Event Creation wizard. Simple events only (time, date, location). Command use restricted to admins._"
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": "*Technical info*: developed and maintained by <@U01EJSDGX50>, written in Python, hosted on Oracle Cloud. See the code here: https://github.com/aliabe-creator."
                }
            ]
        }])
        
    if (option == 'utils'):
        client.chat_postMessage(channel = channel_id, blocks = [{
            "type": "divider"
        },
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "R2D2 - Utilities' Command List",
                "emoji": True
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "`/joke` | _Tells a joke!_"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "`/news news_source` | _Fetches recent/top news. Choose from UCLA Newsroom (`UCLA`), Daily Bruin (`DailyBruin`), LA Times (`LATimes`), New York Times (`NYT`), or British Broadcasting Corp. (`BBC`). Feel free to suggest more sources!_"
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": "*Technical info*: developed and maintained by <@U01EJSDGX50>, written in Python, hosted on Oracle Cloud. See the code here: https://github.com/aliabe-creator."
                }
            ]
        }])
        
    return Response(), 200

if __name__ == "__main__":
    app.run(debug=True, port=5002)