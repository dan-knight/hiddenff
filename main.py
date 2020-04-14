from scrape import pfr
from scrape.base import driver
import db
import learn

import re


current_year = 2019
current_week = 5


if __name__ == '__main__':
    pfr.scrape_season(2019)

    driver.close()
