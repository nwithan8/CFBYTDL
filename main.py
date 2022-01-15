import argparse
import datetime

import modules.cli.cli
from modules.cli import CommandLine, Choice, ask_yes_or_no_question
from modules.sports_api import SportsAPI, Sport, create_game_title
from modules.video_processing import VideoProcessor
from modules.youtube_search import YouTubeSearcher

youtube = YouTubeSearcher()
sports_api = SportsAPI()
cli = CommandLine()

parser = argparse.ArgumentParser(description='Download sports games from YouTube')
parser.add_argument('-s', '--sport', type=str, help='Sport to search for', required=True)
parser.add_argument('--manual', action='store_true', help='Manually provide link and data')


def main_manual(sport: Sport):
    link = cli.ask_question(prompt="Link:").answer
    team_1_name = cli.ask_question(prompt="Team 1:").answer
    team_1_home = cli.ask_question(prompt="Team 1 Home?", y_n=True).answer
    team_2_name = cli.ask_question(prompt="Team 2:").answer
    season = cli.ask_question(prompt="Season:").answer
    game_number = cli.ask_question(prompt="Game Number:").answer

    year = cli.ask_question(prompt="Year:", default_answer=season).answer
    month = cli.ask_question(prompt="Month:").answer
    day = cli.ask_question(prompt="Day:").answer

    game_date = datetime.datetime(year=int(year), month=int(month), day=int(day))
    title = create_game_title(sport=sport, year=int(season), game_number=int(game_number), team_1_name=team_1_name,
                              team_2_name=team_2_name, team_1_home=bool(team_1_home), game_date=game_date)

    if ask_yes_or_no_question(prompt="Special game?"):
        special_game_name = cli.ask_question(prompt="Special game name:").answer
        title = f"{title} ({special_game_name})"

    download(link=link, title=title, year=int(year))


def main_automatic(sport: Sport):
    team_1_name = cli.ask_question(prompt="Team 1:").answer
    team_2_name = cli.ask_question(prompt="Team 2:").answer
    year = cli.ask_question(prompt="Year:").answer

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

    video_choices = cli.ask_choices(prompt="Select video:",
                                    choices=[Choice(name=f"{result.title} ({result.duration_stamp})", value=result)
                                             for result
                                             in
                                             youtube_results.results], most_number_selections=1)
    choice = video_choices.selected_choices[0]
    video = choice.value

    download(link=video.link, title=video.title, year=video.year)


def download(link: str, title: str, year: int):
    embed_captions = ask_yes_or_no_question(prompt="Embed captions?")
    embed_metadata = ask_yes_or_no_question(prompt="Embed metadata?")

    print(f"Downloading {link}")
    processor = VideoProcessor(video_title=title, video_year=year)
    processor.download(youtube_link=link, include_captions=embed_captions, include_metadata=embed_metadata)


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
