from modules import tools
from modules.cfbd_api import CFBDAPI
from modules.yt_downloader import Downloader
from modules.yt_cfb_parser import Parser


def question(prompt: str):
    return input(f"{prompt}: ")


def yes_or_no(prompt: str) -> bool:
    answer = question(prompt=prompt)
    if answer.lower().startswith('y'):
        return True
    return False


class Processor:
    def __init__(self, cfbd_api_key: str):
        self._cfbd_api = CFBDAPI(api_key=cfbd_api_key)
        self._downloader = None
        self._parser = None

        self.youtube_link = None
        self.team_1 = None
        self.team_2 = None
        self.team_1_away = False
        self.year = None
        self.episode = None
        self.date = None
        self.embed_metadata = False
        self.embed_captions = False

    def run(self):
        self.ask_questions()
        # self.parse_link()
        self._get_game_data()
        self.download_video()

    def ask_questions(self):
        self.youtube_link = question("YouTube link")
        self.team_1 = question("Team 1")
        self.team_2 = question("Team 2")
        self.year = int(question("Year"))
        self.embed_captions = yes_or_no("Embed captions?")
        self.embed_metadata = yes_or_no("Embed metadata?")

    def parse_link(self):
        self._parser = Parser(youtube_url=self.youtube_link)
        teams = self._parser.teams
        self.team_1 = teams.home
        self.team_2 = teams.away
        self.year = int(self._parser.year)

    def download_video(self):
        self._downloader = Downloader(title=self._get_game_title(), year=int(self.year) if self.year else None)
        self._downloader.download(youtube_link=self.youtube_link, include_captions=self.embed_captions, include_metadata=self.embed_metadata)

    def _get_game_data(self):
        matchup = self._cfbd_api.get_matchup(team_one=self.team_1, team_two=self.team_2, year=self.year)
        if not matchup:
            print("Matchup does not exist!")
            exit(1)
        self.team_1_away = (matchup.game.away_team == self.team_1)
        self.date = tools.convert_string_date_to_another_format(matchup.game.start_date, "%Y-%m-%dT%H:%M:%S.000Z", "%m-%d-%Y")
        self.episode = matchup.week

    def _get_game_title(self):
        title = f"{self.team_1} {'at' if self.team_1_away else 'vs.'} {self.team_2}"
        season_episode = f"s{self.year}e{self.episode}"
        return f"{season_episode} {title} ({self.date})".strip()


