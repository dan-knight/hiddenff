from scrape import pfr
from scrape.base import driver
import db
import learn


if __name__ == '__main__':
    pfr.scrape_season(2019)

    driver.close()
