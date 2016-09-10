# SteamScraper

These are some scripts that can be used for pulling data about game play time from the steam API. The project was inspired by SteamSpy.com. Instead of taking a random sample of users though, this script starts with a single user and then looks at all of their friends, and then looks at all of their friends' friends, and so on. 

It's written to use two API keys simultaneously to go beyond the 100,000 daily API call limit for the Steam API. It can be easily edited to use more API keys (and less easily edited to use only one API key).

The data can be used to draw conclusions about usage habits for different games.

TODO:
* add exponential backoff if the API call fails
* test indexes vs no indexes
* test optimal number of API keys to be using simultaneously

## Installation and Requirements

Clone repo to your server or whatever. This requires sqlalchemy, requests, and whichever database API you're using.

## Usage

1. Create Database
2. Edit config file with your settings
3. Run models.py to create tables
4. Edit startWithThis.py with your API Key and the target user who you want to start with, then run it.
5. Edit firstKey.py with your API Key, and run it. It will continue to pull data as long as it's running. Change number\_of\_mods and match\_mod\_number depending on how many different keys you have
6. Optional - edit and run secondKey.py with a second key and different mod numbers. Do this for as many files as you have keys to use. 
7. you can restart firstKey.py anytime and it will pick up where it left off. 


## Contributing

standard forking instructions:

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D


## License

TODO: Write license