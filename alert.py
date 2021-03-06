#!/usr/bin/env python3

import urllib.request
import urllib.parse
import requests
import os
import json
import logging
import time
import datetime
import random

#Basic Script Config Variables
webhook_url = None
users = []
streak_data = {}
version = "1.0"
giphy_apikey = ""
phrase_r = {}
login_url = "https://www.duolingo.com/login"
sadness_gif = "https://media.giphy.com/media/Ty9Sg8oHghPWg/giphy.gif"

#Gets time and creates timestamp
timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d')
complete_timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
logging.basicConfig(filename="duoAlert.log", level=logging.INFO)

#Function parses phrases data
def get_phrase():
    with open('phrases.json') as phrase_r:
        phrase = json.load(phrase_r)
        phrases = phrase['phrases']
        r = random.SystemRandom()
        return r.choice(phrases)

#Function parses config data
def get_config():
    global users
    global webhook_url
    global giphy_apikey
    global giphy_rating
    global username
    global password
    with open('config.json') as config_r:
        config = json.load(config_r)
        webhook_url = config['webhook_url']
        users = config['users']
        logging.info(users)
        username = config['username']
        password = config['password']

        if config['use_giphy'] is True:
            giphy_apikey = config['giphy_apikey']
            giphy_rating = config['giphy_rating']

        logging.info("Config set.")

#Main API endpoints
api_endpoint = 'http://www.duolingo.com/users/'
giphy_endpoint = 'https://api.giphy.com/v1/gifs/random?api_key={}&tag={}&rating={}'

# Discord Chat Function, uses JSON to send to Discord Wekhook.
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
            "text":"DuoAlert v{} | {} | Powered by GIPHY".format(version, timestamp),
            "icon_url":"https://i.imgur.com/OTFSldg.png"
          }
        }]
    }
    #Creates JSON  Data to POST to webhook.
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post(webhook_url, data=json.dumps(data), headers=headers)
    #Appends raw POST date to log file.
    logging.info("Post data: {}".format(r))

#Login to get data from Duolingo
def login():
    global session
    login_data = {"login": username, "password": password}
    session = requests.Session()
    jwt = None
    headers = {}

    if jwt is not None:
        headers['Authorization'] = 'Bearer ' + jwt
        logging.info("Header Set")

    req = requests.Request('POST', login_url,json=login_data,headers=headers,cookies=session.cookies)
    prepped = req.prepare()
    request = session.send(prepped)
    attempt = request.json()

    if attempt.get('response') == 'OK':
        logging.info(request.headers['jwt'])
        logging.info("Logged In")

#Updates streak data of users in config file.
def update_data():
    global streak_data

    for user in users:
        logging.info("Loaded User:{}".format(user))
        try:
            with session as data_r:
                data_p = json.loads(json.dumps(data_r.get(api_endpoint + user, cookies=session.cookies).json()))
                logging.info("API url used {}".format(api_endpoint + user))
                streak = get_streak(data_p)
                streak_data[user] = streak
                logging.info("Streak for user {} is {}".format(user, streak))
        except Exception as e:
            logging.exception("Failed to fetch or parse data for user {}. Skipping.".format(user))
            logging.exception("Exception was: {}".format(e))
        continue

    logging.info("Updated Data")

#Updates streak_data.json with pulled data from update_data function
def update_data_file():
    try:
        streak_file = open("streak_data.json", 'w')
        #Gets data from global variable streak_data and writes to file
        streak_file.write(json.dumps(streak_data))
        streak_file.close()
        logging.info("Data file updated.")
    except Exception as e:
        logging.critical("Failed to open or write to data file. Aborting.")
        logging.critical("Exception was {}".format(e))

#Requests data from Duolingo
def check_data():
    #Checks new data vs saved
    previous_r = open('streak_data.json')
    previous = json.load(previous_r)
    previous_r.close()
    logging.info("Loaded streak data.")
    for user in previous.keys():
        #Gets phrase from get_phrase function
        ph = get_phrase()
        phtext = ph["text"]
        phurl = ph["url"]
        #Appends changes if any to log file
        logging.info("Loop 1 for {}: New: {} Old:{}".format(user, streak_data[user], previous[user]))
        #Checks if GIPHY api was set in config, if it doesnt falls back to links in phrases.json
        if not giphy_apikey == "":
            try:
                with urllib.request.urlopen(giphy_endpoint.format(giphy_apikey, urllib.parse.quote(phtext), giphy_rating)) as imgapi:
                    img_p = json.loads(imgapi.read().decode())
                    phurl = img_p["data"]["image_url"]
            except Exception as e:
                logging.exception("Failed to fetch or parse giphy data for keyword '{}'.".format(phtext))
                logging.exception("Exception was: {}".format(e))
        #Checks if user doesnt have streak; if so skips posting to discord
        if streak_data[user] == previous[user]:
            logging.info("No new streak for {}. Skipping.".format(user))
        #Verifies that all users have increased there streak
        elif streak_data[user] > previous[user]:
            #Checks if user has continued their streak, and posts the results to Discord
            if streak_data[user] > 1:
                send_discord("@everyone {} has continued their streak of {} days! {}!".format(user, streak_data[user], phtext), phurl)
                logging.info("{} has extended their streak.".format(user))
            #Check if user lost streak, and posts the results to Discord
            elif streak_data[user] == 1:
                send_discord("@everyone {} has restarted their streak! Clap with pity.".format(user))
                logging.info("{} restarted their streak".format(user))
            else:
                #Fallback message no one should ever see. . . ever!!
                send_discord("This message should not have been sent... *stratches head*. If recieved, call the president! Set DEFCON 1!")
                logging.critical("WTH just happened")
        #If user has not increased streak, posts the results to Discord
        elif streak_data[user] is 0 and previous[user] > 0:
            send_discord("@everyone {} has lost their streak! Tease them mercilessly.".format(user), sadness_gif)
            logging.info("{} failed their streak. Loser.".format(user))
#Returns steak data
def get_streak(data_p):
    streak = data_p["site_streak"]
    return streak

#Main function
def main():
    # check if existing saved data
    logging.info(complete_timestamp)
    #Checks if config is present, else throws error
    try:
        get_config()
    except Exception as e:
        logging.critical("Failed to load configuration. Aborting.")
        logging.critical("Full error is: {}".format(e))

    #Login into accoount 
    login()
    #Updates streak data from Duolingo
    update_data()
    #Verifies that streak_data.json is present and runs check_data to run main routine to verify if users streaks have changed
    if os.path.exists('streak_data.json'):
        check_data()
    #Updates streak_data.json with new data retrieved from Duolingo api
    update_data_file()
#Runs main function
main()
