from mutagen.flac import FLAC, Picture
from mutagen.mp3 import EasyMP3
from mutagen.id3 import APIC, ID3

import pathlib
import re



class AutomaticTagging:
    """
    Example:\n 
    at = AutomaticTagging("path/to/tracklist.txt")\n
    for nr, (file, title, file_format) in enumerate(zip(at.music_files, at.titles, at.music_files_formats), start= 1):\n
        \tat.tag_music_file(nr, file, title, file_format)
        
    """
    def __init__(self, tracklist_file_path: str):
        self.photo_formats = ('png', 'jpg', 'jpeg')
        self.music_formats = ('.mp3', ".flac")

        self.prohibited_signs_in_file_name = ["\"", "\\", "/", ":", "|", "<", ">", "*", "?"]

        self.folder_path = pathlib.Path(tracklist_file_path).parent
        self.tracklist_file = tracklist_file_path

        self.music_files, self.music_files_formats = [], []

        for file in self.folder_path.iterdir():
            file = str(file)

            song_name = file.split("\\")[-1]

            if file.endswith(self.music_formats):
                self.music_files.append(file)
                self.music_files_formats.append(
                            re.findall(f"({'|'.join(self.music_formats)})", song_name)[-1]
                            )

            elif file.endswith(self.photo_formats):
                self.cover_file = file
        
        self.len_of_music_files = len(self.music_files)
        
        self._read_tracklist_file()


    def _read_tracklist_file(self):
        
        self.titles = []
        with open(self.tracklist_file, mode= 'r', encoding= "UTF-8") as tracklist:
            reader = [row.strip() for row in tracklist.readlines()]
            
        self.artist: str = reader[0]
        self.album_title: str = reader[1]
        self.year: str = reader[2]
        self.genre: str = reader[3]
        self.titles: list = reader[4:]
        


    def tag_music_file(self, nr, old_file, title, file_format):

        self.nr = str(nr).zfill(len(str(self.len_of_music_files)))
        self.title = title

        # renaming a file along with checking that the name does not contain prohibited characters 
        correct_title = title
        for char in correct_title:
            if char in self.prohibited_signs_in_file_name:
                correct_title: str = correct_title.replace(char, "_")
        file = pathlib.Path(str(old_file)).rename(f"{self.folder_path}\\{self.nr}. {correct_title}{file_format}")
        
        if file_format == '.flac':
            file = FLAC(file)
            self._tag_mp3_flac(file)
            self._add_img_flac(file, self.cover_file)
        elif file_format == '.mp3':
            self._tag_mp3_flac(EasyMP3(file))
            self._add_img_mp3(file, self.cover_file)


    def _tag_mp3_flac(self, file: FLAC | EasyMP3):
        file['artist'] = self.artist
        file['album'] = self.album_title
        file['title'] = self.title
        file['date'] = self.year
        file['genre'] = self.genre
        file['tracknumber'] = self.nr
        file.save()


    def _add_img_flac(self, file_path: FLAC, img_path):
        audio = file_path
        image_path = img_path
        with open(image_path, 'rb') as img:
            image_data = img.read()

        picture = Picture()
        picture.type = 3
        picture.mime = 'image/jpeg'
        picture.desc = 'Cover'
        picture.data = image_data

        audio.add_picture(picture)
        audio.save()


    def _add_img_mp3(self, file_path, img_path):
        audio = ID3(file_path)

        audio.delall('APIC')
        
        image_path = img_path
        audio.add(
            APIC(  
                encoding=3,
                mime='image/jpeg', 
                type=3,
                desc=u'Cover',
                data= open(image_path, 'rb').read()
        ))
        audio.save()