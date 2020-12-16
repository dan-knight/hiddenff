from scrape.base import RequestsScraper, SeleniumScraper, driver

from selenium.webdriver.support import expected_conditions as cond
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4.element import NavigableString

import json
import re


class StadiumListScraper(RequestsScraper):
    def __init__(self, url):
        super().__init__(url)

        def get_container():
            mw_pages = self.soup.find('div', id='mw-pages')
            return mw_pages.find('div', attrs={'class': 'mw-category'})

        self.container = get_container()

    def get_link(self, name):
        link = ''

        try:
            a = self.container.find('a', text=name)
            link = prepend_link(a['href'])
        except TypeError:
            pass

        return link


class PlayerListScraper(SeleniumScraper):
    def __init__(self, url):
        super().__init__(url)
        self.data['player_links'] = []

        def get_container():
            category = self.soup.find('div', attrs={'class': 'mw-category'})
            return category if category else self.soup.find('div', attrs={'class': 'mw-category-generated'})

        self.container = get_container()

    def interact_with_page(self):
        try:
            super().wait_for_condition(cond.presence_of_element_located(
                (By.CLASS_NAME, 'mw-category')
            ))
        except TimeoutException:
            super().wait_for_condition(cond.presence_of_element_located(
                (By.CLASS_NAME, 'mw-category-generated')
            ))

    def get_links(self, full_name):
        player_links = []

        try:
            a = self.container.find_all('a', text=re.compile(full_name))
            player_links = [prepend_link(link['href']) for link in a]
        except TypeError:
            pass

        self.data['player_links'] = player_links

    def get_next_page_url(self):
        div = self.soup.find('div', id='mw-pages')
        a = div.find('a', text='next page')
        return prepend_link(a['href'])

    def check_last_link(self, last):
        def get_last_player():
            links = self.container.find_all('li')
            li = links[len(links) - 1]
            a = li.find('a')
            name = a.text

            def get_last_name():
                name_no_parenthesis = name.split(' (')[0]
                return name_no_parenthesis.split(' ')[-1]

            return get_last_name()

        last_player = get_last_player()
        return last >= last_player


class StadiumPageScraper(RequestsScraper):
    def __init__(self, url):
        super().__init__(url)
        self.vcard = self.soup.find('table', attrs={'class': 'vcard'})

    def scrape_basic_info(self):
        def get_teams():
            def get_team_rows():
                def get_container():
                    th = self.vcard.find('th', text=re.compile('Tenants'))
                    return th.parent.next_sibling

                return get_container().find_all('a', {'title': 'National Football League'})

            def get_team(nfl_link):
                def get_team_name():
                    team_link = nfl_link.find_previous_sibling('a', text=lambda x: not x == 'AFL')

                    if not team_link and nfl_link.parent.name == 'span':
                        team_link = nfl_link.parent.find_previous_sibling('a')

                    return team_link.text

                def get_years():
                    years = ''

                    def get_text():
                        text = ''

                        def get_element_text(element):
                            element_text = ''

                            if isinstance(element, NavigableString):
                                element_text = element
                            elif element.name == 'a':
                                element_text = element.text
                            elif element.name == 'sup':
                                for child in element.contents:
                                    element_text += get_element_text(child)

                            return element_text

                        for sibling in nfl_link.next_siblings:
                            if sibling.name == 'br':
                                break

                            text += get_element_text(sibling)

                        return text

                    def parse_text(years_text):
                        def get_year_pairs():
                            def format_text():
                                text = years_text.split(') ', 1)[1].strip()
                                no_citation_brackets = text.split('[', 1)[0]
                                return no_citation_brackets.strip('(').strip(')')

                            return format_text().split(', ')

                        return [pair.split('–') for pair in get_year_pairs()]

                    try:
                        years = parse_text(get_text())
                    except IndexError:
                        self.add_error('seasons')

                    return years

                year_pairs = get_years()
                team = get_team_name()

                return [{'team': team,
                        'seasons': years} for years in year_pairs]

            team_data = []

            try:
                for link in get_team_rows():
                    team_data +=get_team(link)
            except AttributeError:
                self.add_error('teams')
            return team_data

        self.data.update({'teams': get_teams()})


class PlayerPageScraper(RequestsScraper):
    def __init__(self, url):
        super().__init__(url)
        self.card = self.soup.find('table', attrs={'class': 'vcard'})

    def get_team(self):
        team_text = ''

        try:
            span = self.card.find('span', attrs={'class': 'org'})
            team_text = span.text
        except AttributeError:
            pass

        self.data['team'] = team_text

    def get_birthday(self):
        text = ''

        try:
            th = self.card.find('th', text=re.compile('Born'))
            td = th.next_sibling
            span = td.find('span', attrs={'class': 'bday'})
            text = span.text
        except AttributeError:
            self.add_error('birthday')

        self.data['birthday'] = text


def get_stadium_link(name):
    global current_stadium_list_scraper

    try:
        link = current_stadium_list_scraper.get_link(name)
    except AttributeError:
        current_stadium_list_scraper = StadiumListScraper('https://en.wikipedia.org/wiki/Category:National_Football_League_venues')
        link = get_stadium_link(name)

    if not link:
        try:
            global former_stadium_list_scraper
            link = former_stadium_list_scraper.get_link(name)
        except AttributeError:
            former_stadium_list_scraper = StadiumListScraper('https://en.wikipedia.org/wiki/Category:Defunct_National_Football_League_venues')
            link = former_stadium_list_scraper.get_link(name)

    return link


def scrape_stadium(link):
    scraper = StadiumPageScraper(link)
    scraper.scrape_basic_info()
    return scraper.data


def get_player_links(first, last, position):
    links = ''
    error_link = errors['player_links'].get(get_full_name(first, last))

    if error_link:
        links = [error_link]
    else:
        def scrape_player_links():
            positions = {
                'RB': 'running_backs',
                'WR': 'wide_receivers',
                'QB': 'quarterbacks',
                'TE': 'tight_ends',
                'FB': 'fullbacks'
            }

            def get_name():
                error_name = errors['player_names'].get(get_full_name(first, last))
                return (error_name['first'], error_name['last']) if error_name else (first, last)

            first_name, last_name = get_name()
            full_name = get_full_name(first_name, last_name)

            def scrape_position(position_suffix):
                def format_url():
                    last_name_suffix = last_name[0]
                    return 'https://en.wikipedia.org/wiki/Category:American_football_%s?from=%s' % \
                           (position_suffix, last_name_suffix)

                scraper = PlayerListScraper(format_url())

                def scrape_list():
                    scraper.get_links(full_name)
                    links = scraper.data['player_links']
                    return links

                links = scrape_list()

                if not links:
                    while scraper.check_last_link(last_name):
                        next_page = scraper.get_next_page_url()
                        scraper = PlayerListScraper(next_page)
                        links = scrape_list()

                return links

            def get_guru_position():
                try:
                    guru_position = positions.pop(position)
                except KeyError:
                    guru_position = positions.pop('RB')

                return guru_position

            player_links = scrape_position(get_guru_position())

            if not player_links:
                def scrape_other_positions():
                    links = []

                    for position_key in positions.keys():
                        links = scrape_position(positions[position_key])

                        if links:
                            break

                    return links

                player_links = scrape_other_positions()

            return player_links

        links = scrape_player_links()

    return links


def scrape_player(link):
    scraper = PlayerPageScraper(link)
    scraper.get_team()
    scraper.get_birthday()
    return scraper.data


# Utilities
current_stadium_list_scraper = None
former_stadium_list_scraper = None

with open('./scrape/error/wiki.json') as file:
    errors = json.load(file)


def prepend_link(link):
    return 'https://en.wikipedia.org' + link


def get_full_name(first, last):
    full_name = '%s %s' % (first, last)
    return full_name.strip()




