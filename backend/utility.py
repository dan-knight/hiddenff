import datetime as dt


def create_datetime(iso_datetime):
    split_text = iso_datetime.split(' ')

    date = create_date(split_text[0])
    time = create_time(split_text[1])

    return dt.datetime.combine(date, time)


def create_date(iso_date):
    split_text = iso_date.split('-')

    return dt.date(int(split_text[0]),
                   int(split_text[1]),
                   int(split_text[2]))


def create_time(iso_time):
    split_text = iso_time.split(':')

    return dt.time(int(split_text[0]),
                   int(split_text[1]),
                   int(split_text[2]))


def try_data_then_kwargs(stat_name, data, **kwargs):
    try:
        value = data[stat_name]
    except KeyError:
        value = kwargs[stat_name]

    return value


def combine_dicts(*args):
    combined = {}

    def add(new):
        for new_key, new_value in new.items():
            if new_value is None:
                continue

            old_value = combined.get(new_key)

            def overwrite_value():
                combined[new_key] = new_value

            def add_to_list(list_values, data_to_add, insert_index=None):
                def get_insert_index():
                    return len(list_values) if insert_index is None else insert_index

                if isinstance(data_to_add, list):
                    list_values.extend(data_to_add)
                else:
                    list_values.insert(get_insert_index(), data_to_add)

                combined[new_key] = list_values

            if old_value is None:
                overwrite_value()
            elif isinstance(old_value, list):
                add_to_list(old_value, new_value)
            elif isinstance(old_value, dict) and isinstance(new_value, dict):
                old_value.update(new_value)
            elif isinstance(new_value, list):
                add_to_list(new_value, old_value, 0)
            else:
                overwrite_value()

    for d in args:
        add(d)

    return combined


# Keys
def get_team_keys():
    teams = {}
    teams.update(dict.fromkeys(['Arizona Cardinals', 'ARI'], 'ARI'))
    teams.update(dict.fromkeys(['Atlanta Falcons', 'ATL'], 'ATL'))
    teams.update(dict.fromkeys(['Baltimore Ravens', 'BAL'], 'BAL'))
    teams.update(dict.fromkeys(['Buffalo Bills', 'BUF'], 'BUF'))
    teams.update(dict.fromkeys(['Carolina Panthers', 'CAR'], 'CAR'))
    teams.update(dict.fromkeys(['Chicago Bears', 'CHI'], 'CHI'))
    teams.update(dict.fromkeys(['Cincinnati Bengals', 'CIN'], 'CIN'))
    teams.update(dict.fromkeys(['Cleveland Browns', 'CLE'], 'CLE'))
    teams.update(dict.fromkeys(['Dallas Cowboys', 'DAL'], 'DAL'))
    teams.update(dict.fromkeys(['Denver Broncos', 'DEN'], 'DEN'))
    teams.update(dict.fromkeys(['Detroit Lions', 'DET'], 'DET'))
    teams.update(dict.fromkeys(['Green Bay Packers', 'GB', 'GNB'], 'GB'))
    teams.update(dict.fromkeys(['Houston Texans', 'HOU'], 'HOU'))
    teams.update(dict.fromkeys(['Indianapolis Colts', 'IND'], 'IND'))
    teams.update(dict.fromkeys(['Jacksonville Jaguars', 'JAX'], 'JAX'))
    teams.update(dict.fromkeys(['Kansas City Chiefs', 'KC', 'KAN'], 'KC'))
    teams.update(dict.fromkeys(['Las Vegas Raiders', 'Oakland Raiders', 'OAK'], 'OAK'))
    teams.update(dict.fromkeys(['Los Angeles Chargers', 'LAC'], 'LAC'))
    teams.update(dict.fromkeys(['Los Angeles Rams', 'LAR'], 'LAR'))
    teams.update(dict.fromkeys(['Miami Dolphins', 'MIA'], 'MIA'))
    teams.update(dict.fromkeys(['Minnesota Vikings', 'MIN'], 'MIN'))
    teams.update(dict.fromkeys(['New England Patriots', 'NE', 'NWE'], 'NE'))
    teams.update(dict.fromkeys(['New Orleans Saints', 'NO', 'NOR'], 'NO'))
    teams.update(dict.fromkeys(['New York Giants', 'NYG'], 'NYG'))
    teams.update(dict.fromkeys(['New York Jets', 'NYJ'], 'NYJ'))
    teams.update(dict.fromkeys(['Philadelphia Eagles', 'PHI'], 'PHI'))
    teams.update(dict.fromkeys(['Pittsburgh Steelers', 'PIT'], 'PIT'))
    teams.update(dict.fromkeys(['San Francisco 49ers', 'SF', 'SFO'], 'SF'))
    teams.update(dict.fromkeys(['Seattle Seahawks', 'SEA'], 'SEA'))
    teams.update(dict.fromkeys(['Tampa Bay Buccaneers', 'TB', 'TAM'], 'TB'))
    teams.update(dict.fromkeys(['Tennessee Titans', 'TEN'], 'TEN'))
    teams.update(dict.fromkeys(['Washington Redskins', 'Washington Football Team', 'WAS'], 'WAS'))
    teams.update(dict.fromkeys(['Free agent', ''], None))

    return teams


team_keys = get_team_keys()


def get_month_keys():
    months = {}
    months.update(dict.fromkeys(['Sep'], '09'))
    months.update(dict.fromkeys(['Oct'], '10'))
    months.update(dict.fromkeys(['Nov'], '11'))
    months.update(dict.fromkeys(['Dec'], '12'))
    months.update(dict.fromkeys(['Jan'], '01'))
    months.update(dict.fromkeys(['Feb'], '02'))

    return months


month_keys = get_month_keys()


def get_roof_keys():
    roofs = {}
    roofs.update(dict.fromkeys(['dome', 'retractable roof (closed)'], True))
    roofs.update(dict.fromkeys(['outdoors', 'retractable roof (open)'], False))

    return roofs


roof_keys = get_roof_keys()


def get_surface_keys():
    surfaces = {}
    surfaces.update(dict.fromkeys(['texasturf', 'astroturf', 'matrixturf', 'polyturf',
                                   'dessograss', 'tartanturf', 'sportturf', 'fieldturf',
                                   'astroplay', 'a_turf'], 'turf'))
    surfaces.update(dict.fromkeys(['grass', 'dirt'], 'grass'))

    return surfaces


surface_keys = get_surface_keys()
