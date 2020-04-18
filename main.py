from scrape import pfr
from scrape import guru
from scrape.base import driver
import db
import learn
from config import current_year

import json
import re
from datetime import datetime


def scrape_and_export():
    data = {
        'players': pfr.scrape_season()
    }

    export_scrape('scrape', data)


def scrape_player(guru_link):
    guru_data = guru.scrape_player(guru_link)

    pfr_link = pfr_player_list.get_player_link(guru_data['first'], guru_data['last'])
    pfr_data = pfr.scrape_player(pfr_link)

    def combine_scraped_data():
        player_data = {}
        player_data.update(pfr_data)
        player_data.update({
            'first': guru_data['first'],
            'last': guru_data['last'],
            'position': guru_data['position']
        })

        player_data['url'] = [guru_data['url'], pfr_data['url']]
        player_data['errors'] = [guru_data['errors'] + pfr_data['errors']]

        return player_data

    return combine_scraped_data()


def check_scraped_errors(filename):
    data = import_scrape(filename)

    for player in data['players']:
        if player['errors']:
            print('%s %s (%s - %s): %s' %
                  (player['first'], player['last'], player['position'], player['team'], player['errors']))


# Utilities
pfr_player_list_url = 'https://www.pro-football-reference.com/years/%s/fantasy.htm' % current_year
pfr_player_list = pfr.PlayerListScraper(pfr_player_list_url)


def split_filename_type(filename, file_type):
    def format_type():
        return '.%s' % file_type if not file_type.startswith('.') else file_type

    suffix = format_type()

    def split_suffix():
        return tuple(filter(None, re.split('(%s)' % suffix, filename)))

    return (filename, suffix) if not filename.endswith(suffix) else split_suffix()


def get_timestamp():
    return datetime.now().strftime('%Y-%m-%d_%H-%M-%S')


def export_scrape(filename, data):
    name, suffix = split_filename_type(filename, 'json')

    with open('./scrape/data/%s_%s%s' % (name, get_timestamp(), suffix), 'w') as file:
        json.dump(data, file)


def import_scrape(filename):
    with open('./scrape/data/%s%s' % split_filename_type(filename, 'json')) as file:
        return json.load(file)


if __name__ == '__main__':
    guru_list_url = 'http://rotoguru1.com/cgi-bin/fstats.cgi?pos=0&sort=1&game=p&colA=0&daypt=0&xavg=0&inact=0&maxprc=99999&outcsv=0'
    players = [scrape_player(link) for link in guru.PlayerListScraper(guru_list_url).get_player_links()]
    export_scrape('guru-pfr-scrape', {'players': players})

    driver.close()
