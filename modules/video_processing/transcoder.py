import subprocess


class Transcoder:
    def __init__(self, temp_file_name: str):
        self._temp_file_name = temp_file_name

    def embed_metadata(self, video_title: str, video_year: int = None):
        command = f'ffmpeg -i {self._temp_file_name} -metadata title="{video_title}"'
        if video_year:
            command += f' -metadata year="{video_year}"'
        command += f' "{self._temp_file_name}"'
        subprocess.call(command, shell=True)

    def rename_temp_file(self, video_title: str):
        subprocess.call(f'mv {self._temp_file_name} "{video_title}.mp4"', shell=True)
