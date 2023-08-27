from flask import Flask, render_template, request
from spell import spell_to_dict, filter_spells
from scrape_data import scrape_class, scrape_spell
import pickle

def scrape_new_data():
	scraped_data = {
		"Paladin": {},
		"Sorcerer": {},
		"Bard": {},
		"Wizard": {}
	}
	print("Scraping data...")
	for class_name in scraped_data:
		spell_list = [scrape_spell(spell_url) for spell_url in scrape_class(class_name)]
		for spell in spell_list:
			scraped_data[class_name][spell.name] = spell
	with open('scraped_data.pkl', 'wb') as f:
		pickle.dump(scraped_data, f)
# Uncomment this to scrape new data (bs4, urllib, and pandas required)
# scrape_new_data()

# load scraped data from file
with open('scraped_data.pkl', 'rb') as f:
	scraped_data = pickle.load(f)
	scraped_data["Custom"] = {}
added_spells = {}

print("Starting app")
print("Spell data loaded")
print("Connect to http://localhost:2000 or an address listed below")
print()

def reset_config(config):
	config["query"] = None
	config["name only"] = True
	config["class"] = None
	config["show"] = 0
	config["levels"] = []
	config["school"] = None
	config["casting_time"] = None
	config["range"] = None
	config["duration"] = None
	config["concentration"] = None
	config["components"] = None
	config["source"] = {
		"phb": True,
		"xge": True,
		"tce": False,
		"ua": False,
		"other": False
	}

config = {}
reset_config(config)

def lighten(hex_color):
	hex_color = hex_color.lstrip('#')
	rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
	new_rgb = tuple([int((255 - rgb[i]) / 2 + rgb[i]) for i in range(3)])
	return '#%02x%02x%02x' % new_rgb

def updateTable(config, scraped_data, added_spells):
	if config["class"] is not None:
		spells = scraped_data[config["class"]]
		spells = filter_spells(config, spells | added_spells)
		spells_data = [spell_to_dict(spell) for spell in spells]
		return render_template('spell_table.html', spells=spells_data, show=config["show"])
	else:
		return render_template('spell_table.html', spells=[], show=0, header_color = "#ffffff")

app = Flask(__name__)

@app.route('/')
def index():
	reset_config(config)
	return render_template("blocks.html")

@app.route('/updateTable', methods=['POST'])
def update():
	return updateTable(config, scraped_data, added_spells)

@app.route('/spell/<spell_name>', methods=['GET'])
def spell(spell_name):
	try:
		content = scraped_data[config["class"]][spell_name].description[0]
	except:
		content = added_spells[spell_name].description[0]
	return content

@app.route('/class/<class_name>', methods=['GET'])
def class_search(class_name):
	if class_name == "Select Class":
		config["class"] = None
		return "", 200
	config["class"] = class_name
	if class_name in ["Paladin", "Ranger"]:
		config["show"] = 1
	else:
		config["show"] = 2
	return updateTable(config, scraped_data, added_spells)

@app.route('/search', methods=['POST'])
def search():
	config["query"] = request.form["query"]
	return updateTable(config, scraped_data, added_spells)

@app.route('/nameOnly', methods=['POST'])
def nameOnly():
	config["name only"] = request.form["name-only"] == "true"
	return updateTable(config, scraped_data, added_spells)

@app.route('/levelSearch', methods=['POST'])
def levelSearch():
	levels = request.form
	config["levels"] = []
	for level in levels:
		if levels[level] == "true":
			level_num = level[5:]
			config["levels"].append(int(level_num))
	return updateTable(config, scraped_data, added_spells)

@app.route('/schoolSearch', methods=['POST'])
def schoolSearch():
	if request.form["school"] != "School":
		config["school"] = request.form["school"]
	else:
		config["school"] = None
	return updateTable(config, scraped_data, added_spells)

@app.route('/castingTimeSearch', methods=['POST'])
def castingTimeSearch():
	if request.form["castingTime"] != "Casting Time":
		config["casting_time"] = request.form["castingTime"]
	else:
		config["casting_time"] = None
	return updateTable(config, scraped_data, added_spells)

@app.route('/rangeSearch', methods=['POST'])
def rangeSearch():
	if request.form["range"] != "Range":
		config["range"] = request.form["range"]
	else:
		config["range"] = None
	return updateTable(config, scraped_data, added_spells)

@app.route('/durationSearch', methods=['POST'])
def durationSearch():
	if request.form["duration"] != "Duration":
		config["duration"] = request.form["duration"]
	else:
		config["duration"] = None
	return updateTable(config, scraped_data, added_spells)

@app.route('/componentsSearch', methods=['POST'])
def componentsSearch():
	if request.form["components"] != "Components":
		config["components"] = request.form["components"]
	else:
		config["components"] = None
	return updateTable(config, scraped_data, added_spells)

@app.route('/concentrationSearch', methods=['POST'])
def concentrationSearch():
	if request.form["concentration"] != "Concentration":
		config["concentration"] = request.form["concentration"]
	else:
		config["concentration"] = None
	return updateTable(config, scraped_data, added_spells)

@app.route('/sourceSearch', methods=['POST'])
def sourceSearch():
	sources = request.form
	for source in sources:
		config["source"][source] = sources[source] == "true"
	return updateTable(config, scraped_data, added_spells)

@app.route('/tryAddSpell', methods=['POST'])
def tryAddSpell():
	spell_link = request.form["spellLink"]
	# see if valid link
	try:
		spell = scrape_spell(spell_link)
		added_spells[spell.name] = spell
		return "Spell added", 200
	except:
		return "Invalid link", 200
	
@app.route('/resetAddedSpells', methods=['POST'])
def resetAllSpells():
	added_spells.clear()
	return "All added spells removed", 200

@app.route('/uploadSpells', methods=['POST'])
def uploadSpells():
	# read in form data
	file = request.files['file']
	# every line is a spell link
	any_added = False
	any_failed = False
	for line in file:
		spell_link = line.decode("utf-8")
		# if line begins with #, skip
		if spell_link[0] == "#":
			continue
		# see if valid link
		try:
			spell = scrape_spell(spell_link)
			added_spells[spell.name] = spell
			any_added = True
		except:
			any_failed = True
			print("Invalid link: " + spell_link)
	if any_failed and not any_added:
		return "All spells failed to add", 200
	elif any_failed:
		return "Some spells failed to add", 200
	elif any_added and not any_failed:
		return "All spells added", 200
	else:
		return "No spells in file", 200
if __name__ == '__main__':
	app.run(port = 2000)
