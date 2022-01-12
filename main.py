import argparse
import datetime

import modules.cli.cli
from modules.cli import CommandLine, Choice
from modules.sports_api import SportsAPI, Sport, create_game_title
from modules.video_processing.yt_downloader import Downloader
from modules.youtube_search import YouTubeSearcher

youtube = YouTubeSearcher()
sports_api = SportsAPI()
cli = CommandLine()

parser = argparse.ArgumentParser(description='Download sports games from YouTube')
parser.add_argument('-s', '--sport', type=str, help='Sport to search for', required=True)
parser.add_argument('--manual', action='store_true', help='Manually provide link and data')


def main_manual(sport: Sport):
    cli.ask_question(prompt="Link:")
    cli.ask_question(prompt="Team 1:")
    cli.ask_question(prompt="Team 1 Home?", y_n=True)
    cli.ask_question(prompt="Team 2:")
    cli.ask_question(prompt="Game Number:")
    cli.ask_question(prompt="Year:")
    cli.ask_question(prompt="Month:")
    cli.ask_question(prompt="Day:")

    link = cli.get_answer(question_number=1)
    team_1_name = cli.get_answer(question_number=2)
    team_1_home = cli.get_answer(question_number=3)
    team_2_name = cli.get_answer(question_number=4)
    game_number = cli.get_answer(question_number=5)
    year = cli.get_answer(question_number=6)
    month = cli.get_answer(question_number=7)
    day = cli.get_answer(question_number=8)

    game_date = datetime.datetime(year=int(year), month=int(month), day=int(day))
    title = create_game_title(sport=sport, year=int(year), game_number=int(game_number), team_1_name=team_1_name,
                              team_2_name=team_2_name, team_1_home=bool(team_1_home), game_date=game_date)

    if modules.cli.cli.ask_yes_or_no_question(prompt="Special game?"):
        cli.ask_question(prompt="Special game name:")
        special_game_name = cli.get_answer(question_number=9)
        title = f"{title} ({special_game_name})"

    print(f"Downloading {link}")
    downloader = Downloader(video_id=link, title=title, year=int(year))
    downloader.download(youtube_link=link, include_captions=False)


def main_automatic(sport: Sport):
    cli.ask_question(prompt="Team 1:")
    cli.ask_question(prompt="Team 2:")
    cli.ask_question(prompt="Year:")

    team_1_name = cli.get_answer(question_number=1)
    team_2_name = cli.get_answer(question_number=2)
    year = cli.get_answer(question_number=3)

    team1 = sports_api.get_team(sport=sport, team_name=team_1_name)
    team2 = sports_api.get_team(sport=sport, team_name=team_2_name)

    game = sports_api.get_game_by_teams_and_year(sport=sport, team_1=team1, team_2=team2, year=int(year))
    if not game:
        print("Could not locate game.")
        exit(0)

    game_search_term = f"Football {team1.name} {team2.name} {game.date.year}"
    youtube_results = youtube.search(game_search_term)

    if not youtube_results:
        print("Could not find any videos.")
        exit(0)

    cli.ask_choices(prompt="Select video:",
                    choices=[Choice(name=f"{result.title} ({result.duration_stamp})", value=result) for result in
                             youtube_results.results], most_number_selections=1)
    choice = cli.get_choices(question_number=4)[0]
    video = choice.value

    print(f"Downloading {video.link}")
    downloader = Downloader(video_id=video.id, title=game.title, year=game.year)
    downloader.download(youtube_link=video.link, include_captions=False)


if __name__ == "__main__":
    args = parser.parse_args()
    _sport = Sport.get_sport_enum(args.sport)
    if not _sport:
        print('Invalid sport')
        exit(1)
    else:
        print("Using sport: " + _sport.name)

    if args.manual:
        main_manual(_sport)
    else:
        main_automatic(_sport)
