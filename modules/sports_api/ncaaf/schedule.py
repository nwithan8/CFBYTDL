from datetime import datetime
from typing import List

from sportsipy.ncaaf.schedule import Schedule as ApiSchedule

from modules.sports_api.ncaaf.game import Game

from modules.sports_api.utils import same_date


class Schedule:
    def __init__(self, schedule: ApiSchedule):
        self._schedule = schedule

    @property
    def games(self) -> List[Game]:
        games = []
        num = 1
        for game in self._schedule._games:
            games.append(Game(game, num))
            num += 1
        return games

    @property
    def last_game(self) -> Game | None:
        try:
            return self.games[-1]
        except IndexError:
            return None

    @property
    def first_game(self) -> Game | None:
        try:
            return self.games[0]
        except IndexError:
            return None

    @property
    def most_recent_game(self) -> Game | None:
        most_recent_game = None
        for game in self.games:
            if game.date <= datetime.now().date():
                most_recent_game = game
            else:
                break
        return most_recent_game

    def get_game_by_number(self, game_number: int) -> Game | None:
        try:
            return self.games[game_number - 1]
        except IndexError:
            return None

    def get_game_by_date(self, date: datetime) -> Game | None:
        """
        Find a game with the same month, day, and year as the given date.
        """
        for game in self.games:
            if same_date(game.datetime, date):
                return game
        return None

    def get_game_by_opponent(self, opponent_abbreviation: str) -> Game | None:
        """
        Find a game with the same opponent name as the given name.
        """
        opponent_abbreviation = opponent_abbreviation.lower()
        for game in self.games:
            if game.opponent_abbr.lower() == opponent_abbreviation:
                return game
        return None
