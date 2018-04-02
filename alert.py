#!/usr/bin/env python3

import urllib.request
import requests
import os
import json
import logging
import time
import datetime
import random

api_endpoint = 'http://www.duolingo.com/users/'

webhook_url = None
users = []
streak_data = {}
version = "0.4"
phrase_r = {}

timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d')
complete_timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
logging.basicConfig(filename="duoAlert.log", level=logging.INFO)

def get_phrase():
    with open('phrases.json') as phrase_r:
        phrase = json.load(phrase_r)
        phrases = phrase['phrases']
        return random.choice(phrases)

def get_config():
    global users
    global webhook_url
    with open('config.json') as config_r:
        config = json.load(config_r)
        webhook_url = config['webhook_url']
        users = config['users']
        logging.info("Config set.")

def send_discord(r_msg, url = None):
    if url is None:
        url = ""
    data = {
        "embeds":[{
          "title":"Duolingo Streak Bot",
          "description":"{}".format(r_msg),
          "color":0xff8000,
          "type":"rich",
          "thumbnail": {
            "url":"https://i.imgur.com/OTFSldg.png"
          },
          "image": {
            "url":"{}".format(url)
          },
          "footer":{
            "text":"DuoAlert v{} | {}".format(version, timestamp),
            "icon_url":"https://i.imgur.com/OTFSldg.png"
          }
        }]
    }
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post(webhook_url, data=json.dumps(data), headers=headers)
    logging.info("Post data: {}".format(r))
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
        logging.info("Data file updated.")
    except Exception as e:
        logging.critical("Failed to open or write to data file. Aborting.")
        logging.critical("Exception was {}".format(e))

def check_data():
    #checks new data vs saved
    previous_r = open('streak_data.json')
    previous = json.load(previous_r)
    previous_r.close()
    logging.info("Loaded streak data.")
    for user in previous.keys():
        ph = get_phrase()
        phtext = ph["text"]
        phurl = ph["url"]
        logging.info("Loop 1 for {}: New: {} Old:{}".format(user, streak_data[user], previous[user]))
        if streak_data[user] == previous[user]:
            logging.info("No new streak for {}. Skipping.".format(user))
        elif streak_data[user] > previous[user]:
            if streak_data[user] > 1:
                send_discord("@everyone {} has continued their streak of {} days! {}!".format(user, streak_data[user], phtext), phurl)
                logging.info("{} has extended their streak.".format(user))
            elif streak_data[user] == 1:
                send_discord("@everyone {} has restarted their streak! Clap with pity.".format(user))
                logging.info("{} restarted their streak".format(user))
            else:
                send_discord("This message should not have been sent... *stratches head*. If recieved, call the president! Set DEFCON 1!")
                logging.critical("WTH just happened")
        elif streak_data[user] is 0 and previous[user] > 0:
            send_discord("@everyone {} has lost their streak! Tease them mercilessly.".format(user))
            logging.info("{} failed their streak. Loser.".format(user))
def get_streak(data_p):
    streak = data_p["site_streak"]
    return streak


def main():
    # check if existing saved data
    logging.info(complete_timestamp)
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
