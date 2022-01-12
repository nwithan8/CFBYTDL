from yt_dlp import YoutubeDL


class Downloader:
    def __init__(self, video_id: str, title: str, year: int = None):
        self._id = video_id
        self._title = title
        self._year = year

    @property
    def temp_file_name(self):
        return f"{self._id}.mp4"

    def download(self, youtube_link: str, include_captions: bool = False):
        print(f"Downloading YouTube video as {self._title}...")
        opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
            'outtmpl': f'{self.temp_file_name}'
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
