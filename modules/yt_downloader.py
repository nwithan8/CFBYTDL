import subprocess
import uuid

from yt_dlp import YoutubeDL


def _get_random_id() -> str:
    return uuid.uuid4().hex


class Downloader:
    def __init__(self, title: str, year: int = None):
        self._title = title
        self._year = year
        self._id = _get_random_id()

    @property
    def _temp_file_name(self):
        return f"{self._id}.mp4"

    def download(self, youtube_link: str, include_captions: bool = False, include_metadata: bool = False):
        print(f"Downloading YouTube video as {self._title}...")
        self._download_youtube_video(youtube_link=youtube_link, include_captions=include_captions)
        if include_metadata:
            self._embed_metadata()
        self._rename_temp_file()

    def _download_youtube_video(self, youtube_link: str, include_captions: bool = False):
        opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
            'outtmpl': f'{self._temp_file_name}'
        }
        if include_captions:
            extra_opts = {
                'subtitleslangs': ['en'],
                'subtitlesformat': 'srt',
                'writeautomaticsub': True,
                'embedsubtitles': True,
            }
            opts.update(extra_opts)
        with YoutubeDL(opts) as ydl:
            ydl.download([youtube_link])

    def _embed_metadata(self):
        command = f'ffmpeg -i temp.mp4 -metadata title="{self._title}"'
        if self._year:
            command += f' -metadata year="{self._year}"'
        command += f' "{self._temp_file_name}"'
        subprocess.call(command, shell=True)

    def _rename_temp_file(self):
        subprocess.call(f'mv {self._temp_file_name} "{self._title}.mp4"', shell=True)
