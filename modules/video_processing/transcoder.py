import subprocess

from modules.video_processing.utils import _get_random_id


def _move_file(src_file: str, dest_file: str):
    subprocess.call(f'mv {src_file} {dest_file}', shell=True)


class Transcoder:
    def __init__(self, temp_file_name: str):
        self._temp_file_name = temp_file_name

    def embed_metadata(self, video_title: str, video_year: int = None):
        dest_file = f'{_get_random_id()}.mp4'
        command = f'ffmpeg -i {self._temp_file_name} -metadata title="{video_title}"'
        if video_year:
            command += f' -metadata year="{video_year}"'
        command += f' "{dest_file}"'
        subprocess.call(command, shell=True)
        _move_file(dest_file, self._temp_file_name)

    def rename_temp_file(self, video_title: str):
        _move_file(self._temp_file_name, f'{video_title}.mp4')
