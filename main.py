from flet import *

from pathlib import Path
import time

import paths_settings
from automatic_tagging import AutomaticTagging



def main(page: Page):
    page.title = "mp3 & flac tagger"
    page.window_center()
    page.window_width, page.window_height = paths_settings.RES_X, paths_settings.RES_Y
    page.window_max_width, page.window_max_height = paths_settings.RES_X, paths_settings.RES_Y
    page.window_min_width, page.window_min_height = paths_settings.RES_X, paths_settings.RES_Y
    page.scroll = True


    def choose_file(file_picker: FilePickerResultEvent):
        def close_dialog(event: ControlEvent):
            dialog.open = False
            page.update()
        
        def close_dialog_not_music_files(event: ControlEvent):
            dialog_not_music_files.open = False
            page.update()
        
        def close_dialog_files_not_equal(event: ControlEvent):
            dialog_files_not_equal_titles.open = False
            page.update()
        
        def close_dialog_cover_is_none(event: ControlEvent):
            dialog_cover_is_none.open = False
            page.update()

        at = AutomaticTagging(str(Path(file_picker.files[0].path)))
        

        if at.len_of_music_files == 0:
            dialog_not_music_files = AlertDialog(
                title= Text(value= paths_settings.NOT_MUSIC_FILES_TITLE, size= 20),
                modal= True,
                content= Text(value= paths_settings.NOT_MUSIC_FILES, size= 15),
                open = True,
                actions= [ElevatedButton(
                    text= Text(value= paths_settings.CLOSE).value,
                    on_click= close_dialog_not_music_files
                )]
            )
            page.dialog = dialog_not_music_files
            page.update()

        elif len(at.music_files) != len(at.titles):
            dialog_files_not_equal_titles = AlertDialog(
                title= Text(value= paths_settings.NUM_OF_MUSIC_FILES_AND_TITLE_NOT_EQUAL_TITLE, size= 20),
                modal= True,
                content= Text(value= paths_settings.NUM_OF_MUSIC_FILES_AND_TITLE_NOT_EQUAL, size= 15),
                open = True,
                actions= [ElevatedButton(
                    text= Text(value= paths_settings.CLOSE).value,
                    on_click= close_dialog_files_not_equal
                )]
            )
            page.dialog = dialog_files_not_equal_titles
            page.update()
        
        elif at.cover_file is None:
            dialog_cover_is_none = AlertDialog(
                title= Text(value= paths_settings.NOT_COVER_TITLE, size= 20),
                modal= True,
                content= Text(value= paths_settings.NOT_COVER, size= 15),
                open = True,
                actions= [ElevatedButton(
                    text= Text(value= paths_settings.CLOSE).value,
                    on_click= close_dialog_cover_is_none
                )]
            )
            page.dialog = dialog_cover_is_none
            page.update()

        else:
            start = time.time()

            dialog = AlertDialog(
                title= Text(value= paths_settings.TAGGING, size= 15),
                modal= True,
            )
            page.dialog = dialog
            dialog.open = True
            page.update()
            
            for nr, (file, title, file_format) in enumerate(zip(at.music_files, at.titles, at.music_files_formats), start= 1):
                dialog.clean()
                
                progress_proc = round(100 * (int(nr) / int(at.len_of_music_files)), 2)

                dialog.content = Column(
                    height= 50,
                    controls= [
                        Text(value= f"{str(nr).zfill(len(str(at.len_of_music_files)))}/{at.len_of_music_files}. {title}"),
                        Text(value= f"{paths_settings.PROGRESS}: {progress_proc}%"),
                        ProgressBar(width= 400, value= round(progress_proc / 100, 2), color= 'amber'),
                    ]
                ) 

                dialog.update()
                
                at.tag_music_file(nr, file, title, file_format)

            end = time.time()
            time_delta = end - start

            dialog.clean()
            dialog.content = Text(
                value= paths_settings.TIME_DELTA.format(time_delta)
            )
            dialog.actions = [
                ElevatedButton(
                    text= Text(value= paths_settings.CLOSE).value,
                    on_click= close_dialog
                )
            ]
            dialog.update()
    

    def change_language(event: ControlEvent):
        paths_settings.change_language(event.control.text)
        page.window_close()


    pick_file = FilePicker(on_result= choose_file)
    page.overlay.append(pick_file)

    page.add(
        Container(
            alignment= alignment.center, 
            content= Text(
                value= paths_settings.CHANGE_LANGUAGE, 
                text_align= TextAlign.CENTER,
                selectable= False,
                size= 25,
            ),
        ),

        ResponsiveRow(
            controls= [
                Container(
                    col= 3,
                    content= ElevatedButton(
                        text= lang, 
                        on_click= change_language,
                        bgcolor= colors.RED,
                        color= colors.BLACK,
                    ),  
                ) for lang in paths_settings.LANGUAGES
            ],
        ),

        Container(
            alignment= alignment.center, 
            margin= Margin(0, 20, 0, 0), 
            content= ElevatedButton(
                text= Text(value= paths_settings.CHOOSE_FILE).value,
                on_click= lambda _: pick_file.pick_files(allowed_extensions= ["txt"],),
                icon= icons.UPLOAD_FILE,
                height= 40,
                width= 0.9 * paths_settings.RES_X,
            ),
        ),

        Container(
            alignment= alignment.center,
            content= ElevatedButton(
                text= Text(value= paths_settings.SOURCE_CODE).value,
                icon= icons.OPEN_IN_BROWSER,
                url= "https://github.com/skrzypa/Mp3_Flac_tag_editor",
                height= 40,
                width= 0.9 * paths_settings.RES_X,
            ),
        ),

        Container(
            alignment= alignment.center_left,
            border= border.all(),
            padding= padding.all(10),
            margin= margin.all(0),
            bgcolor= colors.BLACK,
            content= Text(
                value= f"{paths_settings.FOLDER_CONTAIN}\n\n1. Plik (File): .txt\n2. Plik (File): .jpg, .jpeg lub (or) .png\n3. Pliki (Files): .mp3 i / lub (and / or) .flac", 
                size= 15,
                selectable= True,
            ),
        ),

        Container(
            alignment= alignment.center_left,
            border= border.all(),
            padding= padding.all(10),
            margin= margin.all(0),
            bgcolor= colors.BLACK,
            content= Text(
                value= f"{paths_settings.TXT_CONTAIN}\n\nNazwę artysty (Artist name)\nNazwę albumu (Album name)\nRok wydania (Release year)\nGatunek (Music genre)\nTytuł 1 (Title 1)\nTytuł 2 (Title 2)\nTytuł 3 (Title 3)\n...\nTytuł n (Title n)", 
                size= 15,
                selectable= True,
            ),
        ),
    )


app(target= main)