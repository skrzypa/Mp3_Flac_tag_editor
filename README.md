### Python and library versions
1. python 3.11.1
1. mutagen 1.46.0
1. pyinstaller 6.1.0
1. flet==0.10.3
```
pip install mutagen==1.46.0 pyinstaller==6.1.0 flet==0.10.3
```

#
### About project
A simple program for tagging mp3 and flac files with a GUI made with the help of the library Mutangen and. This program renames files, adds artist name, album name, release year, music genre and cover art.

#
### How to use
1. Create folder with 
    1. tracklist.txt file
    1. cover image (.jpg, .jpeg or .png)
    1. music files (.mp3 or .flac)
  
1. The tracklist file must look like this
```
artist name
album title
release year
genre
song title 1
song title 2
song title 3
song title 4
...
```

#
### If you want add your language
Translate languages.json like this on each row
```
"Wybierz plik z tracklistą","Select a tracklist file","<text in your language>"
```

Add code in paths_settings.py
```
langs = {"PL": 0,
        "EN": 1,
        "<code>": 2  
}
```

Change code in settings.json
```
{
    "language": "<code>"
}
```

#
### Create .exe file with pyinstaller
    pyinstaller -F "path/to/file.py"

#
#### Optional with icon, title and without console
    pyinstaller -F "path/to/file.py" --icon="path/to/icon.png" --noconsole -n "AppName"

#
### Example of use
https://www.pskrzynski.pl/flac_mp3_tag/#chapter6