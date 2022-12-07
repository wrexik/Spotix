import spotipy
import spotipy.util as util
import os
import time
import requests
import wget
import shutil
import re #for non ASCII detector

import cv2
import numpy as np
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

#user edit section
myClientId='YourClientId'
mySecret='YourSecret'

#you dont have to edit myRedirect just make sure you have same one in your spotify application
myRedirect='http://localhost:8888/callback'

#get avreage color from album cover
getcolor = True                 #If False tool will use color set down below. If True tool will calculate avrerage color from the image
background_color = (50, 50, 50) #input wanted rgb color for image background 

#request delay (updates in second)
#its also limited with spotify max requests and image generation
delay = 10
#font (download font in .tff format and put it in the assets folder and dont forget to rename this variable)
font = "OpenSans-Regular.ttf"
font_name_size = 97
font_artist_size = 80

#username (just to sort the tokens and stuff)
username = "Wrexik"


#end of user edit section 😁
OpenSans = 'assets/OpenSans-Regular.ttf'
NotoSans = 'assets/NotoSansSC-Regular.otf'
non_ascii_font = NotoSans

scope = "user-read-currently-playing"
version = "v3"

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
        
def findfonts():
    if not os.path.exists(OpenSans):
        if not os.path.exists(NotoSans):
            print("fonts not found")
            return False
            
    
    else:
        return True

def checkfiles():

    logo() #just logo


    print("----Folders----")
    #folders part
    if not os.path.exists('assets'):
        os.mkdir('assets')
    else:
        print("File assets already exist 😎")

    if not os.path.exists('output'):
        os.mkdir('output')
    else:
        print("File assets output exist 😎")
    
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

            if cjk_detect(song_name) == True:
                non_ascii_font_size = font_name_size - 15

                name = ImageFont.truetype(non_ascii_font, non_ascii_font_size)
                print("Found non ASCII chars in song's name")
            else:
                name = ImageFont.truetype("assets/"f'{font}', font_artist_size)

            if cjk_detect(song_image) == True:
                non_ascii_font_size = font_artist_size - 15

                art = ImageFont.truetype(non_ascii_font, non_ascii_font_size)
                print("Found non ASCII chars in song's artist")
            else:
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
    checkfiles() #checks if folders and fonts are OK
    ascii()
    inf = 1




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
            
            down = getimage()
            out = getname()
            updelay()

        else:
            #this is where the magic happens (token refresh!)
            start_time = gen_token()
            start_output = start_time + 3500
            gen_token()
            updelay()

        clear()

main()

    
