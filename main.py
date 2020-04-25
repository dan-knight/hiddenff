from scrape import pfr
from scrape import guru
from scrape import wiki
from scrape.base import driver
import db
import learn
from config import current_year

import json
import re
from datetime import datetime


def scrape_and_export(guru_list_link):
    data = {
        'players': [scrape_player(link) for link in guru.PlayerListScraper(guru_list_link).get_player_links()]
    }

    export_path = export_scrape('guru-pfr-scrape', data)
    print_scraped_errors(export_path)


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
        player_data['errors'] = guru_data['errors'] + pfr_data['errors']

        return player_data

    return combine_scraped_data()


def get_scraped_errors(filename):
    data = import_scrape(filename)
    return [player for player in data['players'] if player['errors']]


def print_scraped_errors(filename):
    for player in get_scraped_errors(filename):
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
    filename = '%s_%s%s' % (name, get_timestamp(), suffix)
    export_path = './scrape/data/' + filename

    with open(export_path, 'w') as file:
        json.dump(data, file)

    return filename


def import_scrape(filename):
    with open('./scrape/data/%s%s' % split_filename_type(filename, 'json')) as file:
        return json.load(file)


if __name__ == '__main__':
    # guru_list_url = 'http://rotoguru1.com/cgi-bin/fstats.cgi?pos=0&sort=1&game=p&colA=0&daypt=0&xavg=0&inact=0&maxprc=99999&outcsv=0'
    # scrape_and_export(guru_list_url)

    errors = get_scraped_errors('guru-pfr-scrape_2020-04-18_18-18-37.json')
    for player in errors:
        print(player['first'], player['last'])
        links = wiki.get_player_links(player['first'], player['last'], player['position'])
        if links:
            for link in links:
                print(wiki.scrape_player(link))

    driver.close()
