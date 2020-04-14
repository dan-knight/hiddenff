from scrape.base import RequestsScraper, SeleniumScraper, driver
from selenium.webdriver.support import expected_conditions as cond
from selenium.webdriver.common.by import By
from main import current_year

import re


class PlayerListScraper(RequestsScraper):
    pass

    def get_player_links(self):
        def get_rows():
            container = self.soup.find('div', id='all_fantasy')
            tbody = container.find('tbody')
            return tbody.find_all('tr', class_=lambda x: x != 'thead')

        def get_link(row):
            td = row.find('td', {'data-stat': 'player'})
            a = td.find('a')
            return prepend_link(a['href'])

        return [get_link(row) for row in get_rows()]


class PlayerPageScraper(RequestsScraper):
    def __init__(self, url, year=current_year):
        self.year = year

        def format_gamelog_url():
            append = '/gamelog/%s/' % self.year
            return re.sub('.htm$', append, url)

        super().__init__(format_gamelog_url())

    def scrape_basic_info(self):
        container = self.soup.find('div', id='meta')

        def get_name():
            first_text = ''
            last_text = ''
            h1 = container.find('h1', {'itemprop': 'name'})

            try:
                full_name = h1.text
                split_name = full_name.split(' ', 1)
                first_text = split_name[0]
                last_text = split_name[1]
            except (IndexError, AttributeError):
                self.data['errors'].append('name')

            return first_text, last_text

        def get_position():
            text = ''
            strong = container.find('strong', text={re.compile('Position')})

            try:
                raw_text = strong.next_sibling

                def format_position():
                    stripped = raw_text.strip()
                    return re.sub('^: ', '', stripped)

                text = format_position()
            except AttributeError:
                self.data['errors'].append('position')

            return text

        def get_team():
            text = ''
            span = container.find('span', {'itemprop': 'affiliation'})

            try:
                text = span.text
            except AttributeError:
                self.data['errors'].append('team')

            return text

        def get_birth_date():
            year = ''
            month = ''
            day = ''

            span = container.find('span', id='necro-birth')

            try:
                text = span['data-birth']
                split_text = text.split('-')
                year = split_text[0]
                month = split_text[1]
                day = split_text[2]
            except (AttributeError, IndexError):
                self.data['errors'].append('birth_date')

            return year, month, day

        first, last = get_name()
        position = get_position()
        team = get_team()
        birth_year, birth_month, birth_day = get_birth_date()

        return first, last, position, team, birth_year, birth_month, birth_day, self.data['errors']

    def scrape_game_stats(self, week):
        pass


def scrape_season(year):
    player_list_url = 'https://www.pro-football-reference.com/years/%s/fantasy.htm' % year
    player_links = PlayerListScraper(player_list_url).get_player_links()

    for link in player_links:
        basic = PlayerPageScraper(link, year).scrape_basic_info()
        print(basic)


def scrape_player(link):
    pass


# Utilities
def prepend_link(link):
    return 'https://www.pro-football-reference.com' + link
