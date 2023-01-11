import spotipy
import spotipy.util as util
import os

import time
import datetime

import requests
import wget
import shutil
import re #for non ASCII detector
import sys
import configparser
import math

import cv2
import numpy as np
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

#my idea section:

"""
✅ Non-Ascii support
❌ Enable or disable image output generation
❌ Add option to enable dominant color (officialy used on older android's by spotify)

"""



#end of user edit section 😁
OpenSans = 'assets/OpenSans-Regular.ttf'
NotoSans = 'assets/NotoSansSC-Regular.otf'
non_ascii_font = NotoSans

scope = "user-read-currently-playing"
version = "v4 Python"

inf = 1
osn = os.name

def config():
    if not os.path.exists("spotix_config.ini"):
        print(" ")
        myClientId = input("Please input your client id: ")
        mySecret = input("Please input your secret: ")
        print("Make sure you have your redirect-uri set to http://localhost:8888/callback in your spotify application")
        username = input("Please input your username: ")
        
        config = configparser.ConfigParser()
        config['LOGIN'] = {'client-id': myClientId,
                            'client-secret': mySecret,
                            'username': username}
        config['REDIRECT'] = {'redc': 'http://localhost:8888/callback'}

        config['custom'] = {
            'get_average_color': False,
            'get_dominant_color': True,
            'set_background_color': False,
            'background_color': (50, 50, 50),
            'delay': 20,
            'font': "OpenSans-Regular.ttf",
            'font_name_size': 97, 
            'font_artist_size': 80
        }
        with open('spotix_config.ini', 'w') as configfile:
            config.write(configfile)
        time.sleep(5)

    else:
        config = configparser.ConfigParser()

        # Read in the config file
        config.read('spotix_config.ini')

        # Access values in the config file
        myClientId = config.get('LOGIN', 'client-id')
        mySecret = config.get('LOGIN', 'client-secret')
        myRedirect = config.get('REDIRECT', 'redc')
        delay = config.get('custom', 'delay')

        get_average_color = config.get('custom', 'get_average_color')
        get_dominant_color = config.get('custom', 'get_dominant_color')

        if get_average_color == True:
            if get_dominant_color == True:
                get_average_color = False
                print("Using dominant color")
            else:
                get_dominant_color = False
                print("Using average color")

        font = config.get('custom', 'font')
        font_name_size = config.get('custom', 'font_name_size')
        font_artist_size = config.get('custom, font_artist_size')

        username = config.get('custom', 'username')
        background_color = config.get('custom', 'background_color')



def gen_token():
    config = configparser.ConfigParser()

    # Read in the config file
    config.read('spotix_config.ini')

    # Access values in the config file
    myClientId = config.get('LOGIN', 'client-id')
    mySecret = config.get('LOGIN', 'client-secret')
    myRedirect = config.get('REDIRECT', 'redc')

    username = config.get('LOGIN', 'username')

    if os.path.exists(".cache-"f'{username}'):
        os.remove(".cache-"f'{username}')
        print("deleted .cache-"f'{username}')
    """
        returns refreshed Spotify API authentication with defined credentials
    """
    start_time = time.time()
    scope = "user-read-currently-playing"

    token = util.prompt_for_user_token(username, scope, myClientId, mySecret, myRedirect)

    currenttime = time.ctime()
    sp = spotipy.Spotify(auth=token)
    print("Refreshing token |", f'{currenttime}')
    print("Using generated token for 1000 seconds")

    return start_time
        
def findfonts():
    if not os.path.exists(OpenSans):
        if not os.path.exists(NotoSans):
            print("fonts not found")
            return False
            
    
    else:
        return True

def checkfiles():

    print("----Folders----")
    #folders part
    if not os.path.exists('assets'):
        os.mkdir('assets')
        print("Folder assets not found")
    else:
        print("File assets already exist 😎")

    if not os.path.exists('output'):
        os.mkdir('output')
        print("Folder output not found")
    else:
        print("File output output exist 😎")
    
    print(" ")
    print("----Fonts----")
    
    checkfonts = findfonts()

    if checkfonts == False:
        #font part
        OpenSans_file_name = 'Open_sans.zip'
        non_ascii_file_name = 'Noto_Sans_SC.zip'
        OpenSans_url = 'https://fonts.google.com/download?family=Open%20Sans'
        non_ascii_font_url = 'https://fonts.google.com/download?family=Noto%20Sans%20SC'
        OpenSans_extract_dir = 'assets/' + OpenSans_file_name
        non_ascii_extract_dir = 'assets/' + non_ascii_file_name


        if not os.path.exists(OpenSans):
            #download OpenSans
            print("Missing " f'{OpenSans}' " 💀")
            print("Downloading needed fonts (1) 📡")
            wget.download(OpenSans_url)
            print(" ")
            shutil.move(OpenSans_file_name , OpenSans_extract_dir)
            print("Unpacking font (1) ⚙")
            shutil.unpack_archive(OpenSans_extract_dir, "assets/")

            #now the very fun part :(
            print("Moving downloaded font (1) 🔁")
            shutil.move('assets/static/OpenSans/OpenSans-Regular.ttf', 'assets/')
                #removing crap
            print("Removing crap (1) 🚮")
            shutil.rmtree('assets/static')
            os.remove(OpenSans_extract_dir)
            os.remove('assets/README.txt')
                #yes im keeping the licence file
            os.rename('assets/OFL.txt', 'assets/OFL_OpenSans.txt')
            print('Done ✅')

        if not os.path.exists("assets/NotoSansSC-Regular.otf"):
            print('')
            print("Missing " f'{NotoSans}' " 💀")
            print("Downloading needed fonts (2) 📡")
            wget.download(non_ascii_font_url)
            print(" ")
            #font downloaded
            print("Moving downloaded font (1) 🔁")
            shutil.move(non_ascii_file_name , "assets/")
            print("Unpacking font (2) ⚙")
            shutil.unpack_archive(non_ascii_extract_dir, "assets/")
                #now the very fun part :(
                #removing crap
            print("Removing crap (2) 🚮")
            os.remove(non_ascii_extract_dir)
            os.remove('assets/NotoSansSC-Black.otf')
            os.remove('assets/NotoSansSC-Bold.otf')
            os.remove('assets/NotoSansSC-Light.otf')
            os.remove('assets/NotoSansSC-Medium.otf')
            os.remove('assets/NotoSansSC-Thin.otf')
                #yes im keeping the licence file
            os.rename('assets/OFL.txt', 'assets/OFL_NotoSans.txt')
            print('Done ✅')

            time.sleep(2)
        time.sleep(2)

    else:
        print("Fonts already downloaded 😎")
        time.sleep(2)

def cjk_detect(texts):
    # korean
    if re.search("[\uac00-\ud7a3]", texts):
        return True
    # japanese
    if re.search("[\u3040-\u30ff]", texts):
        return True
    # chinese
    if re.search("[\u4e00-\u9FFF]", texts):
        return True
    return False


def clear():
    if(osn == 'posix'):
        os.system('clear')
    else:
        os.system('cls')


def checkstring(string):
    if string.isdigit():
        # The string is a valid integer, so we can safely interpret it as one
        integer = int(string)
    else:
        print(Exception)

    return(integer)

def is_color_white(color):
    white = (255, 255, 255)
    threshold = 55
    try: 
        distance = math.sqrt((white[0]-color[0])**2 + (white[1]-color[1])**2 + (white[2]-color[2])**2)
        if distance < threshold:
            return True
        else:
            return False
    except:
        print("error checking for white")
        return True

def averageimg():
    config = configparser.ConfigParser()

    # Read in the config file
    config.read('spotix_config.ini')

    # Access values in the config file
    myClientId = config.get('LOGIN', 'client-id')
    mySecret = config.get('LOGIN', 'client-secret')
    myRedirect = config.get('REDIRECT', 'redc')

    font = config.get('custom', 'font')
    font = "assets/{}".format(font)

    font_name_size = config.get('custom', 'font_name_size')
    font_artist_size = config.get('custom', 'font_artist_size')

    username = config.get('LOGIN', 'username')

    token = util.prompt_for_user_token(username, scope, myClientId, mySecret, myRedirect)
    sp = spotipy.Spotify(auth=token)
    currentsong = sp.currently_playing()

    while True:
        try: 
            currentsong = sp.currently_playing()
            song_name = currentsong['item']['name']
        except spotipy.SpotifyException: #token expired
            print("Refreshing token")
            gen_token()
            break
        
        except TypeError: #checks if something is playing
            logo()
            print("Nothing is playing at the moment | {}".format(datetime.datetime.now().strftime("%H:%M:%S")))
            time.sleep(5)
            clear()
        else:
            break

    song_image = currentsong['item']['album']['images'][0]['url']
    song_artist = currentsong['item']['artists'][0]['name']

    url = song_image

    #simple request for cover image
    r = requests.get(url, stream=True)
    ext = r.headers['content-type'].split('/')[-1] # converts response headers mime type to an extension (may not work with everything)
    with open("output/icon.jpeg" , 'wb') as f: # open the file to write as binary - replace 'wb' with 'w' for text files
        for chunk in r.iter_content(1024): # iterate on stream using 1KB packets
            f.write(chunk) # write the file

    # Calculate the average color of the image
    src_img = cv2.imread('output/icon.jpeg')
    average_color_row = np.average(src_img, axis=0)
    average_color = np.average(average_color_row, axis=0)

    '''
    cv2.imshow('Source image',src_img)
    cv2.imshow('Average Color',average_color_row)
    cv2.waitKey(1)
    '''

    #convert to simple brackets
    average_color = average_color.astype(np.uint)
    average_color_tuple = (*average_color,)

    print("Average color (RGB): " + f'{average_color_tuple}')

    #building the final image
    img = Image.open('output/icon.jpeg', 'r')

    background = Image.new('RGB', (1920, 640), average_color_tuple)
    offset = (0, 0)
    background.paste(img, offset)
    draw = ImageDraw.Draw(background)

    if cjk_detect(song_name) == True:
        non_ascii_font_size = int(font_name_size) - 15

        name = ImageFont.truetype(non_ascii_font, non_ascii_font_size)
        print("Found non ASCII chars in song's name")
    else:
        name = ImageFont.truetype(font, int(font_artist_size))

    if cjk_detect(song_image) == True:
        non_ascii_font_size = int(font_artist_size) - 15

        art = ImageFont.truetype(non_ascii_font, non_ascii_font_size)
        print("Found non ASCII chars in song's artist")
    else:
        art = ImageFont.truetype(font, int(font_artist_size))

    if is_color_white(average_color_tuple) == True:
        draw.text((650, 240),song_name,(0,0,0),font=name)
        draw.text((650, 320),song_artist,(0,0,0),font=art)
    else:
        draw.text((650, 240),song_name,(255,255,255),font=name)
        draw.text((650, 320),song_artist,(255,255,255),font=art)

    background.save('output/output.jpeg')

def dominantimg():
    config = configparser.ConfigParser()

    # Read in the config file
    config.read('spotix_config.ini')

    # Access values in the config file
    myClientId = config.get('LOGIN', 'client-id')
    mySecret = config.get('LOGIN', 'client-secret')
    myRedirect = config.get('REDIRECT', 'redc')

    font = config.get('custom', 'font')
    font = "assets/{}".format(font)

    font_name_size = config.get('custom', 'font_name_size')
    font_artist_size = config.get('custom', 'font_artist_size')

    username = config.get('LOGIN', 'username')

    token = util.prompt_for_user_token(username, scope, myClientId, mySecret, myRedirect)
    sp = spotipy.Spotify(auth=token)
    currentsong = sp.currently_playing()

    while True:
        try: 
            currentsong = sp.currently_playing()
            song_name = currentsong['item']['name']
        except spotipy.SpotifyException: #token expired
            print("Refreshing token")
            gen_token()
            break
        
        except TypeError: #checks if something is playing
            logo()
            print("Nothing is playing at the moment | {}".format(datetime.datetime.now().strftime("%H:%M:%S")))
            time.sleep(5)
            clear()
        else:
            break

    song_image = currentsong['item']['album']['images'][0]['url']
    song_artist = currentsong['item']['artists'][0]['name']

    url = song_image

    #simple request for cover image
    r = requests.get(url, stream=True)
    ext = r.headers['content-type'].split('/')[-1] # converts response headers mime type to an extension (may not work with everything)
    with open("output/icon.jpeg" , 'wb') as f: # open the file to write as binary - replace 'wb' with 'w' for text files
        for chunk in r.iter_content(1024): # iterate on stream using 1KB packets
            f.write(chunk) # write the file

    # Calculate the average color of the image
    img = Image.open('output/icon.jpeg', 'r')
    colors = img.getcolors(img.size[0] * img.size[1])

    # Sort the list of colors by count
    sorted_colors = sorted(colors, key=lambda t: t[0])

    # Get the most frequent color
    dominant_color = sorted_colors[-1][1]

    if dominant_color == '255':
        dominant_color = (255, 255, 255)
    print("Dominant color = {}".format(dominant_color))


    background = Image.new('RGB', (1920, 640), dominant_color)

    offset = (0, 0)
    background.paste(img, offset)
    draw = ImageDraw.Draw(background)

    if cjk_detect(song_name) == True:
        non_ascii_font_size = int(font_name_size) - 15

        name = ImageFont.truetype(non_ascii_font, non_ascii_font_size)
        print("Found non ASCII chars in song's name")
    else:
        name = ImageFont.truetype(font, int(font_artist_size))

    if cjk_detect(song_image) == True:
        non_ascii_font_size = int(font_artist_size) - 15

        art = ImageFont.truetype(non_ascii_font, non_ascii_font_size)
        print("Found non ASCII chars in song's artist")
    else:
        art = ImageFont.truetype(font, int(font_artist_size))

    if is_color_white(dominant_color) == True:
        draw.text((650, 240),song_name,(0,0,0),font=name)
        draw.text((650, 320),song_artist,(0,0,0),font=art)
    else:
        draw.text((650, 240),song_name,(255,255,255),font=name)
        draw.text((650, 320),song_artist,(255,255,255),font=art)

    background.save('output/output.jpeg')

def setcolor():
    config = configparser.ConfigParser()

    # Read in the config file
    config.read('spotix_config.ini')

    # Access values in the config file
    myClientId = config.get('LOGIN', 'client-id')
    mySecret = config.get('LOGIN', 'client-secret')
    myRedirect = config.get('REDIRECT', 'redc')

    font = config.get('custom', 'font')
    font = "assets/{}".format(font)

    font_name_size = config.get('custom', 'font_name_size')
    font_artist_size = config.get('custom', 'font_artist_size')

    username = config.get('LOGIN', 'username')

    background_color = config.get('custom', 'background_color')

    token = util.prompt_for_user_token(username, scope, myClientId, mySecret, myRedirect)
    sp = spotipy.Spotify(auth=token)
    currentsong = sp.currently_playing()

    while True:
        try: 
            currentsong = sp.currently_playing()
            song_name = currentsong['item']['name']
        except spotipy.SpotifyException: #token expired
            print("Refreshing token")
            gen_token()
            break
        
        except TypeError: #checks if something is playing
            logo()
            print("Nothing is playing at the moment | {}".format(datetime.datetime.now().strftime("%H:%M:%S")))
            time.sleep(5)
            clear()
        else:
            break

    song_image = currentsong['item']['album']['images'][0]['url']
    song_artist = currentsong['item']['artists'][0]['name']

    url = song_image

    #simple request for cover image
    r = requests.get(url, stream=True)
    ext = r.headers['content-type'].split('/')[-1] # converts response headers mime type to an extension (may not work with everything)
    with open("output/icon.jpeg" , 'wb') as f: # open the file to write as binary - replace 'wb' with 'w' for text files
        for chunk in r.iter_content(1024): # iterate on stream using 1KB packets
            f.write(chunk) # write the file

    print("Using color from config (RGB): {}".format(background_color))
    background = Image.new('RGB', (1920, 640), eval(background_color))

    img = Image.open('output/icon.jpeg', 'r')
    offset = (0, 0)
    background.paste(img, offset)
    draw = ImageDraw.Draw(background)

    if cjk_detect(song_name) == True:
        non_ascii_font_size = int(font_name_size) - 15

        name = ImageFont.truetype(non_ascii_font, non_ascii_font_size)
        print("Found non ASCII chars in song's name")
    else:
        name = ImageFont.truetype(font, int(font_artist_size))

    if cjk_detect(song_image) == True:
        non_ascii_font_size = int(font_artist_size) - 15

        art = ImageFont.truetype(non_ascii_font, non_ascii_font_size)
        print("Found non ASCII chars in song's artist")
    else:
        art = ImageFont.truetype(font, int(font_artist_size))

    if is_color_white(eval(background_color)) == True:
        draw.text((650, 240),song_name,(0,0,0),font=name)
        draw.text((650, 320),song_artist,(0,0,0),font=art)
    else:
        draw.text((650, 240),song_name,(255,255,255),font=name)
        draw.text((650, 320),song_artist,(255,255,255),font=art)

    background.save('output/output.jpeg')


def getname():

        config = configparser.ConfigParser()

        # Read in the config file
        config.read('spotix_config.ini')

        # Access values in the config file
        myClientId = config.get('LOGIN', 'client-id')
        mySecret = config.get('LOGIN', 'client-secret')
        myRedirect = config.get('REDIRECT', 'redc')
        username = config.get('LOGIN', 'username')

        token = util.prompt_for_user_token(username, scope, myClientId, mySecret, myRedirect)
        sp = spotipy.Spotify(auth=token)
        currentsong = sp.currently_playing()

        while True:
            try: 
                currentsong = sp.currently_playing()
                song_name = currentsong['item']['name']
            except spotipy.SpotifyException: #token expired
                print("Refreshing token")
                gen_token()
                break
            
            except TypeError: #checks if something is playing
                logo()
                print("Nothing is playing at the moment | {}".format(datetime.datetime.now().strftime("%H:%M:%S")))
                time.sleep(5)
                clear()
            else:
                break

        song_artist = currentsong['item']['artists'][0]['name']
        song_image = currentsong['item']['album']['images'][0]['url']

        out = {
            "NAME": song_name,
            "ARTIST": song_artist
        }

        print("Now playing {} by {}".format(song_name, song_artist), "🎶")

        txtoutput = song_name + " by " + song_artist

        if cjk_detect(txtoutput) == True:
            with open("output/song.txt", "w",encoding='utf-8') as f:
                f.writelines(txtoutput)
                f.close
                
        else:
            f = open("output/song.txt", "w")
            f.write(txtoutput)
            f.close
    
        url = song_image
        last_url = "0"
        return out

#ascii art 👑

def art():
    osn = os.name
    print(r"""
       ____ 
      / __/
     _\ \/
    /___/

                                """)
    time.sleep(.5)
    clear()

    print(r"""
       ____ 
      / __/__  
     _\ \/ _ \
    /___/ .__/
       /_/                     
                                """)
    time.sleep(.5)
    clear()

    print(r"""
       ____   
      / __/__  ___ 
     _\ \/ _ \/ _ \
    /___/ .__/\___/
       /_/                     
                                """)
    time.sleep(.5)
    clear()

    print(r"""
       ____          __ 
      / __/__  ___  / /_
     _\ \/ _ \/ _ \/ __/
    /___/ .__/\___/\__/
       /_/                     
                                """)
    time.sleep(.5)
    clear()

    print(r"""
       ____          __  _     
      / __/__  ___  / /_(_)
     _\ \/ _ \/ _ \/ __/ /
    /___/ .__/\___/\__/_/
       /_/                     
                                """)
    time.sleep(.5)
    clear()

    print("""
       ____          __  _     
      / __/__  ___  / /_(_)_ __
     _\ \/ _ \/ _ \/ __/ /\ \ /
    /___/ .__/\___/\__/_//_\_\  {}
       /_/                     
                                """.format(version))

def updelay():
    repeat = 0
    config = configparser.ConfigParser()
    config.read('spotix_config.ini')
    # Access values in the config file
    delay = config.get('custom', 'delay')

    print("Delay in seconds: "f'{delay}')
    while int(delay) > repeat:
        repeat = repeat + 1
        time.sleep(1)
        print("["f'{repeat}'"]", end='',flush=True)

def logo():
            print("""
            ____          __  _     
           / __/__  ___  / /_(_)_ __
          _\ \/ _ \/ _ \/ __/ /\ \ /
         /___/ .__/\___/\__/_//_\_\  {}
            /_/                     
                                    """.format(version))



def main():

    #start
    art()

    checkfiles() #checks if folders and fonts are OK
    if not os.path.exists("spotix_config.ini"):
        config()

    start_time = gen_token()
    start_output = start_time + 1000

    time.sleep(5)

    clear()
    #ez infinity loop
    while inf == 1:
        new_time = time.time()

        #yeah you need to keep the token alive as well 🏥
        if new_time < start_time + 1000:
            logo() #hehe


            remaining = start_output - new_time
            tokenage = np.round(remaining)
            #prints all info !
            print("Remaining seconds till token refresh: " f'{tokenage}')

            config = configparser.ConfigParser()

            # Read in the config file
            config.read('spotix_config.ini')

            get_average_color = config.get('custom', 'get_average_color')

            get_dominant_color = config.get('custom', 'get_dominant_color')

            set_background_color = config.get('custom', 'set_background_color')

            if get_dominant_color == 'True': #gets dominant color if set in config
                if get_average_color == 'True':
                    clear()
                    print("Only one option please :D")
                    print("get_average OR get_dominant OR set_background")
                    time.sleep(10)
                    exit("Two or more options set in config")
                if set_background_color == 'True':
                    clear()
                    print("Only one option please :D")
                    print("get_average OR get_dominant OR set_background")
                    time.sleep(10)
                    exit("Two or more options set in config")
                dominantimg()

            if get_average_color == 'True': #gets average color if set in config
                if get_dominant_color == 'True':
                    clear()
                    print("Only one option please :D")
                    print("get_average OR get_dominant OR set_background")
                    time.sleep(10)
                    exit("Two or more options set in config")
                if set_background_color == 'True':
                    clear()
                    print("Only one option please :D")
                    print("get_average OR get_dominant OR set_background")
                    time.sleep(10)
                    exit("Two or more options set in config")
                averageimg()

            if set_background_color == 'True': #gets set background color as set in config
                if get_dominant_color == 'True':
                    clear()
                    print("Only one option please :D")
                    print("get_average OR get_dominant OR set_background")
                    time.sleep(10)
                    exit("Two or more options set in config")
                if get_average_color == 'True':
                    clear()
                    print("Only one option please :D")
                    print("get_average OR get_dominant OR set_background")
                    time.sleep(10)
                    exit("Two or more options set in config")
                setcolor()

            getname()
            updelay()
            

        else:
            #this is where the magic happens (token refresh!)
            start_time = gen_token()
            start_output = start_time + 1000
            gen_token()
            updelay()

        clear()

main()

    
