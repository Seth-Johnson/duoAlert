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
        lang = config['language']

def send_discord(r_msg):
    data = {
        "content": r_msg
    }
    r = requests.post(webhook_url, data=data)

def update_data():
    global streak_data
    for user in users:
        try:
            with urllib.request.urlopen(api_endpoint + user) as data_r:
                data_p = json.loads(data_r.read().decode())
        except Exception as e:
            logging.exception("Failed to fetch or parse data for user {}. Skipping.".format(user))
            logging.exception("Exception was: {}".format(e))
            continue
        streak = get_streak(data_p)
        streak_data[user] = streak

def update_data_file():
    try:
        streak_file = open("streak_data.json", 'w')
        streak_file.write(json.dumps(streak_data))
        streak_file.close()
    except Exception as e:
        logging.critical("Failed to open or write to data file. Aborting.")
        logging.critical("Exception was {}".format(e))

def check_data():
    #checks new data vs saved
    previous_r = open('streak_data.json')
    previous = json.load(previous_r)
    previous_r.close()
    for user in previous.keys():
        logging.INFO("Loop 1: New: {} Old:{}".format(streak_data[user], previous[user]))
        if streak_data[user] == previous[user]:
            logging.INFO("First If: New: {} Old:{}".format(streak_data[user], previous[user]))
        elif streak_data[user] > previous[user]:
            if streak_data[user] > 1:
                send_discord("@everyone {} has continued their streak of {} days! Congratulations!".format(user, streak_data[user]))
            elif streak_data[user] == 1:
                send_discord("@everyone {} has restarted their streak! Clap with pity.".format(user))
            else:
                send_discord("This message should not have been sent... *stratches head*. If recieved, call the president! Set DEFCON 1!")
                logging.critical("WTH just happened")

def get_streak(data_p):
    streak = data_p["language_data"][lang]["streak"]
    return streak


def main():
    # check if existing saved data
    try:
        get_config()
    except Exception as e:
        logging.critical("Failed to load configuration. Aborting.")
        logging.critical("Full error is: {}".format(e))
    update_data()
    if os.path.exists('streak_data.json'):
        check_data()
    update_data_file()


main()
