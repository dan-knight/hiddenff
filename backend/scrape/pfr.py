from scrape.base import RequestsScraper, SeleniumScraper
from config import current_season, current_week
from utility import month_keys

from selenium.webdriver.support import expected_conditions as cond
from selenium.webdriver.common.by import By

import re
import json


class GameListScraper(RequestsScraper):
    def __init__(self, season):
        url = 'https://www.pro-football-reference.com/years/%s/games.htm' % season
        super().__init__(url)

        def get_container():
            div = self.soup.find('div', id='all_games')
            return div.find('tbody')

        self.container = get_container()

    def get_week_links(self, week):
        cells = self.container.find_all('th', {'data-stat': 'week_num'}, text=week)
        return [GameListScraper.get_link(th.parent) for th in cells]

    @staticmethod
    def get_link(row):
        link = ''

        try:
            a = row.find('a', text='boxscore')
            link = prepend_link(a['href'])
        except AttributeError:
            pass

        return link


class PlayerListScraper(RequestsScraper):
    def __init__(self, season):
        url = 'https://www.pro-football-reference.com/years/%s/fantasy.htm' % season
        super().__init__(url)

        def get_container():
            div = self.soup.find('div', id='all_fantasy')
            return div.find('tbody')

        self.container = get_container()

    def get_link(self, first, last):
        full_name = ' '.join((first, last))

        def scrape_list(name):
            link = ''

            def get_name_matches():
                def element_matches(element):
                    return element.name == 'a' and element.text.strip(' ') == name

                return self.container.find_all(element_matches)

            def get_href(a):
                return prepend_link(a['href'])

            link_matches = get_name_matches()

            if len(link_matches) == 1:
                link = get_href(link_matches[0])
            elif len(link_matches) == 0:
                error_name = errors['player_names'].get(full_name)

                if error_name:
                    link = scrape_list(error_name)
                else:
                    link = prepend_link(errors['player_links'].get(full_name))

            return link

        return scrape_list(full_name)


class GamePageScraper(SeleniumScraper):
    def __init__(self, url):
        super().__init__(url)
        self.scorebox = self.soup.find('div', attrs={'class': 'scorebox'})

    def interact_with_page(self):
        super().wait_for_condition(cond.presence_of_element_located(
            (By.ID, 'home_snap_counts')
        ))

        super().wait_for_condition(cond.presence_of_element_located(
            (By.ID, 'vis_snap_counts')
        ))

    def scrape_basic_info(self):
        def get_season():
            season = ''

            def get_li():
                container = self.soup.find('div', id='inner_nav')
                ul = container.find('ul', attrs={'class': 'hoversmooth'})
                return ul.find('li', text=re.compile('NFL Scores'))

            try:
                text = get_li().text
                split_text = text.split(' ', 1)
                season = split_text[0]
            except AttributeError:
                self.add_error('season')

            return season

        def get_week():
            text = ''

            try:
                div = self.soup.find('div', id='div_other_scores')
                h2 = div.find('h2')
                a = h2.find('a')
                text = a.text.split(' ')[-1]
            except AttributeError:
                self.add_error('week')

            return text

        def scrape_scorebox():
            meta_div = self.scorebox.find('div', attrs={'class': 'scorebox_meta'})

            def get_meta_text(label):
                text = ''

                try:
                    strong = meta_div.find('strong', text=lambda x: label in x)
                    div = strong.parent
                    text = div.text.split(': ', 1)[1]
                except AttributeError:
                    self.add_error(label)

                return text

            def get_start():
                start = ''

                def get_date():
                    def get_text():
                        text_ = ''

                        try:
                            div = meta_div.find('div')
                            text_ = div.text
                        except AttributeError:
                            self.add_error('date')

                        return text_

                    text = get_text()

                    def format_date():
                        text_ = ''
                        try:
                            split_text = text.split(' ')

                            def get_day():
                                day_text = split_text[2].strip(',')

                                if int(day_text) < 10:
                                    day_text = '0' + day_text

                                return day_text

                            year = split_text[-1]
                            month = month_keys[split_text[1]]
                            day = get_day()
                            text_ = '-'.join([year, month, day])
                        except IndexError:
                            self.add_error('date')

                        return text_

                    if text:
                        text = format_date()

                    return text

                def get_time():
                    time_text = get_meta_text("Start Time")

                    def format_time():
                        split_text = time_text[:-2].split(':')
                        hours = int(split_text[0])

                        if time_text.endswith('pm') and hours < 12:
                            hours += 12
                        elif hours < 10:
                            hours = '0' + str(hours)

                        text = '%s:%s:00' % (str(hours), split_text[1])

                        return text

                    if time_text:
                        time_text = format_time()

                    return time_text

                date = get_date()
                time = get_time()

                if date and time:
                    start = '%s %s' % (get_date(), get_time())

                return start

            def get_stadium():
                name = ''
                link = ''

                try:
                    strong = meta_div.find('strong', text=re.compile('Stadium'))
                    div = strong.parent
                    a = div.find('a')
                    name = a.text
                    link = prepend_link(a['href'])
                except (AttributeError, KeyError):
                    self.add_error('stadium')

                return name, link

            start_text = get_start()
            stadium_name_text, stadium_link_text = get_stadium()
            length_text = get_meta_text('Time of Game')

            return start_text, stadium_name_text, stadium_link_text, length_text

        start, stadium_name, stadium_link, length = scrape_scorebox()

        def scrape_game_info():
            div = self.soup.find('table', id='game_info')

            def get_row_value(label):
                th = div.find('th', {'data-stat': 'info'},
                              text=re.compile(label))

                return th.next_sibling.text

            roof_text = get_row_value('Roof')
            surface_text = get_row_value('Surface')
            spread_text = get_row_value('Vegas Line')
            over_under_text = get_row_value('Over/Under')

            return roof_text, surface_text, spread_text, over_under_text

        roof, surface, spread, over_under = scrape_game_info()

        self.data.update({
            'season': get_season(),
            'week': get_week(),
            'start': start,
            'stadium_name': stadium_name,
            'stadium_link': stadium_link,
            'length': length,
            'roof': roof,
            'surface': surface,
            'spread': spread,
            'over_under': over_under,
        })

    def scrape_team_info(self):
        basic_info_divs = self.scorebox.find_all('div', attrs={'class': False},
                                                 recursive=False)

        snap_count_divs = [
            self.soup.find('table', id='home_snap_counts'),
            self.soup.find('table', id='vis_snap_counts')
        ]

        teams = []

        for index, team_div in enumerate(basic_info_divs):
            def scrape_team():
                def get_element_text(element, error_name):
                    text = ''

                    try:
                        text = element.text
                    except AttributeError:
                        self.add_error(error_name)

                    return text

                def get_snaps():
                    snaps = ''

                    def get_cells():
                        table = snap_count_divs[index]

                        def get_percent_cell():
                            cell = table.find('td', {'data-stat': 'off_pct'},
                                                 text=re.compile('100%'))

                            if not cell:
                                cell = table.find('td', {'data-stat': 'off_pct'},
                                              text=lambda x: x != '0%')

                            return cell

                        percent = get_percent_cell()
                        row = percent.parent
                        amount = row.find('td', {'data-stat': 'offense'})

                        return percent, amount

                    try:
                        percent_cell, amount_cell = get_cells()

                        def calculate_snaps():
                            def get_percent():
                                text = percent_cell.text.split('%')[0]
                                return int(text)

                            percent = get_percent()
                            amount = int(amount_cell.text)
                            result = percent * 0.01 * amount
                            return round(result)

                        snaps = calculate_snaps()
                    except AttributeError:
                        self.add_error('snaps')

                    return snaps

                team_name = get_element_text(
                        team_div.find('a', {'itemprop': 'name'}), 'name')

                score = get_element_text(
                        team_div.find('div', attrs={'class': 'score'}), 'score')

                snaps = get_snaps()

                return {
                    'team': team_name,
                    'score': score,
                    'snaps': snaps
                }

            teams.append(scrape_team())

        self.data.update({'team_games': teams})


class StadiumPageScraper(RequestsScraper):
    pass

    def scrape_basic_info(self):
        container = self.soup.find('div', id='meta')

        def scrape_row(label, stat_name):
            data = []

            def get_entries():
                p = container.find('b', text=re.compile(label))
                text = p.next_sibling.strip()
                return text.split(', ')

            def parse_entry(entry):
                split_text = entry.split(' (')
                surface_text = split_text[0].strip()
                years_text = split_text[1].strip(')').split('-')
                return {stat_name: surface_text,
                        'seasons': years_text}

            try:
                data = [parse_entry(entry) for entry in get_entries()]
            except (AttributeError, IndexError):
                self.add_error(stat_name)

            return data

        def get_names():
            stat_name = 'name'

            names = scrape_row('Known As', stat_name)

            if not names:
                def get_title_name():
                    name = ''

                    try:
                        h1 = container.find('h1', {'itemprop': 'name'})
                        name = h1.text.split(' History', 1)[0]
                        self.data['errors'].remove('name')
                    except AttributeError:
                        self.add_error('names')

                    return name

                def get_years_active():
                    years = []
                    try:
                        p = container.find('b', text=re.compile('Years Active'))
                        text = p.next_sibling
                        years_text = text.split('(')[0].strip()
                        years = years_text.split('-')
                    except AttributeError:
                        pass

                    return years

                names = [{stat_name: get_title_name(),
                          'seasons': get_years_active()}]

            return names

        self.data['names'] = get_names()
        self.data['surfaces'] = scrape_row('Surfaces', 'surface')


class PlayerPageScraper(RequestsScraper):
    def __init__(self, url, season):
        def format_gamelog_url():
            append = '/gamelog/%s/' % season
            return re.sub('.htm$', append, url)

        super().__init__(format_gamelog_url())

        self.season = season
        self.meta_div = self.soup.find('div', id='meta')
        self.data['games'] = {season: {}}

    def scrape_basic_info(self):
        def get_name():
            first_text = ''
            last_text = ''
            h1 = self.meta_div.find('h1', {'itemprop': 'name'})

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
            span = self.meta_div.find('span', {'itemprop': 'affiliation'})

            try:
                text = span.text
            except AttributeError:
                self.add_error('team')

            return text

        def get_birthday():
            text = ''

            span = self.meta_div.find('span', id='necro-birth')

            try:
                text = span['data-birth']
            except TypeError:
                self.add_error('birthday')

            return text

        first, last = get_name()

        self.data.update({
            'first': first,
            'last': last,
            'team': get_team(),
            'birthday': get_birthday()
        })

    def scrape_position(self):
        pass

    def scrape_game_stats(self, weeks):
        def get_game_rows(game_weeks):
            rows = []

            try:
                for week in game_weeks:
                    td = self.soup.find('td', {'data-stat': 'week_num'}, text=week)
                    if td:
                        rows.append(td.parent)
            except TypeError:
                rows = get_game_rows([game_weeks])
            return rows

        for row in get_game_rows(weeks):
            def scrape_game_row():
                def get_datastat_text(label):
                    text = '0'
                    td = row.find('td', {'data-stat': label})

                    try:
                        text = td.text
                    except AttributeError:
                        pass

                    return text

                week = get_datastat_text('week_num')

                data = {week: {'team': get_datastat_text('team'),
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
                               }}

                return data

            try:
                self.data['games'][self.season].update(scrape_game_row())
            except AttributeError:
                pass


def get_player_link(first, last, seasons=current_season):
    global player_list_cache

    link = ''

    for season in seasons:
        try:
            player_list = player_list_cache[season]
        except KeyError:
            player_list = PlayerListScraper(season)

        link = player_list.get_link(first, last)

        if link:
            break

    return link


def get_game_links(week, season):
    global game_list_cache

    try:
        links = game_list_cache[season].get_week_links(week)
    except KeyError:
        game_list_cache[season] = GameListScraper(season)
        links = get_game_links(week, season)

    return links


def scrape_player(link, season_week_pairs):
    player = {'games': {}}
    seasons = list(season_week_pairs)
    first_season = seasons.pop()

    def add_basic_info():
        player_scraper = PlayerPageScraper(link, first_season)

        player_scraper.scrape_basic_info()
        player.update(player_scraper.data)

        return player_scraper

    def scrape_games():

        def add_season(scraper, season_):
            scraper.scrape_game_stats(season_week_pairs[season_])

            if scraper.data['games'][scraper.season]:
                player['games'].update(scraper.data['games'])

        first_scraper = add_basic_info()
        add_season(first_scraper, first_season)

        for season in seasons:
            game_scraper = PlayerPageScraper(link, season)
            add_season(game_scraper, season)

    scrape_games()

    return player


def scrape_game(link):
    game = GamePageScraper(link)
    game.scrape_basic_info()
    game.scrape_team_info()
    return game.data


def scrape_stadium(link):
    stadium = StadiumPageScraper(link)
    stadium.scrape_basic_info()
    return stadium.data


# Utilities
player_list_cache = {}
game_list_cache = {}

with open('./scrape/error/pfr.json') as file:
    errors = json.load(file)


def prepend_link(link):
    try:
        text = 'https://www.pro-football-reference.com' + link
    except TypeError:
        text = ''

    return text
