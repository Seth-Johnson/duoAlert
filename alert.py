#!/usr/bin/env python3
from re import U
from PIL import Image, ImageDraw, ImageSequence
import requests, os, json, logging, time, datetime, random, io

#Basic Script Config Variables
streak_data = {}
version = "2.0"
login_url = "https://www.duolingo.com/login"

#Main API endpoints
api_endpoint = 'http://www.duolingo.com/users/'
giphy_endpoint = 'https://api.giphy.com/v1/gifs/random?api_key={}&tag={}&rating={}'

#Gets time and creates timestamp
timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d')
complete_timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
logging.basicConfig(filename="config/duoAlert.log", level=logging.CRITICAL)

#Function parses phrases data
def get_phrase():
    with open('phrases.json') as phrase_r:
        phrase = json.load(phrase_r)
        phrases = phrase['phrases']
        r = random.SystemRandom()
        get_phrase.v = r.choice(phrases)

#Function parses config data
def get_config(value):
    with open('config/config.json') as config_r:
        config = json.load(config_r)
        if not value == "password":
            logging.info("Config value {} loaded with output of {}".format(value, config[value]))
        return config[value]

def graphic_overlay(user, url):
    #Remove existing GIF
    if os.path.isfile("tmp/{}.gif".format(user)):
        os.remove("tmp/{}.gif".format(user))
    #Download GIF and same using user
    r = requests.get(url, allow_redirects=True)
    open("tmp/{}-giphy.gif".format(user), "wb").write(r.content)
    #Overlay User
    im = Image.open("tmp/{}-giphy.gif".format(user))
    msg = "{}!".format(user)
    frames = []

    for frame in ImageSequence.Iterator(im):
        d = ImageDraw.Draw(frame)

        w, h = d.textsize(msg)
        d.text((((im.width-w)/2)+.2,((im.height-h)/2)-.2), msg, fill="#000")
        d.text((((im.width-w)/2)-.2,((im.height-h)/2)+.2), msg, fill="#000")
        d.text((((im.width-w)/2)-.4,((im.height-h)/2)+.4), msg, fill="#000")
        d.text((((im.width-w)/2)+.4,((im.height-h)/2)-.4), msg, fill="#000")
        d.text(((im.width-w)/2,(im.height-h)/2), msg, fill="#fff")
        del d

        b = io.BytesIO()
        frame.save(b, format="GIF")
        frame = Image.open(b)

        frames.append(frame)
        
    frames[0].save('tmp/{}.gif'.format(user), save_all=True, append_images=frames[1:])
    return "{}.gif".format(user)

# Discord Chat Function, uses JSON to send to Discord Wekhook.
def send_discord(r_msg, user, url = None):
    if url is None:
        url = ""
    data = {
        "embeds":[{
          "title":"DuoAlert",
          "description":"{}".format(r_msg),
          "color":0xff8000,
          "type":"rich",
          "thumbnail": {
            "url":"https://i.imgur.com/ZoPDQV9.png"
          },
          "image": {
            "url":"attachment://{}".format(graphic_overlay(user, url))
          },
          "footer":{
            "text":"DuoAlert v{} | {} | Powered by GIPHY".format(version, timestamp),
            "icon_url":"https://i.imgur.com/vJGlCau.png"
          }
        }]
    }
    files = {
        'payload_json': (None, json.dumps(data), 'multipart/form-data'),
        'file2':(os.path.basename("tmp/{}".format(graphic_overlay(user, url))), open("tmp/{}".format(graphic_overlay(user, url)), 'rb'), 'multipart/form-data')
    }

    #Creates JSON  Data to POST to webhook.
    r = requests.post(get_config("webhook_url"), files=files)
    #Appends raw POST date to log file.
    logging.info("Post data: {}".format(r))
    logging.info(r.content)

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
                data_p = data_r.get(api_endpoint + user, cookies=session.cookies).json()
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
                    with requests.get(giphy_endpoint.format( get_config("giphy_apikey"), get_config("sadness_phrase"), get_config("giphy_rating"))) as imgapi:
                        sadness_gif = imgapi.json()["data"]["images"]["fixed_width_downsampled"]["url"]
                except Exception as e:
                    logging.exception("Failed to fetch or parse giphy data for keyword '{}'.".format(get_phrase.v["text"]))
                    logging.exception("Exception was: {}".format(e))
            else:
                sadness_gif = get_config("sadness_gif")

            #Verifies that all users have increased there streak
            if streak_data[current_user] > previous[current_user]:
                #Checks if user has continued their streak, and posts the results to Discord
                if streak_data[current_user] > 1:
                    send_discord("@everyone {} has continued their streak of {} days! {}!".format(current_user, streak_data[current_user], get_phrase.v["text"]), current_user, get_phrase.v["url"])
                    logging.info("{} has extended their streak.".format(current_user))
                #Check if user lost streak, and posts the results to Discord
                elif streak_data[current_user] == 1:
                    send_discord("@everyone {} has restarted their streak! Clap with pity.".format(current_user), current_user)
                    logging.info("{} restarted their streak".format(current_user))
            #If user has not increased streak, posts the results to Discord
            elif streak_data[current_user] == 0 and previous[current_user] > 0:
                send_discord("@everyone {} has lost their streak! Tease them mercilessly.".format(current_user), current_user, sadness_gif)
                logging.info("{} failed their streak. Loser.".format(current_user))

#Main function
def main():
    # check if existing saved data
    logging.info(complete_timestamp)
    #Checks if config is present, else throws error

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
    try:
        os.path.exists('config.json')
        main()
        time.sleep(300)
    except Exception as e:
        logging.critical("Failed to load configuration. Aborting.")
        logging.critical("Full error is: {}".format(e))
    