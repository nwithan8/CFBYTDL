import re
from typing import Union

from yt_dlp import YoutubeDL

from classes.sports.team_pair import TeamPair


class Parser:
    def __init__(self, youtube_url):
        self._link = youtube_url
        self._yt = YoutubeDL()
        self._info = None

    @property
    def info(self):
        if not self._info:
            self._info = self._yt.extract_info(self._link, download=False)
        return self._info

    @property
    def title(self):
        return self.info['title']

    @property
    def teams(self) -> Union[TeamPair, None]:
        title = self.title.lower()
        for word in ['full ', 'game ', 'ncaaf', 'week ']:
            title = title.replace(word, '')
        # Ex: NCAAF 2021 Week #11 - Purdue Boilermakers vs. Ohio State Buckeyes -> Purdue Boilermakers vs. Ohio State Buckeyes
        team_subtitle = re.search(r'(?:([a-z]{1}[a-z&]{1}[a-z]*\s)+)(at|@|vs\.?)\s?(?:([a-z]{1}[a-z&]{1}[a-z]*\s?)+)', title).group(0)
        if team_subtitle:
            teams = re.match(r'(.*)\s([aA]t|@|[Vv]s\.?)\s(.*\s?)', team_subtitle)
            if teams:
                return TeamPair([team for team in teams.groups()], team_subtitle)
            return None
        return None

    @property
    def year(self) -> str:
        # use regex to extract year from title
        return re.search(r'\d{4}', self.title).group(0)
