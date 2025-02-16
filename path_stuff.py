from sys import path
from os.path import abspath
from os import getcwd
import pygame

from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir("media/main_game/moon_types") if isfile(join("media/main_game/moon_types", f))]
print(onlyfiles)