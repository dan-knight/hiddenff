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


def scrape_games_and_export(weeks=current_week, season=current_season):
    def get_pfr_links(weeks_to_scrape):
        links = []
        try:
            for week in weeks_to_scrape:
                links += pfr.get_game_links(week, season)
        except TypeError:
            links = get_pfr_links([weeks_to_scrape])

        return links

    pfr_links = get_pfr_links(weeks)

    data = {
        'games': [scrape_game(link) for link in pfr_links]
    }

    export_scrape('game-scrape', data)


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

    def get_most_recent_name():
        name = pfr_data['names'][-1]['name']
        try:
            name = wiki.errors['stadium_names'][name]
        except KeyError:
            pass

        return name

    most_recent_name = get_most_recent_name()
    wiki_link = wiki.get_stadium_link(most_recent_name)

    wiki_data = {}

    if wiki_link:
        wiki_data = wiki.scrape_stadium(wiki_link)
        links.add(wiki_data['url'])
        errors.update(wiki_data['errors'])
    else:
        errors.add('wiki_link')

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
    #guru_list_url = 'http://rotoguru1.com/cgi-bin/fstats.cgi?pos=0&sort=1&game=p&colA=0&daypt=0&xavg=0&inact=0&maxprc=99999&outcsv=0'

    # players = import_scrape('player-scrape_2020-05-01_18-03-11.json')['players']
    # games = import_scrape('game-scrape_2020-05-15_19-41-29.json')['games']
    # teams = import_scrape('teams')
    # stadiums = import_scrape('stadium-scrape_2020-05-12_10-15-21.json')['stadiums']
    #
    # # db.reset_tables()
    #
    # db.update_from_scraped({'teams': teams,
    #                         'games': games,
    #                         'players': players,
    #                         'stadiums': stadiums})
    #
    # db.calculate_stats()

    # close_driver()
    # db.session.commit()

    scrape_players_and_export(dict.fromkeys(range(2014, 2019 + 1), range(1, 17 + 1)))
    close_driver()

    # for player in import_scrape('')['players']:
    #     if player['errors']:
    #         print(player)


