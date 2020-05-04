from utility import team_keys, roof_keys, create_datetime, create_date

from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, Date, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

import os
import datetime as dt


uri = os.getenv('DATABASE_URI')
engine = create_engine(uri)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class HiddenFF:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def update(cls, data):
        db_row = cls.get(data)

        if not db_row:
            db_row = cls.new(data)
            session.add(db_row)
        else:
            def update_row():
                for column in db_row.modifiable_columns:
                    new_value = update_row()[column]

                    if new_value and not db_row.__getattribute__(column) == new_value:
                        db_row.__setattr__(column, new_value)

        return db_row

    @staticmethod
    def new(data):
        return None

    @staticmethod
    def get(data):
        return None


class Game(HiddenFF, Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True)
    week = Column(Integer)
    start = Column(DateTime, nullable=False)
    length = Column(Integer)
    stadium = Column(String(255), nullable=False)
    roof = Column(Boolean)
    surface = Column(String(255))

    team_games = relationship('TeamGame', back_populates='game')

    @staticmethod
    def update_from_scraped(scraped_data):
        db_game = Game.update(scraped_data)

        def parse_spread():
            split_text = scraped_data['spread'].rsplit(' ', 1)
            return split_text[0], float(split_text[1])

        favorite, spread = parse_spread()

        over_under = float(scraped_data['over_under'].split(' ', 1)[0])
        split_total = over_under / 2

        def parse_team_games():
            def parse_data(scraped_team_game):
                team = team_keys[scraped_team_game['team']]

                is_favorite = team == team_keys[favorite]

                def get_handicap():
                    return spread if is_favorite else spread * -1

                handicap = get_handicap()

                def get_total():
                    return split_total - (handicap / 2)

                team_game = {
                    'team': team,
                    'score': scraped_team_game['score'],
                    'handicap': get_handicap(),
                    'total': get_total(),
                    'snaps': scraped_team_game['snaps'],
                    'game_id': db_game.id,
                    'week': db_game.week
                }

                return team_game

            return [parse_data(game) for game in scraped_data['team_games']]

        for team_game in parse_team_games():
            db_game.team_games.append(TeamGame.update(team_game))

    @staticmethod
    def new(scraped_data):
        def parse_length():
            split_text = scraped_data['length'].split(':')
            timedelta = dt.timedelta(int(split_text[0]),
                                     int(split_text[1]))

            return timedelta.total_seconds()

        start = create_datetime(scraped_data['start'])
        length = parse_length()

        return Game(week=scraped_data['week'],
                    start=start,
                    length=length,
                    stadium=scraped_data['stadium'],
                    roof=roof_keys[scraped_data['roof']],
                    surface=scraped_data['surface'])

    @staticmethod
    def get(scraped_data):
        game = session.query(Game).filter_by(stadium=scraped_data['stadium'],
                                             start=scraped_data['start']).first()

        return game


class Player(HiddenFF, Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True)
    first = Column(String(32), nullable=False)
    last = Column(String(32), nullable=False)
    position = Column(String(2))
    team = Column(String(3))
    birthday = Column(Date)

    player_games = relationship('PlayerGame', back_populates='player')

    def __repr__(self):
        return '%s %s (%s): %s' % (self.first, self.last, self.position, self.team)

    modifiable_columns = {'position', 'team'}

    @staticmethod
    def update_from_scraped(scraped_data):
        team = team_keys[scraped_data['team']]

        scraped_data.update({'team': team})

        db_player = Player.update(scraped_data)

        for game in scraped_data.get('games'):
            team = team_keys[game['team']]

            game.update({'player_id': db_player.id,
                         'team': team})

            db_player_game = PlayerGame.update(game)
            db_player.player_games.append(db_player_game)
            db_team_game = TeamGame.get({'team': game['team'],
                                         'week': game['week']})

            db_team_game.player_games.append(db_player_game)

    @staticmethod
    def new(data):
        player = Player(first=data['first'],
                        last=data['last'],
                        position=data['position'],
                        team=data['team'],
                        birthday=create_date(data['birthday']))

        return player

    @staticmethod
    def get(data):
        player = session.query(Player).filter_by(first=data['first'],
                                                 last=data['last'],
                                                 birthday=data['birthday']).first()

        return player


class TeamGame(HiddenFF, Base):
    __tablename__ = 'team_games'

    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey('games.id'))
    team = Column(String(3), nullable=False)
    score = Column(Integer)
    handicap = Column(Float)
    total = Column(Float)
    snaps = Column(Integer)

    game = relationship('Game', back_populates='team_games')
    player_games = relationship('PlayerGame', back_populates='team_game')

    modifiable_columns = {'score', 'handicap', 'total', 'snaps'}

    @staticmethod
    def new(data):
        game = TeamGame(team=data['team'],
                        score=data['score'],
                        handicap=data['handicap'],
                        total=data['total'],
                        snaps=data['snaps'])

        return game

    @staticmethod
    def get(data):
        game = session.query(TeamGame).filter_by(team=data['team']).\
            join(TeamGame.game).filter_by(week=data['week']).first()

        return game

    def get_week(self):
        return self.game.week


class PlayerGame(HiddenFF, Base):
    __tablename__ = 'player_games'

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('players.id'))
    team_game_id = Column(Integer, ForeignKey('team_games.id'))

    rush_att = Column(Integer, nullable=False)
    rush_yd = Column(Integer, nullable=False)
    rush_td = Column(Integer, nullable=False)

    tgt = Column(Integer, nullable=False)
    rec = Column(Integer, nullable=False)
    rec_yd = Column(Integer, nullable=False)
    rec_td = Column(Integer, nullable=False)

    pass_att = Column(Integer, nullable=False)
    pass_cmp = Column(Integer, nullable=False)
    pass_yd = Column(Integer, nullable=False)
    pass_td = Column(Integer, nullable=False)

    fum = Column(Integer, nullable=False)
    int = Column(Integer, nullable=False)
    sacked = Column(Integer, nullable=False)
    snaps = Column(Integer, nullable=False)

    player = relationship('Player', back_populates='player_games')
    team_game = relationship('TeamGame', back_populates='player_games')

    modifiable_columns = {
        'team',
        'rush_att', 'rush_yd', 'rush_td', 'fum',
        'tgt', 'rec', 'rec_yd', 'rec_td',
        'pass_att', 'pass_cmp', 'pass_yd', 'pass_td',
        'fum', 'int', 'sacked', 'snaps'
    }

    @staticmethod
    def new(data):
        def check_stat(stat):
            scraped_stat = data[stat]
            return scraped_stat if scraped_stat else '0'

        game = PlayerGame(rush_att=check_stat('rush_att'),
                          rush_yd=check_stat('rush_yd'),
                          rush_td=check_stat('rush_td'),
                          tgt=check_stat('tgt'),
                          rec=check_stat('rec'),
                          rec_yd=check_stat('rec_yd'),
                          rec_td=check_stat('rec_td'),
                          pass_att=check_stat('pass_att'),
                          pass_cmp=check_stat('pass_cmp'),
                          pass_yd=check_stat('pass_yd'),
                          pass_td=check_stat('pass_td'),
                          fum=check_stat('fum'),
                          int=check_stat('int'),
                          sacked=check_stat('sacked'),
                          snaps=data['snaps'])

        return game

    @staticmethod
    def get(data):
        game = session.query(PlayerGame).filter_by(player_id=data['player_id'])\
            .join(PlayerGame.team_game)\
            .join(TeamGame.game, aliased=True, from_joinpoint=True).filter_by(week=data['week']).first()

        return game

    def get_week(self):
        return self.team_game.game.week

    def get_team(self):
        return self.team_game.team


# Utilities
def reset_tables():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
