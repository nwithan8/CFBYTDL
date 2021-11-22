from modules.youtube_search import YouTubeSearcher
from modules.sports_api import SportsAPI, Sport
from modules.cli import CommandLine, Choice
from modules.video_processing.yt_downloader import Downloader

youtube = YouTubeSearcher()
sports_api = SportsAPI()
cli = CommandLine()


def main():
    cli.ask_question(prompt="Team 1:")
    cli.ask_question(prompt="Team 2:")
    cli.ask_question(prompt="Year:")

    team_1_name = cli.get_answer(question_number=1)
    team_2_name = cli.get_answer(question_number=2)
    year = cli.get_answer(question_number=3)

    team1 = sports_api.get_team(sport=Sport.NCAAF, team_name=team_1_name)
    team2 = sports_api.get_team(sport=Sport.NCAAF, team_name=team_2_name)

    game = sports_api.get_game_by_teams_and_year(sport=Sport.NCAAF, team_1=team1, team_2=team2, year=int(year))
    if not game:
        print("Could not locate game.")
        exit(0)

    game_search_term = f"Football {team1.name} {team2.name} {game.date.year}"
    youtube_results = youtube.search(game_search_term)

    if not youtube_results:
        print("Could not find any videos.")
        exit(0)

    cli.ask_choices(prompt="Select video:", choices=[Choice(name=f"{result.title} ({result.duration_stamp})", value=result) for result in youtube_results.results], most_number_selections=1)
    choice = cli.get_choices(question_number=4)[0]
    video = choice.value

    print(f"Downloading {video.link}")
    downloader = Downloader(video_id=video.id, title=game.title, year=game.year)
    downloader.download(youtube_link=video.link, include_captions=False)


if __name__ == "__main__":
    main()
