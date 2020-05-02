from utility import team_keys, roof_keys, create_datetime, create_date

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Date, Time, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

import os
import datetime as dt


uri = os.getenv('DATABASE_URI')
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
    birthday = Column(Date)

    player_games = relationship('PlayerGame', back_populates='player')

    def __repr__(self):
        return '%s %s (%s): %s' % (self.first, self.last, self.position, self.team)

    modifiable_columns = {'position', 'team'}

    @staticmethod
    def update(player_data):
        db_player = Player.get(player_data)

        if not db_player:
            db_player = Player.new(player_data)
            session.add(db_player)
        else:
            update_row(db_player, player_data)

        for game in player_data.get('games'):
            db_player.update_game(game)

    def update_game(self, game_data):
        week = game_data.get('week')

        if week:
            db_game = PlayerGame.get(self.id, week)

            if not db_game:
                db_game = (PlayerGame.new(game_data))
                self.player_games.append(db_game)
            else:
                update_row(db_game, game_data)

    @staticmethod
    def new(player_data):
        player = Player(first=player_data['first'],
                        last=player_data['last'],
                        position=player_data['position'],
                        team=team_keys[player_data['team']],
                        birthday=create_date(player_data['birthday']))

        return player

    @staticmethod
    def get(player_data):
        player = session.query(Player).filter_by(first=player_data['first'],
                                                 last=player_data['last'],
                                                 birthday=player_data['birthday']).first()

        return player


class PlayerGame(Base):
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
    def new(game_data):
        def check_stat(stat):
            scraped_stat = game_data[stat]
            return scraped_stat if scraped_stat else '0'

        game = PlayerGame(week=game_data['week'],
                          team=team_keys[game_data['team']],
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
                          snaps=game_data['snaps']
                          )

        return game

    @staticmethod
    def get(player_id, week):
        game = session.query(PlayerGame).filter_by(player_id=player_id,
                                                   week=week).first()

        return game


class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True)
    week = Column(Integer)
    start = Column(DateTime, nullable=False)
    length = Column(Integer)
    stadium = Column(String(255), nullable=False)
    roof = Column(Boolean)
    surface = Column(String(255))

    @staticmethod
    def new(game_data):
        def parse_length():
            split_text = game_data['length'].split(':')
            timedelta = dt.timedelta(int(split_text[0]),
                                     int(split_text[1]))

            return timedelta.total_seconds()

        start = create_datetime(game_data['start'])
        length = parse_length()

        return Game(week=game_data['week'],
                    start=start,
                    length=length,
                    stadium=game_data['stadium'],
                    roof=roof_keys[game_data['roof']],
                    surface=game_data['surface'])


def update_row(row, new_data):
    for column in row.modifiable_columns:
        new_value = new_data[column]

        if new_value and not row.__getattribute__(column) == new_value:
            row.__setattr__(column, new_value)


# Utilities
def reset_tables():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
