from scrape import pfr
from scrape import guru
from scrape import wiki
from scrape.base import close_driver

from db import db

import learn
from config import current_season, current_week

import json
import re
import datetime as dt


# Database


# Scraping
def scrape_players_and_export(season_week_pairs=None):
    if season_week_pairs is None:
        season_week_pairs = {current_season: [current_week]}

    guru_links_and_names = guru.get_player_links_and_names(season_week_pairs)

    data = {
        'players': [scrape_player(link, season_week_pairs, name) for link, name in guru_links_and_names.items()]
    }

    export_scrape('player-scrape', data)


def scrape_player(guru_link, season_week_pairs, name=None):
    guru_data = guru.scrape_player(guru_link, name)

    def get_pfr_link():
        link = pfr.get_player_link(guru_data['first'], guru_data['last'], list(season_week_pairs))

        if not link:
            link = pfr.prepend_link(pfr.errors['player_links'].get(guru_link))

        return link

    pfr_link = get_pfr_link()

    def get_pfr_data():
        return pfr.scrape_player(pfr_link, season_week_pairs) if pfr_link else {'url': pfr_link,
                                                                                'errors': {'pfr_link'}}

    pfr_data = get_pfr_data()

    def combine_scraped_data():
        scraped_data = {
            'links': [guru_data['url'], pfr_link],
            'first': guru_data['first'],
            'last': guru_data['last'],
            'position': guru_data['position'],
            'team': pfr_data.get('team'),
            'birthday': pfr_data.get('birthday'),
            'games': pfr_data.get('games'),
        }

        def check_data_errors():
            full_name = '%s %s' % (scraped_data['first'], scraped_data['last'])

            def update_from_errors(errors):
                scraped_data.update(errors['data'].get(full_name, {}))

            update_from_errors(pfr.errors)

        check_data_errors()

        def check_errors():
            def combine_errors():
                all_errors = guru_data['errors']
                all_errors.update(pfr_data['errors'])
                return all_errors

            errors = combine_errors()

            if errors:
                wiki_links = wiki.get_player_links(scraped_data['first'], scraped_data['last'], scraped_data['position'])
                for link in wiki_links:
                    wiki_data = wiki.scrape_player(link)

                    if wiki_data['birthday'] == scraped_data['birthday']:
                        def update_scraped_data():
                            for error in errors.copy():
                                if wiki_data.get(error):
                                    scraped_data.update({error: wiki_data[error]})
                                    errors.remove(error)

                        update_scraped_data()
                        break

            scraped_data.update({'errors': list(errors)})

        check_errors()
        return scraped_data

    return combine_scraped_data()


def scrape_games_and_export(season_week_pairs=None):
    if season_week_pairs is None:
        season_week_pairs = {current_season: [current_week]}

    def get_pfr_links():
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

    def scrape_games(links):
        games = {}

        for link in links:
            game = scrape_game(link)

            season = game.pop('season')
            week = game.pop('week')

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

    export_scrape('game-scrape', {'games': scrape_games(get_pfr_links())})


def scrape_game(pfr_link):
    pfr_game = pfr.scrape_game(pfr_link)
    pfr_game['errors'] = list(pfr_game['errors'])

    return pfr_game


def scrape_stadiums_and_export(pfr_links):
    data = {'stadiums': [scrape_stadium(link) for link in pfr_links]}

    export_scrape('stadium-scrape', data)


def scrape_stadium(pfr_link):
    pfr_data = pfr.scrape_stadium(pfr_link)

    links = {pfr_data['url']}
    errors = pfr_data['errors'].copy()

    def get_wiki_link():
        def get_most_recent_name():
            name = pfr_data['names'][-1]['name']

            try:
                name = wiki.errors['stadium_names'][name]
            except KeyError:
                pass

            return name

        error_link = wiki.errors['stadium_links'].get(pfr_link)
        return error_link if error_link else wiki.get_stadium_link(get_most_recent_name())

    wiki_link = get_wiki_link()
    wiki_data = {}

    if wiki_link:
        wiki_data = wiki.scrape_stadium(wiki_link)
        links.add(wiki_data['url'])
        errors.update(wiki_data['errors'])
    else:
        errors.add('wiki_link')

    def check_errors():
        def check_teams():
            if 'teams' in errors:
                try:
                    wiki_data.update({'teams': wiki.errors['stadium_teams'][pfr_link]})
                    errors.remove('teams')
                except KeyError:
                    pass

        if errors:
            check_teams()

    check_errors()

    return {'links': list(links),
            'names': pfr_data.get('names'),
            'surfaces': pfr_data.get('surfaces'),
            'teams': wiki_data.get('teams'),
            'errors': list(errors)}


def get_scraped_errors(filename):
    data = import_scrape(filename)
    errors = {}

    for key in data.keys():
        errors[key] = [x for x in data[key] if x.get('errors')]

    return errors


def print_scraped_errors(filename):
    errors = get_scraped_errors(filename)

    for key in errors.keys():
        print(key)

        for error in errors[key]:
            print(error)

        print()


def export_scrape(filename, data):
    name, suffix = split_filename_type(filename, 'json')
    filename = '%s_%s%s' % (name, get_timestamp(), suffix)
    export_path = './scrape/data/' + filename

    with open(export_path, 'w') as file:
        json.dump(data, file)


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


def get_scraped_stadium_links_from_games(filename):
    games = import_scrape(filename)['games']
    links = set()

    for game in games:
        links.add(game['stadium_link'])

    return links


if __name__ == '__main__':
    scrape_games_and_export({2019: [i + 1 for i in range(11)]})
    close_driver()
