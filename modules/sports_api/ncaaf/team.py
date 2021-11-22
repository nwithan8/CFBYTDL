from datetime import datetime
from typing import List

from sportsipy.ncaaf.teams import Team as ApiTeam
from sportsipy.ncaaf.schedule import Schedule as ApiSchedule

from modules.sports_api.ncaaf.game import Game
from modules.sports_api.ncaaf.schedule import Schedule


class Team:
    def __init__(self, team: ApiTeam):
        self._team = team

    @property
    def name(self) -> str:
        return self._team.name

    @property
    def abbreviation(self) -> str:
        return self._team.abbreviation

    @property
    def most_recent_game(self) -> Game | None:
        return self.get_schedule().most_recent_game

    @property
    def first_game(self) -> Game | None:
        return self.get_schedule().first_game

    @property
    def last_game(self) -> Game | None:
        return self.get_schedule().last_game

    @property
    def all_games(self) -> List[Game]:
        return self.get_schedule().games

    def get_schedule(self, year: int = None) -> Schedule:
        return Schedule(ApiSchedule(abbreviation=self.abbreviation, year=year), team=self)

    def get_game_by_year_by_opponent(self, year: int, opponent_abbreviation: str) -> Game | None:
        return self.get_schedule(year=year).get_game_by_opponent(opponent_abbreviation=opponent_abbreviation)

    def get_game_by_year_by_number(self, year: int, game_number: int) -> Game | None:
        return self.get_schedule(year=year).get_game_by_number(game_number=game_number)

    def get_game_by_date(self, date: datetime) -> Game | None:
        return self.get_schedule().get_game_by_date(date=date)
