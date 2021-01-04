from scrape import pfr
from scrape import guru
from scrape.base import close_driver
from scrape import scrape_player, scrape_game, scrape_stadium

from db import db

import learn
from config import current_season, current_week
from utility import combine_dicts

import json
import re
import datetime as dt


# Database


# Scraping
def scrape_players(season_week_pairs=None, guru_links_and_names=None):
    if season_week_pairs is None:
        season_week_pairs = {current_season: [current_week]}

    if guru_links_and_names is None:
        guru_links_and_names = guru.get_player_links_and_names(season_week_pairs)

    return {'players', [scrape_player(link, season_week_pairs, name) for link, name in guru_links_and_names.items()]}


def scrape_games(season_week_pairs=None, pfr_links=None):
    stadium_links = set()

    def get_pfr_links():
        def scrape_links():
            links = []

            for season, weeks in season_week_pairs.items():
                weeks_to_scrape = weeks if isinstance(weeks, list) else [weeks]

                def get_pfr_season_links():
                    season_links = []

                    for week in weeks_to_scrape:
                        season_links += pfr.get_game_links(week, season)

                    return season_links

                links += get_pfr_season_links()

            return links

        def format_links():
            return pfr_links if isinstance(pfr_links, list) else [pfr_links]

        return format_links() if pfr_links is not None else scrape_links()

    def get_game_data(links):
        games = {}

        for link in links:
            game = scrape_game(link)

            season = game.pop('season')
            week = game.pop('week')

            stadium_links.add(game['stadium_link'])

            def add_game_data():
                try:
                    season_data = games[season]

                    def add_game():
                        try:
                            week_data = season_data[week]
                            week_data.append(game)
                        except KeyError:
                            season_data[week] = [game]

                    add_game()

                except KeyError:
                    games[season] = {week: [game]}

            add_game_data()

        return games

    game_data = get_game_data(get_pfr_links())
    stadium_data = scrape_stadiums(stadium_links)

    return {'games': game_data,
            'stadiums': stadium_data}


def scrape_stadiums(pfr_links):
    return {'stadiums': [scrape_stadium(link) for link in pfr_links]}


def get_scraped_errors(filename):
    scraped_data = import_scrape(filename)
    errors = {}

    for scrape_type, data in scraped_data.items():
        errors[scrape_type] = [d for d in data if d.get('errors')]

    return errors


def print_scraped_errors(filename):
    errors = get_scraped_errors(filename)

    for key in errors.keys():
        print(key)

        for error in errors[key]:
            print(error)

        print()


def export_scrape(*args):
    filename = '%s_%s%s' % ('scrape', get_timestamp(), '.json')
    export_path = './scrape/data/' + filename

    with open(export_path, 'w') as file:
        json.dump(combine_dicts(args), file)


# Utilities
def split_filename_type(filename, file_type):
    def format_type():
        return '.%s' % file_type if not file_type.startswith('.') else file_type

    suffix = format_type()

    def split_suffix():
        return tuple(filter(None, re.split('(%s)' % suffix, filename)))

    return (filename, suffix) if not filename.endswith(suffix) else split_suffix()


def get_timestamp():
    return dt.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')


def import_scrape(filename):
    with open('./scrape/data/%s%s' % split_filename_type(filename, 'json')) as file:
        return json.load(file)


if __name__ == '__main__':
    timeframe = {2019: [i + 1 for i in range(11)]}

    game_data = scrape_games(timeframe)
    player_data = scrape_players(timeframe)
    close_driver()

    export_scrape(player_data, game_data)



