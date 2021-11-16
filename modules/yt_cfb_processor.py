from modules import tools, sportsapi
from modules.yt_downloader import Downloader
from modules.yt_cfb_parser import Parser
from modules.sportsapi import Sport, SportsAPI


def question(prompt: str):
    return input(f"{prompt}: ")


def yes_or_no(prompt: str) -> bool:
    answer = question(prompt=prompt)
    if answer.lower().startswith('y'):
        return True
    return False


class Processor:
    def __init__(self):
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
        _parser = Parser(youtube_url=self.youtube_link)
        teams = _parser.teams
        self.team_1 = teams.home
        self.team_2 = teams.away
        self.year = int(_parser.year)

    def download_video(self):
        _downloader = Downloader(title=self._get_game_title(), year=int(self.year) if self.year else None)
        _downloader.download(youtube_link=self.youtube_link, include_captions=self.embed_captions, include_metadata=self.embed_metadata)

    def _get_game_data(self):
        _sportapi = SportsAPI()
        _team_1 = _sportapi.get_team(sport=sportsapi.Sport.NCAAF, team_name=self.team_1)
        _team_2 = _sportapi.get_team(sport=sportsapi.Sport.NCAAF, team_name=self.team_2)
        if not _team_1 or not _team_2:
            print("Could not find one or both of the teams.")
            exit(1)
        matchup = _sportapi.get_game_by_teams_and_year(sport=sportsapi.Sport.NCAAF, team_1=_team_1, team_2=_team_2, year=self.year)
        if not matchup:
            print("Matchup does not exist!")
            exit(1)
        self.team_1_away = matchup.is_away
        self.date = matchup.datetime.strftime("%m-%d-%Y")
        self.episode = matchup.number

    def _get_game_title(self):
        title = f"{self.team_1} {'at' if self.team_1_away else 'vs.'} {self.team_2}"
        season_episode = f"s{self.year}e{self.episode}"
        return f"{season_episode} {title} ({self.date})".strip()


