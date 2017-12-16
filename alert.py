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
    with open('config.json') as config_r:
        config = json.load(config_r)
        webhook_url = config['webhook_url']
        users = config['users']
        lang = config['language']
        # add any more config we need

def send_discord(r_msg):
    data = {
        "content": r_msg
    }
    r = requests.post(webhook_url, data=data)

def update_data():
    for user in users:
        with urllib.request.urlopen(api_endpoint + user) as data_r:
            data_p = json.loads(data_r.read().decode())
            streak = get_streak(data_p)
            streak_data[user] = streak
            print(streak_data[user]) #DEBUG
        #DEBUG print(data_p)
        #DEBUG print(type(data_p))

def update_data_file():
    try:
        streak_file = open("streak_data.json", 'w')
        streak_file.write(json.dumps(streak_data))
    except Exception as e:
        logging.critical("the world has ended. data file cannot be accessed")
        loggin.critical("Exception was {}".format(e))

def check_data():
    #checks new data vs saved
    previous_r = open('streak_data.json')
    previous = json.load(previous_r)
    for user in previous.keys():
        if streak_data[user] == previous[user]:
            pass
        elif streak_data[user] == 0:
            print("Resetting streak")
            streak_data[user] = 0
            # update the file
            update_data_file()
        elif streak_data[user] > previous[user] and streak_data[user] is not 1:
            print("Sending a message")
            # send message
            if streak_data[user] > 1:
                send_discord("{} has continued their streak of {} days! Congratulations!".format(user, streak_data[user]))
            elif streak_data[user] == 1:
                send_discord("{} has restarted their streak! Clap with pity.".format(user))
            else:
                send_discord("This message should not have been sent... *stratches head*. If recieved, call the president! Set DEFCON 1!")
                logging.critical("WTH just happened")

def get_streak(data_p):
    #DEBUG print(type(data_p))
    streak = data_p["language_data"][lang]["streak"]
    #DEBUG print(streak)
    return streak


def main():
    # check if existing saved data
    print("In main") #DEBUG
    get_config()
    if os.path.exists('streak_data.json'):
        #DEBUG print("it worked?")
        # call check_data()
        update_data()
        check_data()
    else:
        print("In except") #DEBUG
        # create data file
        update_data()
        update_data_file()
    #DEBUG print(streak_data.keys())


main()
