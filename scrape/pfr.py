from scrape.base import RequestsScraper, SeleniumScraper, driver
from selenium.webdriver.support import expected_conditions as cond
from selenium.webdriver.common.by import By
from main import current_year, current_week

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
        self.data['games'] = []

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
        birth_year, birth_month, birth_day = get_birth_date()

        self.data.update({
            'first': first,
            'last': last,
            'position': get_position(),
            'team': get_team(),
            'birth_year': birth_year,
            'birth_month': birth_month,
            'birth_day': birth_day
        })

    def scrape_game_stats(self, week):
        def get_row():
            td = self.soup.find('td', {'data-stat': 'week_num'}, text=week)
            return td.parent

        try:
            row = get_row()

            def get_datastat_text(label):
                text = '0'
                td = row.find('td', {'data-stat': label})

                try:
                    text = td.text
                except AttributeError:
                    pass

                return text

            self.data['games'].append({
                'week': week,
                'team': get_datastat_text('team'),
                'rush_att': get_datastat_text('rush_att'),
                'rush_yd': get_datastat_text('rush_yds'),
                'rush_td': get_datastat_text('rush_td'),
                'fum': get_datastat_text('fumbles'),
                'tgt': get_datastat_text('targets'),
                'rec': get_datastat_text('rec'),
                'rec_yd': get_datastat_text('rec_yds'),
                'rec_td': get_datastat_text('rec_td'),
                'pass_att': get_datastat_text('pass_att'),
                'pass_cmp': get_datastat_text('pass_cmp'),
                'pass_yd': get_datastat_text('pass_yds'),
                'pass_td': get_datastat_text('pass_td'),
                'int': get_datastat_text('pass_int'),
                'sacked': get_datastat_text('pass_sacked'),
                'snaps': get_datastat_text('offense')
            })
        except AttributeError:
            pass


def scrape_season(year):
    player_list_url = 'https://www.pro-football-reference.com/years/%s/fantasy.htm' % year
    player_links = PlayerListScraper(player_list_url).get_player_links()

    for link in player_links:
        print(scrape_player(link, year))


def scrape_player(link, year):
    player = PlayerPageScraper(link, year)
    player.scrape_basic_info()
    player.scrape_game_stats(current_week)
    return player.data


# Utilities
def prepend_link(link):
    return 'https://www.pro-football-reference.com' + link
