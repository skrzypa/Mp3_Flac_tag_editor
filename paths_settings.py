import pathlib
import csv
import json
import sys
import os

PATH = pathlib.Path(sys.executable).parent # when program is .exe file
if not os.path.exists(os.path.join(PATH, 'settings.json')): # if program is not an .exe file
    PATH = pathlib.Path(__file__).parent


ICON_PATH : str = str(pathlib.Path(PATH, "icon.png"))
BANNER_PATH : str = str(pathlib.Path(PATH, "banner.png"))


LANGS = {
    "PL": 0,
    "EN": 1,
}


with open(file= str(pathlib.Path(PATH, "settings.json")), mode= "r", encoding= "UTF-8") as file:
    read = json.load(file)
    
LANG = LANGS[read['language']]
RES_X, RES_Y = read['resolution']


with open(file= str(pathlib.Path(PATH, "languages.csv")), 
          mode= "r",
          encoding= "UTF-8") as file:
    reader = csv.reader(file)

    LANGUAGES = next(reader)
    LANGUAGES_CODES = next(reader)
    CHANGE_LANGUAGE = next(reader)[LANG]
    CHOOSE_FILE = next(reader)[LANG]
    CHOOSE_CORRECT_FILE = next(reader)[LANG]
    FILTER_TXT = next(reader)[LANG]
    FILTER_ALL = next(reader)[LANG]
    SOURCE_CODE = next(reader)[LANG]
    TIME_DELTA = next(reader)[LANG]
    TAGGING = next(reader)[LANG]
    START = next(reader)[LANG]
    PROGRESS = next(reader)[LANG]
    CLOSE = next(reader)[LANG]


def change_language(choosen_lang):
    langs = {k:v for k,v in zip(LANGUAGES, LANGUAGES_CODES)}
    choosen_lang = langs[choosen_lang]

    with open(file= pathlib.Path(PATH, 'settings.json'), mode='r', encoding= "UTF-8") as file:
        load = json.load(fp= file)
        load['language'] = choosen_lang
    
    with open(file= pathlib.Path(PATH, 'settings.json'), mode='w', encoding= "UTF-8") as file:
        json.dump(obj= load, fp= file, indent= 4)
