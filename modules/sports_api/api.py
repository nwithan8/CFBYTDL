from __future__ import annotations

from modules.sports_api import ncaaf
from modules.sports_api.enums import Sport


class SportsAPI:
    def __init__(self):
        self._ncaaf = ncaaf.API()

    def _get_sub_api(self, sport: Sport):
        if sport in [Sport.NCAAF, Sport.COLLEGE_FOOTBALL]:
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
