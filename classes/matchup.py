from cfbd import Game


class Matchup:
    def __init__(self, game: Game, team: str, week: int):
        self.game = game
        self.team = team
        self.week = week
