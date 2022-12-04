import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import os
import time
from spotipy.oauth2 import SpotifyOAuth
import requests

import cv2
import numpy as np
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

#user edit section
myClientId='c0a96d6c83c142cc88d0429d3da466db'
mySecret='12fc1005272d487ca8e70c9e24e8e225'

#you dont have to edit myRedirect just make sure you have same one in your spotify application
myRedirect='http://localhost:8888/callback'

#get avreage color from album cover
getcolor = True                 #If False tool will use color set down below. If True tool will calculate avrerage color from the image
background_color = (50, 50, 50) #input wanted rgb color for image background 

#request delay (updates in seconds)
#its also limited with spotify max requests and image generation
delay = 10
#font (download font in .tff format and put it in the assets folder and dont forget to rename this variable)
font = "agrane.ttf"
font_name_size = 97
font_artist_size = 80

#username (just to sort the tokens and stuff)
username = "Wrexik"


#end of user edit section 😁
scope = "user-read-currently-playing"
version = "v2.1"
osn = os.name

token = util.prompt_for_user_token(username, scope, myClientId, mySecret, myRedirect)

CREDENTIALS = spotipy.oauth2.SpotifyClientCredentials(client_id=myClientId,
                                                     client_secret=mySecret)
def gen_token():
    """
        returns refreshed Spotify API authentication with defined credentials
    """
    start_time = time.time()
    username = "Wrexik"
    scope = "user-read-currently-playing"

    token = util.prompt_for_user_token(username, scope, myClientId, mySecret, myRedirect)

    currenttime = time.ctime()

    sp = spotipy.Spotify(auth=token)
    print("Refreshing token |", f'{currenttime}')
    print("Using generated token for 3600 seconds")
    return start_time

def checkfile():
    if not os.path.exists('assets'):
        os.mkdir('assets')
    else:
        print("File assets already exist 😎")

    if not os.path.exists('output'):
        os.mkdir('output')
    else:
        print("File assets output exist 😎")

def clear():
    if(osn == 'posix'):
        os.system('clear')
    else:
        os.system('cls')

def getimage():
        sp = spotipy.Spotify(auth=token)
        currentsong = sp.currently_playing()
        song_name = currentsong['item']['name']
        song_image = currentsong['item']['album']['images'][0]['url']
        song_artist = currentsong['item']['artists'][0]['name']
            
    
        url = song_image

        #simple request for cover image
        r = requests.get(url, stream=True)
        ext = r.headers['content-type'].split('/')[-1] # converts response headers mime type to an extension (may not work with everything)
        with open("output/icon.jpeg" , 'wb') as f: # open the file to write as binary - replace 'wb' with 'w' for text files
            for chunk in r.iter_content(1024): # iterate on stream using 1KB packets
                f.write(chunk) # write the file

        #creates background from average color
        if getcolor == False:
            average_color_tuple = background_color
        else:
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
            name = ImageFont.truetype("assets/"f'{font}', font_name_size)
            art = ImageFont.truetype("assets/"f'{font}', font_artist_size)

            #prints song name & artist
            draw.text((650, 240),song_name,(255,255,255),font=name)
            draw.text((650, 320),song_artist,(255,255,255),font=art)
            background.save('output/output.jpeg')
 

def getname():
        sp = spotipy.Spotify(auth=token)
        currentsong = sp.currently_playing()

        song_name = currentsong['item']['name']
        song_artist = currentsong['item']['artists'][0]['name']
        song_image = currentsong['item']['album']['images'][0]['url']

        out = {
            "NAME": song_name,
            "ARTIST": song_artist
        }

        print("Now playing {} by {}".format(song_name, song_artist), " 🎶")

        filewrite = song_name + " by " + song_artist
        f = open("output/song.txt", "w")
        f.write(filewrite)
        f.close
    
        url = song_image
        last_url = "0"
        return out

#ascii art 👑

def ascii():
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
    print("Delay in seconds: "f'{delay}')
    while delay > repeat:
        repeat = repeat + 1
        time.sleep(1)
        print("["f'{repeat}'"]", end='',flush=True)

ascii()

inf = 1
down = False
checkfile()
start_time = gen_token()
start_output = start_time + 3500

time.sleep(2)

clear()
#ez infinity loop
while inf == 1:

    print("""
         ____          __  _     
        / __/__  ___  / /_(_)_ __
       _\ \/ _ \/ _ \/ __/ /\ \ /
      /___/ .__/\___/\__/_//_\_\  {}
         /_/                     
                                """.format(version))

    new_time = time.time()

    #yeah you need to keep the token alive as well 🏥
    if new_time < start_time + 3500:
        remaining = start_output - new_time
        tokenage = np.round(remaining)
        #prints all info !
        print("Remaining seconds till token refresh: " f'{tokenage}')

    else:
        #this is where the magic happens (token refresh!)
        start_time = gen_token()
        start_output = start_time + 3500
        gen_token()
        updelay()

    clear()

    
