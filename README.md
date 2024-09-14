# Spotix
Spotify streaming tool - Spotix is a tool that enables you to have spotify current playing song on your stream!

This is one of the outputs you can get with Spotix!

![This is output](https://github.com/wrexik/Spotix/blob/main/output/output.jpeg)

# Installation Python ⚙:
1. First of all you need to create spotify application [here](https://developer.spotify.com/dashboard/applications)
  Log in and create application make sure you set Uri redirect to `http://localhost:8888/callback`
2. And now let's install requirements with `python -m pip install -r requirements.txt` and we are done here!
3. Now we'll edit the tool to work with spotify. Download `main.py` from [here](https://github.com/wrexik/Spotix/releases)
4. Run the `main.py` and paste in your `client-id` and `client-secret` finally set your username!
5. And enjoy. Outputs are located in `output` folder

# Installation for exe ⚙:
1. First of all you need to create spotify application [here](https://developer.spotify.com/dashboard/applications) Log in and create application make sure you set Uri redirect to `http://localhost:8888/callback`
3. Download exe from [here](https://github.com/wrexik/Spotix/releases)
4. Run the exe and paste in your `client-id` and `client-secret` finally set your username!
5. And enjoy. Outputs are located in `output` folder


# Customization 🔧:
Tool has options to custumize output text, color and font.

**All accesable in `spotix_config.ini`**

### Text 📃:
- Font's are downloaded automaticaly on first run! but it's needed to have them because the tool checks for them everytime.
- To change font, download font in `.ttf` format and put it in the folder named `fonts` next set `font = 'YourFontName.ttf'` don't forget the `.ttf` and done.

- To change size easily edit `font_name_size = 97` and `font_artist_size = 80`.

That means `font_name_size` is name of the song
and `font_artist_size` is the name of the artist

### Color 🎨:
- To disable / enable average color use `get_average_color = True/False`.
- To disable / enable dominant color use `get_dominant_color = True/False`
- To change color enable `set_background_color = True` and set `background_color = YourRGBValue` (don't forget it needs to be in tuple)

# To Do 🎛:
- [x] **Detect when nothing is playing**
- [x] Support for chinesse characters
- [x] Still background color
- [x] Dominant color maybe
- [x] Token refresh
