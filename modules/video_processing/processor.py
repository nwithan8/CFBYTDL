from modules.video_processing.yt_downloader import Downloader
from modules.video_processing.transcoder import Transcoder
from modules.video_processing.utils import _get_random_id


class VideoProcessor:
    def __init__(self, video_title: str, video_year: int = None):
        self._id = _get_random_id()
        self._title = video_title
        self._year = video_year
        self._downloader = Downloader(video_id=self._id, title=self._title, year=self._year)
        self._transcoder = Transcoder(temp_file_name=self._downloader.temp_file_name)

    def download(self, youtube_link: str, include_captions: bool = False, include_metadata: bool = False):
        self._downloader.download(youtube_link, include_captions)
        if include_metadata:
            self._transcoder.embed_metadata(video_title=self._title, video_year=self._year)

    def embed_metadata(self, title: str, year: int = None):
        self._transcoder.embed_metadata(video_title=title, video_year=year)

    def finalize_file(self):
        self._transcoder.rename_temp_file(self._title)