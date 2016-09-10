

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import Column
from sqlalchemy import BigInteger, Integer, DateTime
import datetime
from config import *
from sqlalchemy import create_engine


Base = declarative_base()


class SteamUsers(Base):
	__tablename__ = 'SteamUsers'
	# steam_id = Column(BigInteger, primary_key=True, index=True)  # probably don't want index, need to test
	steam_id = Column(BigInteger, primary_key=True)
	node_level = Column(Integer)
	insert_time = Column(DateTime(timezone=True), default=datetime.datetime.now)
	update_time = Column(DateTime(timezone=True))

class UsersGamesStats(Base):
	__tablename__ = 'UsersGamesStats'
	# pkey = Column(BigInteger)
	steam_id = Column(BigInteger, primary_key=True)
	game_id = Column(Integer, primary_key=True)
	playtime_2weeks = Column(Integer)
	playtime_forever = Column(Integer)
	update_time = Column(DateTime(timezone=True), default=datetime.datetime.now)


# run this script to create database
if __name__ == '__main__':
	eng = create_engine(CON_STRING, echo=True)
	Base.metadata.create_all(eng)
