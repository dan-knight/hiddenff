from scrape import pfr
from scrape.base import driver
import db
import learn

import json
import re
from datetime import datetime


def scrape_and_export():
    data = {
        'players': pfr.scrape_season()
    }

    export_scrape('scrape', data)


def check_scraped_errors(filename):
    data = import_scrape(filename)

    for player in data['players']:
        if player['errors']:
            print('%s %s (%s - %s): %s' %
                  (player['first'], player['last'], player['position'], player['team'], player['errors']))


# Utilities
current_year = 2019
current_week = 17


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
    # scrape_and_export()
    check_scraped_errors('scrape_2020-04-15_17-47-30.json')
    driver.close()
