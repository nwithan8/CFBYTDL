from __future__ import annotations

from datetime import datetime

from sportsipy.ncaaf.teams import Team as ApiTeam, _retrieve_all_teams
from sportsipy.ncaaf.schedule import Schedule as ApiSchedule

from modules.sports_api.ncaaf.game import Game
from modules.sports_api.ncaaf.team import Team
from modules.sports_api.ncaaf.schedule import Schedule


class API:
    teams_cache = {}

    def get_teams(self, year: int = None) -> list:
        if year is None:
            year = str(datetime.now().year)
        if year in self.teams_cache.keys():
            return self.teams_cache[year]
        teams_data, _ = _retrieve_all_teams(year=year, season_page=None, offensive_stats=None, defensive_stats=None)
        teams = [Team(ApiTeam(team_data=team['data'])) for team in teams_data.values()]
        self.teams_cache[year] = teams
        return teams

    def get_team(self, team_name: str, year: int = None) -> Team | None:
        for team in self.get_teams(year=year):
            if team.name == team_name:
                return team
        return None

    def get_team_schedule(self, team: Team = None, team_abbreviation: str = None, year: int = None) -> Schedule:
        return Schedule(ApiSchedule(abbreviation=team.abbreviation if team else team_abbreviation, year=year), team=team)

    def get_game_by_teams_and_year(self, team_1: Team, team_2: Team, year: int) -> Game:
        return team_1.get_game_by_year_by_opponent(year=year, opponent_abbreviation=team_2.abbreviation)
