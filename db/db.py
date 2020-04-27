from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


uri = 'mysql+pymysql://root:@localhost:3307/hiddenff'
engine = create_engine(uri)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Player(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True)
    first = Column(String(32), nullable=False)
    last = Column(String(32), nullable=False)
    position = Column(String(2))
    team = Column(String(50))
    birth_year = Column(Integer, nullable=False)
    birth_month = Column(Integer, nullable=False)
    birth_day = Column(Integer, nullable=False)

    def __repr__(self):
        return '%s %s (%s): %s' % (self.first, self.last, self.position, self.team)


def create_player(player_data):
    player = Player(first=player_data['first'],
                    last=player_data['last'],
                    position=player_data['position'],
                    team=team_keys[player_data['team']],
                    birth_year=player_data['birth_year'],
                    birth_month=player_data['birth_month'],
                    birth_day=player_data['birth_day'])

    return player


def add_player(player):
    session.add(player)


def find_player(player_data):
    player = session.query(Player).filter_by(first=player_data['first'],
                                             last=player_data['last'],
                                             birth_year=player_data['birth_year'],
                                             birth_month=player_data['birth_month'],
                                             birth_day=player_data['birth_day']).first()

    return player


# Utilities
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
    teams.update(dict.fromkeys(['Green Bay Packers', 'GB'], 'GB'))
    teams.update(dict.fromkeys(['Houston Texans', 'HOU'], 'HOU'))
    teams.update(dict.fromkeys(['Indianapolis Colts', 'IND'], 'IND'))
    teams.update(dict.fromkeys(['Jacksonville Jaguars', 'JAX'], 'JAX'))
    teams.update(dict.fromkeys(['Kansas City Chiefs', 'KC'], 'KC'))
    teams.update(dict.fromkeys(['Las Vegas Raiders', 'Oakland Raiders', 'OAK'], 'OAK'))
    teams.update(dict.fromkeys(['Los Angeles Chargers', 'LAC'], 'LAC'))
    teams.update(dict.fromkeys(['Los Angeles Rams', 'LAR'], 'LAR'))
    teams.update(dict.fromkeys(['Miami Dolphins', 'MIA'], 'MIA'))
    teams.update(dict.fromkeys(['Minnesota Vikings', 'MIN'], 'MIN'))
    teams.update(dict.fromkeys(['New England Patriots', 'NE'], 'NE'))
    teams.update(dict.fromkeys(['New Orleans Saints', 'NO'], 'NO'))
    teams.update(dict.fromkeys(['New York Giants', 'NYG'], 'NYG'))
    teams.update(dict.fromkeys(['New York Jets', 'NYJ'], 'NYJ'))
    teams.update(dict.fromkeys(['Philadelphia Eagles', 'PHI'], 'PHI'))
    teams.update(dict.fromkeys(['Pittsburgh Steelers', 'PIT'], 'PIT'))
    teams.update(dict.fromkeys(['San Francisco 49ers', 'SF'], 'SF'))
    teams.update(dict.fromkeys(['Seattle Seahawks', 'SEA'], 'SEA'))
    teams.update(dict.fromkeys(['Tampa Bay Buccaneers', 'TB'], 'TB'))
    teams.update(dict.fromkeys(['Tennessee Titans', 'TEN'], 'TEN'))
    teams.update(dict.fromkeys(['Washington Redskins', 'WAS'], 'WAS'))
    teams.update(dict.fromkeys(['Free agent', ''], ''))

    return teams


team_keys = get_team_keys()


def reset_tables():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
