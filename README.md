# Spotix
Spotify streaming tool - Spotix is a tool that enables you to have spotify current playing song on your stream!

This is one of the outpusts you can get with Spotix!

![This is output](https://github.com/wrexik/Spotix/blob/main/output/output.jpeg)

# Instalation:
1. First of all you need to create spotify application [here](https://developer.spotify.com/dashboard/applications)
  Log in and create application make sure you set Uri redirect to `http://localhost:8888/callback`
2. And now let's install requirements with `python -m pip install -r requirements.txt` and we are done here!
3. Now we'll edit the tool to work with spotify. Open `main.py` and edit these variables to match your spotify application
4. **Dont forget** put the font (agrane.ttf for example) into assets folder and change the name to the fonts name in the config!
```
myClientId='YourClientId'
mySecret='YourSecret'

font = "agrane.ttf" #or your font name
```
# Customization:
Tool has options to custumize output text, color and font

### Text:
To change font, download font in `.ttf` format and put it in the folder named assets
next set `font = 'YourFontName.ttf'` dont forget the `.ttf`

To change size easily edit `font_name_size = 74` and `font_artist_size = 70`.

That means `font_name_size` is name of the song
and `font_artist_size` is the name of the artist

### Color:
To disable average color use `getcolor = True/False`.
To change color use `background_color = YourRGBValue` (don't forget it needs to be in tuple)

# ToDo:
- [ ] **Detect when nothing is playing**
- [ ] fit text to image output
- [ ] more customization and dominant color maybe
- [ ] support for chinesse characters
