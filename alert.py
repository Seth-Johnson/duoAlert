#!/usr/bin/env python3
import requests
import os
import json
import logging
import time
import datetime
import random

#Basic Script Config Variables
streak_data = {}
version = "2.0"
login_url = "https://www.duolingo.com/login"
sadness_gif = "https://media.giphy.com/media/Ty9Sg8oHghPWg/giphy.gif"
sadness_phrase = "Sadness"

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
        get_phrase.v = r.choice(phrases)

#Function parses config data
def get_config(value):
    with open('config.json') as config_r:
        config = json.load(config_r)
        if not value == "password":
            logging.info("Config value {} loaded with output of {}".format(value, config[value]))
        return config[value]

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
            "url":"https://i.imgur.com/ZoPDQV9.png"
          },
          "image": {
            "url":"{}".format(url)
          },
          "footer":{
            "text":"DuoAlert v{} | {} | Powered by GIPHY".format(version, timestamp),
            "icon_url":"https://i.imgur.com/vJGlCau.png"
          }
        }]
    }
    #Creates JSON  Data to POST to webhook.
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post(get_config("webhook_url"), data=json.dumps(data), headers=headers)
    #Appends raw POST date to log file.
    logging.info("Post data: {}".format(r))

#Login to get data from Duolingo
def login():
    global session
    login_data = {"login": get_config("username"), "password": get_config("password")}
    session = requests.Session()

    req = requests.Request('POST', login_url,json=login_data,cookies=session.cookies)
    prepped = req.prepare()
    request = session.send(prepped)
    attempt = request.json()

    if attempt.get('response') == 'OK':
        logging.info("Logged In")

#Updates streak data of users in config file.
def update_data():
    global streak_data
    for user in get_config("users"):
        logging.info("Loaded User:{}".format(user))
        try:
            with session as data_r:
                jwt = session.cookies.get_dict()['jwt_token']
                headers = {"User-Agent": "Totally not python","Authorization": "Bearer {}".format(jwt)}
                #data_p = data_r.get(api_endpoint + user,headers=headers).json()
                data_p = requests.get(api_endpoint + user,headers=headers).json()
                logging.info("API url used {}".format(api_endpoint + user))
                streak_data[user] = data_p["site_streak"]
                logging.info("Streak for user {} is {}".format(user, data_p["site_streak"]))
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
    global sadness_gif
    #Checks new data vs saved
    previous = json.load(open('streak_data.json'))
    logging.info("Loaded streak data.")
    for current_user in get_config("users"):
        get_phrase()
        if current_user in previous:
            #Checks if GIPHY was set enabled config, if it doesnt falls back to links in phrases.json
            if get_config("use_giphy") and get_config("giphy_apikey"):
                try:
                    with requests.get(giphy_endpoint.format(get_config("giphy_apikey"), get_phrase.v["text"], get_config("giphy_rating"))) as imgapi:
                        get_phrase.v["url"] = imgapi.json()["data"]["images"]["fixed_width_downsampled"]["url"]
                    with requests.get(giphy_endpoint.format( get_config("giphy_apikey"), sadness_phrase, get_config("giphy_rating"))) as imgapi:
                        sadness_gif = imgapi.json()["data"]["images"]["fixed_width_downsampled"]["url"]
                except Exception as e:
                    logging.exception("Failed to fetch or parse giphy data for keyword '{}'.".format(get_phrase.v["text"]))
                    logging.exception("Exception was: {}".format(e))

            #Verifies that all users have increased there streak
            if streak_data[current_user] > previous[current_user]:
                #Checks if user has continued their streak, and posts the results to Discord
                if streak_data[current_user] > 1:
                    send_discord("@everyone {} has continued their streak of {} days! {}!".format(current_user, streak_data[current_user], get_phrase.v["text"]), get_phrase.v["url"])
                    logging.info("{} has extended their streak.".format(current_user))
                #Check if user lost streak, and posts the results to Discord
                elif streak_data[current_user] == 1:
                    send_discord("@everyone {} has restarted their streak! Clap with pity.".format(current_user))
                    logging.info("{} restarted their streak".format(current_user))
            #If user has not increased streak, posts the results to Discord
            elif streak_data[current_user] == 0 and previous[current_user] > 0:
                send_discord("@everyone {} has lost their streak! Tease them mercilessly.".format(current_user), sadness_gif)
                logging.info("{} failed their streak. Loser.".format(current_user))

#Main function
def main():
    # check if existing saved data
    logging.info(complete_timestamp)
    #Checks if config is present, else throws error
    try:
        os.path.exists('config.json')
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