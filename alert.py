
#!/usr/bin/env python3

import urllib.request
import requests
import os
import json
import logging

api_endpoint = 'http://www.duolingo.com/users/'

webhook_url = None
users = []
streak_data = {}
lang = None

logging.basicConfig(filename="duoAlert.log", level=logging.INFO)

def get_config():
    global users
    global webhook_url
    global lang
    with open('config.json') as config_r:
        config = json.load(config_r)
        webhook_url = config['webhook_url']
        users = config['users']
        print(type(users))
        print("users are {}".format(users))
        print("raw users are ---vegan--- {}".format(config['users']))
        lang = config['language']
        # add any more config we need

def send_discord(r_msg):
    data = {
        "content": r_msg
    }
    r = requests.post(webhook_url, data=data)

def update_data():
    global streak_data
    print("Nothing is happening")
    print(users)
    for user in users:
        print(user)
        with urllib.request.urlopen(api_endpoint + user) as data_r:
            print(data_r.getcode())
            data_p = json.loads(data_r.read().decode())
            streak = get_streak(data_p)
            print(streak)
            streak_data[user] = streak
            print(streak_data[user]) #DEBUG
        #DEBUG print(data_p)
        #DEBUG print(type(data_p))

def update_data_file():
    try:
        streak_file = open("streak_data.json", 'w')
        streak_file.write(json.dumps(streak_data))
        print("Bob: {}".format(json.dumps(streak_data)))
    except Exception as e:
        logging.critical("the world has ended. data file cannot be accessed")
        loggin.critical("Exception was {}".format(e))

def check_data():
    #checks new data vs saved
    previous_r = open('streak_data.json')
    previous = json.load(previous_r)
    for user in previous.keys():
        print("Loop 1: New: {} Old:{}".format(streak_data[user], previous[user]))
        if streak_data[user] == previous[user]:
            print("First If: New: {} Old:{}".format(streak_data[user], previous[user]))
        elif streak_data[user] > previous[user]:
            print("Sending a message")
            # send message
            if streak_data[user] > 1:
                send_discord("@everyone {} has continued their streak of {} days! Congratulations!".format(user, streak_data[user]))
            elif streak_data[user] == 1:
                send_discord("@everyone {} has restarted their streak! Clap with pity.".format(user))
            else:
                send_discord("This message should not have been sent... *stratches head*. If recieved, call the president! Set DEFCON 1!")
                logging.critical("WTH just happened")
    update_data_file()

def get_streak(data_p):
    #DEBUG print(type(data_p))
    streak = data_p["language_data"][lang]["streak"]
    #DEBUG print(streak)
    return streak


def main():
    # check if existing saved data
    print("In main") #DEBUG
    get_config()
    update_data()
    if os.path.exists('streak_data.json'):
        #DEBUG print("it worked?")
        # call check_data()
        check_data()
    else:
        print("In except") #DEBUG
        # create data file
        update_data_file()
    #DEBUG print(streak_data.keys())


main()
