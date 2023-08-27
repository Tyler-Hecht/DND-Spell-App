# DND Spell App

This is a webapp that displays spells for a given DND class\
The spells can be searched by name and filtered by level, casting time, etc.\
Clicking on a spell shows its description\
You can include other spells in your list by clicking on the book on the main page\
Add individual spells by link (dnd5e.wikidot.com) or upload a txt file with a list of spells links (one per line)\
Spell links with # at the beginning are ignored\

Currently, four classes are supported\
More features are being added

## Running

1. Install [Python](https://www.python.org/downloads/) with [pip](https://pip.pypa.io/en/stable/installation/)
2. Install Flask with `pip install flask`
3. Start the app by running the .bat file or entering `flask run` in the terminal
4. In a browser, go to `localhost:2000`

Uncomment the line in the .env file to join with devices on the same network\
The steps described above are meant for Windows, but similar steps can be followed for Mac
