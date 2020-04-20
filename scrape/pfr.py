from scrape.base import RequestsScraper
from config import current_year, current_week

import re
import json


class PlayerListScraper(RequestsScraper):
    def __init__(self, url):
        super().__init__(url)

        def get_container():
            div = self.soup.find('div', id='all_fantasy')
            return div.find('tbody')

        self.container = get_container()

    def get_player_link(self, first, last):
        link = ''
        full_name = ' '.join((first, last))

        def get_link(name):
            a = self.container.find('a', text=name)
            return prepend_link(a['href'])

        def check_errors():
            error_name = errors['player_names'].get(full_name)
            return get_link(error_name) if error_name else prepend_link(errors['player_links'].get(full_name, ''))

        try:
            link = get_link(full_name)
        except TypeError:
            link = check_errors()

        return link


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
                self.add_error('name')

            return first_text, last_text

        def get_team():
            text = ''
            span = container.find('span', {'itemprop': 'affiliation'})

            try:
                text = span.text
            except AttributeError:
                self.add_error('team')

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
            except (TypeError, IndexError):
                self.add_error('birth_date')

            return year, month, day

        first, last = get_name()
        birth_year, birth_month, birth_day = get_birth_date()

        self.data.update({
            'first': first,
            'last': last,
            'team': get_team(),
            'birth_year': birth_year,
            'birth_month': birth_month,
            'birth_day': birth_day
        })

    def scrape_game_stats(self, week=current_week):
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


def scrape_player(link, year=current_year, weeks=current_week):
    player = PlayerPageScraper(link, year)
    player.scrape_basic_info()

    def scrape_games():
        for week in weeks:
            player.scrape_game_stats(week)

    try:
        scrape_games()
    except TypeError:
        weeks = [weeks]
        scrape_games()

    return player.data


# Utilities
with open('./scrape/error/pfr.json') as file:
    errors = json.load(file)


def prepend_link(link):
    return 'https://www.pro-football-reference.com' + link
