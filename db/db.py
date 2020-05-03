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
    team = Column(String(50))
    birthday = Column(Date)

    player_games = relationship('PlayerGame', back_populates='player')

    def __repr__(self):
        return '%s %s (%s): %s' % (self.first, self.last, self.position, self.team)

    modifiable_columns = {'position', 'team'}

    @classmethod
    def update(cls, data):
        db_player = super().update(data)

        for game in data.get('games'):
            game['player_id'] = db_player.id
            db_game = PlayerGame.update(game)
            db_player.player_games.append(db_game)

    @staticmethod
    def new(data):
        player = Player(first=data['first'],
                        last=data['last'],
                        position=data['position'],
                        team=team_keys[data['team']],
                        birthday=create_date(data['birthday']))

        return player

    @staticmethod
    def get(data):
        player = session.query(Player).filter_by(first=data['first'],
                                                 last=data['last'],
                                                 birthday=data['birthday']).first()

        return player


class PlayerGame(HiddenFF, Base):
    __tablename__ = 'player_games'

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('players.id'))
    week = Column(Integer, nullable=False)
    team = Column(String(3), nullable=False)

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

        game = PlayerGame(week=data['week'],
                          team=team_keys[data['team']],
                          rush_att=check_stat('rush_att'),
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
                          snaps=data['snaps']
                          )

        return game

    @staticmethod
    def get(data):
        game = session.query(PlayerGame).filter_by(player_id=data['player_id'],
                                                   week=data['week']).first()

        return game


# Utilities
def reset_tables():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
