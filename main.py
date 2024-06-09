from flet import *


from pathlib import Path
import time
import json


import paths_settings
from automatic_tagging import AutomaticTagging



def main(page: Page):
    page.title = "mp3 & flac tagger"
    page.window_center()
    page.window_width, page.window_height = paths_settings.RES_X, paths_settings.RES_Y
    page.window_max_width, page.window_max_height = paths_settings.RES_X, paths_settings.RES_Y
    page.window_min_width, page.window_min_height = paths_settings.RES_X, paths_settings.RES_Y
    page.scroll = True


    def choose_file(e: FilePickerResultEvent):
        def close_dialog(event):
            dialog.open = False
            page.update()

        at = AutomaticTagging(str(Path(e.files[0].path)))

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

            dialog.content = Column(controls= [
                Text(value= f"{str(nr).zfill(len(str(at.len_of_music_files)))}/{at.len_of_music_files}. {title}"),
                Text(value= f"{paths_settings.PROGRESS}: {progress_proc}%"),
                ProgressBar(width= 400, value= round(progress_proc / 100, 2), color= 'amber'),
            ]) 

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
    )


app(target= main)