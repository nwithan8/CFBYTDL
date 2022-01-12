from datetime import datetime

from sportsipy import constants
from sportsipy.ncaaf.schedule import Game as ApiGame


class Game:
    def __init__(self, game: ApiGame, number: int, team):
        self.number = number
        self._game = game
        self._team = team

    @property
    def opponent_name(self) -> str:
        return self._game.opponent_name

    @property
    def opponent_abbr(self) -> str:
        return self._game.opponent_abbr

    @property
    def own_score(self) -> int:
        return self._game.points_for

    @property
    def opponent_score(self) -> int:
        return self._game.points_against

    @property
    def won(self) -> bool:
        return self.own_score > self.opponent_score

    @property
    def lost(self) -> bool:
        return self.own_score < self.opponent_score

    @property
    def tied(self) -> bool:
        return self.own_score == self.opponent_score

    @property
    def datetime(self) -> datetime:
        return self._game.datetime

    @property
    def date(self) -> datetime:
        return self.datetime.date()

    @property
    def year(self) -> int:
        return self.date.year

    @property
    def date_string(self) -> str:
        return self._game.date

    @property
    def time_string(self) -> str:
        return self._game.time

    @property
    def location(self) -> str:
        return self._game.location

    @property
    def is_home(self) -> bool:
        return self.location == constants.HOME

    @property
    def is_away(self) -> bool:
        return self.location == constants.AWAY

    @property
    def is_neutral(self) -> bool:
        return self.location == constants.NEUTRAL

    @property
    def title(self) -> str:
        return Game.create_game_title(year=self.year, game_number=self.number, team_1_name=self._team.name,
                                      team_2_name=self.opponent_name, team_1_home=self.is_home, game_date=self.date)

    @classmethod
    def create_game_title(cls, year: int, game_number: int, team_1_name: str,
                          team_2_name: str, team_1_home: bool, game_date: datetime) -> str:
        return f"s{year}e{game_number:02d} {team_1_name} " \
               f"{'vs.' if team_1_home else 'at'} {team_2_name} ({game_date.strftime('%Y-%m-%d')})"
