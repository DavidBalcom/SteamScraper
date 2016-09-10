

from SteamScraper import *
from sqlalchemy.exc import IntegrityError
import requests

API_KEY = '1111111111111111111111111111'

ss = SteamScraper(API_KEY)

node_level = ss.getMinNodeLevel()

while True:

	try:
		ss.updateUser(node_level, number_of_mods=2, match_mod_number=0)
	except NoResultFound:
		print "NoResultFound. Updating min node level"
		node_level = ss.getMinNodeLevel()
	except IntegrityError:
		print "integrity error"
	except requests.exceptions.ConnectionError:
		print "connection error"