from scrape import pfr
from scrape import guru
from scrape import wiki
from scrape.base import driver

from db import db

import learn
from config import current_year, current_week

import json
import re
from datetime import datetime


# Database


# Scraping
def scrape_players_and_export(guru_list_link):
    data = {
        'players': [scrape_player(link) for link in guru.PlayerListScraper(guru_list_link).get_player_links()]
    }

    export_path = export_scrape('player-scrape', data)
    print_scraped_errors(export_path)


def scrape_player(guru_link):
    guru_data = guru.scrape_player(guru_link)

    pfr_link = pfr_player_list.get_player_link(guru_data['first'], guru_data['last'])
    pfr_data = pfr.scrape_player(pfr_link, weeks=range(1, 18))

    def combine_scraped_data():
        scraped_data = {
            'links': [guru_data['url'], pfr_data['url']],
            'first': guru_data['first'],
            'last': guru_data['last'],
            'position': guru_data['position'],
            'team': pfr_data['team'],
            'birth_year': pfr_data['birth_year'],
            'birth_month': pfr_data['birth_month'],
            'birth_day': pfr_data['birth_day'],
            'games': pfr_data['games'],
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

                    def is_same_birthday():
                        return wiki_data['birth_year'] == scraped_data['birth_year'] and \
                               wiki_data['birth_month'] == scraped_data['birth_month'] and \
                               wiki_data['birth_day'] == scraped_data['birth_day']

                    if is_same_birthday():
                        def update_scraped_data():
                            for error in errors.copy():
                                if wiki_data[error]:
                                    scraped_data.update({error: wiki_data[error]})
                                    errors.remove(error)

                        update_scraped_data()
                        break

            scraped_data.update({'errors': list(errors)})

        check_errors()
        return scraped_data

    return combine_scraped_data()


def scrape_games_and_export():
    def get_pfr_links():
        links = []

        for week in range(1, current_week + 1):
            links += pfr_game_list.get_week_links(week)

        return links

    pfr_links = get_pfr_links()

    data = {
        'games': [scrape_game(link) for link in pfr_links]
    }

    export_path = export_scrape('game-scrape', data)
    print_scraped_errors(export_path)


def scrape_game(pfr_link):
    pfr_data = pfr.scrape_game(pfr_link)

    return pfr_data


def get_scraped_errors(filename):
    data = import_scrape(filename)
    return [player for player in data['players'] if player.get('errors')]


def print_scraped_errors(filename):
    for player in get_scraped_errors(filename):
        print('%s %s (%s - %s): %s' %
              (player['first'], player['last'], player['position'], player['team'], player['errors']))


def export_scrape(filename, data):
    name, suffix = split_filename_type(filename, 'json')
    filename = '%s_%s%s' % (name, get_timestamp(), suffix)
    export_path = './scrape/data/' + filename

    with open(export_path, 'w') as file:
        json.dump(data, file)

    return filename


# Utilities
pfr_player_list_url = 'https://www.pro-football-reference.com/years/%s/fantasy.htm' % current_year
pfr_player_list = pfr.PlayerListScraper(pfr_player_list_url)

pfr_game_list_url = 'https://www.pro-football-reference.com/years/%s/games.htm' % current_year
pfr_game_list = pfr.GameListScraper(pfr_game_list_url)


def split_filename_type(filename, file_type):
    def format_type():
        return '.%s' % file_type if not file_type.startswith('.') else file_type

    suffix = format_type()

    def split_suffix():
        return tuple(filter(None, re.split('(%s)' % suffix, filename)))

    return (filename, suffix) if not filename.endswith(suffix) else split_suffix()


def get_timestamp():
    return datetime.now().strftime('%Y-%m-%d_%H-%M-%S')


def import_scrape(filename):
    with open('./scrape/data/%s%s' % split_filename_type(filename, 'json')) as file:
        return json.load(file)


if __name__ == '__main__':
    # guru_list_url = 'http://rotoguru1.com/cgi-bin/fstats.cgi?pos=0&sort=1&game=p&colA=0&daypt=0&xavg=0&inact=0&maxprc=99999&outcsv=0'
    # scrape_and_export(guru_list_url)

    scrape_games_and_export()
    driver.close()

    # db.reset_tables()
    # db.session.commit()
