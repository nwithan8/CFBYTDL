from enum import Enum


class Sport(Enum):
    SOCCER = 1
    COLLEGE_FOOTBALL = 2
    PRO_FOOTBALL = 3
    COLLEGE_BASKETBALL = 4
    PRO_BASKETBALL = 5
    COLLEGE_BASEBALL = 6
    PRO_BASEBALL = 7
    HOCKEY = 8

    @staticmethod
    def get_sport_enum(sport: str) -> 'Sport':
        sport = sport.lower().strip()
        if sport in ["futbol", "soccer"]:
            return Sport.SOCCER
        elif sport in ["ncaaf", "cfb", "college football"]:
            return Sport.COLLEGE_FOOTBALL
        elif sport in ["nfl", "football"]:
            return Sport.PRO_FOOTBALL
        elif sport in ["ncaab", "cfb", "college basketball"]:
            return Sport.COLLEGE_BASKETBALL
        elif sport in ["nba", "basketball"]:
            return Sport.PRO_BASKETBALL
        elif sport in ["college baseball"]:
            return Sport.COLLEGE_BASEBALL
        elif sport in ["mlb", "baseball"]:
            return Sport.PRO_BASEBALL
        elif sport == ["nhl", "hockey"]:
            return Sport.HOCKEY
        else:
            return None
