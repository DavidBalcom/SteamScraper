

from SteamScraper import *
from sqlalchemy.exc import IntegrityError
import requests

SECOND_KEY = '22222222222222222222222222222222'

ss = SteamScraper(SECOND_KEY)

node_level = ss.getMinNodeLevel()

while True:

	try:
		ss.updateUser(node_level, number_of_mods=2, match_mod_number=1)
	except NoResultFound:
		print "NoResultFound. Updating min node level"
		node_level = ss.getMinNodeLevel()
	except IntegrityError:
		print "integrity error"
	except requests.exceptions.ConnectionError:
		print "connection error"