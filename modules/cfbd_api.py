from typing import List, Union

import cfbd
from classes import Matchup


class CFBDAPI:
    def __init__(self, api_key: str):
        config = cfbd.Configuration()
        config.api_key['Authorization'] = api_key
        config.api_key_prefix['Authorization'] = 'Bearer'
        self.client = cfbd.ApiClient(configuration=config)

    @property
    def _games_api(self) -> cfbd.GamesApi:
        return cfbd.GamesApi(self.client)

    @property
    def _teams_api(self):
        return cfbd.TeamsApi(self.client)

    def is_valid_team(self, team_name: str):
        return not not self._teams_api.get_roster(team=team_name)  # do results exist?

    def get_schedule(self, year: int, team_name: str, postseason: bool = False) -> List[cfbd.Game]:
        return self._games_api.get_games(year=year, team=team_name,
                                         season_type=('postseason' if postseason else 'regular'))

    def get_matchup(self, team_one: str, team_two: str, year: int) -> Union[Matchup, None]:
        schedule = self.get_schedule(year=year, team_name=team_one)
        week = 1
        for game in schedule:
            if team_two in [game.home_team, game.away_team]:
                return Matchup(game=game, team=team_one, week=week)
            week += 1
        return None
