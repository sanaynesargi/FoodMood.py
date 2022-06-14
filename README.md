# **FoodMood**
## Food Image Compiler
### By: Sanay Nesargi

![Imgur Image](https://i.imgur.com/CZlzqlo.png)

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

FoodMood is a food compliler that takes your food images and outputs beautiful videos that have
predifined "reactions" at the bottom. Then in compiles these edited images into a video

- Note that images directly imported from iPhones may have to be converted from the HEIF format

## Features

- Works with images in any format
- Automatically adjusts image resolution
- Exports video as mp4

## Tech

Libraries Used:

- **OpenCV Python** - A port of OpenCV (a Computer Vision library) in Python
- **Numpy** - A library for working with arrays and objects in Python with C-like speeds
- **MoviePy** - A library to edit videos in python using ffmpeg
- **Python Standard Library** - The libraries of os and shutil to work with and edit files


## Installation

FoodMood requires Python 3.6+ to run.

- First install the dependencies (Preferably in a virtual environment)
- Then put your photos into the photos directory
- Run the program (main.py) and watch FoodMood work it's magic!

```sh
git clone https://github.com/sanaynesargi/FoodMood.py.git
cd FoodMood
(not required) python(version) -m venv env
(not required) activate the environment
!Remember to move photos to photos directory
pip(version) install -r requirements.txt
python(version) main.py
```


## License

MIT

Software is free to all
