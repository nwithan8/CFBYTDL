from typing import List


class TeamPair:
    def __init__(self, teams: List[str], original_string: str):
        self.home = teams[2] if any(word in original_string for word in ['at ', '@']) else teams[0]
        self.away = teams[0] if self.home == teams[2] else teams[2]
