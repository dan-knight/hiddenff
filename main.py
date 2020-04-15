from scrape import pfr
from scrape.base import driver
import db
import learn

import json


current_year = 2019
current_week = 17


def check_filename_type(filename, file_type):
    return filename + '.%s' % file_type if not filename.endswith('.%s' % file_type) else filename


def export_scrape(filename, data):
    with open('./scrape/data/%s.json' % check_filename_type(filename, 'json'), 'w') as file:
        json.dump(data, file)


def import_scrape(filename):
    with open('./scrape/data/%s' % check_filename_type(filename, 'json')) as file:
        return json.load(file)


if __name__ == '__main__':
    # players = pfr.scrape_season()
    # export_scrape('scrape', players)

    print(import_scrape('scrape.json'))
    driver.close()
