
import requests
from config import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from sqlalchemy import exists
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
from models import *
import datetime

import pdb


class SteamScraper(object):
	"""
	base class with functions to pull data from the Steam API

	"""
	def __init__(self, API_KEY):
		self.API_KEY = API_KEY
		self.eng = create_engine(CON_STRING, echo=False)
		Session = sessionmaker(bind=self.eng)
		self.session = Session()



	def getWorkerSteamId(self, number_of_mods=2, match_mod_number=0):
		""" get steam id with lowest node level that hasnt been updated """
		return self.session.query(SteamUsers.steam_id)\
			.filter(SteamUsers.update_time == None)\
			.filter(func.mod(SteamUsers.steam_id, number_of_mods) == match_mod_number)\
			.order_by(SteamUsers.node_level).limit(1).one()[0]




	def getMinNodeLevel(self):
		""" get min node level""" 
		return self.session.query(func.min(SteamUsers.node_level)).filter(SteamUsers.update_time == None).one()[0]
	


	def setUpdateTimeForUser(self, steam_id):
		self.session.query(SteamUsers).filter(SteamUsers.steam_id == int(steam_id)).update({"update_time": datetime.datetime.now()})
		self.session.commit()



	def getFriendsListForUser(self, steam_id):
		""" return friends list for given steam user """

		steam_id = str(steam_id)

		url = 'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={self.API_KEY}&steamid={steam_id}&relationship=friend'.format(**locals())

		response = requests.get(url)
		response = response.json()

		friendslist = response['friendslist']['friends']

		return [int(friend['steamid']) for friend in friendslist]


	
	def insertNewSteamUsers(self, friendslist, node_level):
		""" insert list of friends into DB
		"""

		for friend in friendslist:  # friend is an integer steam ID

			self.session.merge(SteamUsers(steam_id=friend, node_level=node_level))

		self.session.commit()



	def _returnUserGameStatObject(self, steam_id, game):
		""" helper function to create UserGameStat object from json response """
		
		try:
			playtime_2weeks = int(game['playtime_2weeks'])
		except KeyError:
			playtime_2weeks = None

		return UsersGamesStats(steam_id=int(steam_id), game_id=int(game['appid']), playtime_2weeks=playtime_2weeks, playtime_forever=int(game['playtime_forever']))		



	def getGameStats(self, steam_id):
		""" get games stats for given steam user, then insert into DB """

		steam_id = str(steam_id)
		
		url = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={self.API_KEY}&steamid={steam_id}&format=json'.format(**locals())

		response = requests.get(url)
		response = response.json()

		gameList = response['response']['games']

		objList = [self._returnUserGameStatObject(steam_id, game) for game in gameList]

		self.session.add_all(objList)
		self.session.commit()



	def startWithFirstUser(self, API_KEY, FIRST_STEAM_ID):

		self = SteamScraper(API_KEY)

		# add first user to user database
		self.session.add(SteamUsers(steam_id=FIRST_STEAM_ID, node_level=0))
		self.session.commit()

		friendList = self.getFriendsListForUser(FIRST_STEAM_ID)

		self.insertNewSteamUsers(friendList, 1)

		self.getGameStats(FIRST_STEAM_ID)

		self.setUpdateTimeForUser(FIRST_STEAM_ID)



	def updateUser(self, node_level, number_of_mods, match_mod_number):
		""" update data for a steam user 


		"""

		# slow af
		# node_level = self.getMinNodeLevel()

		node_level += 1

		steam_id = self.getWorkerSteamId(number_of_mods, match_mod_number)
		print "doing "+str(steam_id)

		# get steam user's friends
		try:
			self.insertNewSteamUsers(self.getFriendsListForUser(steam_id), node_level)
		except KeyError:
			self.setUpdateTimeForUser(steam_id)
			print str(steam_id)+" has no friends list"
			
		# get game data for steam user
		try:
			self.getGameStats(steam_id)
		except KeyError:
			self.setUpdateTimeForUser(steam_id)
			print str(steam_id)+" has no games"

		self.setUpdateTimeForUser(steam_id)

