from __future__ import annotations

from datetime import datetime
from typing import Type

from modules.sports_api import ncaaf
from modules.sports_api.enums import Sport


class SportsAPI:
    def __init__(self):
        self._ncaaf = ncaaf.API()

    def _get_sub_api(self, sport: Sport):
        if sport == Sport.COLLEGE_FOOTBALL:
            return self._ncaaf

    def get_team(self, sport: Sport, team_name: str) -> ncaaf.Team | None:
        try:
            return self._get_sub_api(sport).get_team(team_name=team_name)
        except KeyError:
            return None

    def get_team_schedule(self, sport: Sport, team: ncaaf.Team = None, team_abbreviation: str = None,
                          year: int = None) -> ncaaf.Schedule | None:
        if not team and not team_abbreviation:
            return None
        try:
            return self._get_sub_api(sport).get_team_schedule(team_abbreviation=team_abbreviation, team=team, year=year)
        except KeyError:
            return None

    def get_game_by_teams_and_year(self, sport: Sport, team_1: ncaaf.Team, team_2: ncaaf.Team,
                                   year: int) -> ncaaf.Game | None:
        try:
            return self._get_sub_api(sport).get_game_by_teams_and_year(team_1=team_1, team_2=team_2, year=year)
        except KeyError:
            return None


def _get_game_class(sport: Sport) -> Type[ncaaf.Game]:
    if sport == Sport.COLLEGE_FOOTBALL:
        return ncaaf.Game


def create_game_title(sport: Sport, year: int, game_number: int, team_1_name: str,
                      team_2_name: str, team_1_home: bool, game_date: datetime) -> str:
    game_class = _get_game_class(sport)
    return game_class.create_game_title(year=year, game_number=game_number, team_1_name=team_1_name,
                                        team_2_name=team_2_name, team_1_home=team_1_home, game_date=game_date)
