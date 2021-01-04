import scrape.pfr
import scrape.guru
import scrape.wiki


def scrape_player(guru_link, season_week_pairs, name=None):
    guru_data = guru.scrape_player(guru_link, name)

    def get_pfr_link():
        link = pfr.get_player_link(guru_data['first'], guru_data['last'], list(season_week_pairs))

        if not link:
            link = pfr.prepend_link(pfr.errors['player_links'].get(guru_link))

        return link

    pfr_link = get_pfr_link()

    def get_pfr_data():
        return pfr.scrape_player(pfr_link, season_week_pairs) if pfr_link else {'url': pfr_link,
                                                                                'errors': {'pfr_link'}}

    pfr_data = get_pfr_data()

    def combine_scraped_data():
        scraped_data = {
            'links': [guru_data['url'], pfr_link],
            'first': guru_data['first'],
            'last': guru_data['last'],
            'position': guru_data['position'],
            'team': pfr_data.get('team'),
            'birthday': pfr_data.get('birthday'),
            'games': pfr_data.get('games'),
        }

        def check_data_errors():
            full_name = '%s %s' % (scraped_data['first'], scraped_data['last'])

            def update_from_errors(errors):
                scraped_data.update(errors['data'].get(full_name, {}))

            update_from_errors(pfr.errors)

        check_data_errors()

        def check_errors():
            def combine_errors():
                all_errors = guru_data['errors']
                all_errors.update(pfr_data['errors'])
                return all_errors

            errors = combine_errors()

            if errors:
                wiki_links = wiki.get_player_links(scraped_data['first'], scraped_data['last'], scraped_data['position'])
                for link in wiki_links:
                    wiki_data = wiki.scrape_player(link)

                    if wiki_data['birthday'] == scraped_data['birthday']:
                        def update_scraped_data():
                            for error in errors.copy():
                                if wiki_data.get(error):
                                    scraped_data.update({error: wiki_data[error]})
                                    errors.remove(error)

                        update_scraped_data()
                        break

            scraped_data.update({'errors': list(errors)})

        check_errors()
        return scraped_data

    return combine_scraped_data()


def scrape_game(pfr_link):
    pfr_game = pfr.scrape_game(pfr_link)
    pfr_game['errors'] = list(pfr_game['errors'])

    return pfr_game

