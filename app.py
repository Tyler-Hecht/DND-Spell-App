from flask import Flask, render_template, request, make_response
from spell import spell_to_dict, filter_spells
from scrape_data import scrape_class, scrape_spell
import uuid
import pickle

def scrape_new_data():
	classes = ["Paladin", "Sorcerer", "Bard", "Wizard"]
	scraped_data = {}
	print("Scraping data...")
	for class_name in classes:
		scraped_data[class_name] = {}
		spell_list = [scrape_spell(spell_url) for spell_url in scrape_class(class_name)]
		for spell in spell_list:
			scraped_data[class_name][spell.name] = spell
	with open('scraped_data.pkl', 'wb') as f:
		pickle.dump(scraped_data, f)
# Uncomment this to scrape new data (bs4 and urllib required)
# scrape_new_data()

# load scraped data from file
with open('data/scraped_data.pkl', 'rb') as f:
	scraped_data = pickle.load(f)
	scraped_data["Custom"] = {}
added_spells = {}

print("Starting app")
print("Spell data loaded")
print("Connect to http://localhost:2000 or an address listed below")
print()

def reset_config(config, user_id):
	if user_id not in config:
		config[user_id] = {}
	config[user_id]["query"] = None
	config[user_id]["name only"] = True
	config[user_id]["class"] = None
	config[user_id]["show"] = 0
	config[user_id]["levels"] = []
	config[user_id]["school"] = None
	config[user_id]["casting_time"] = None
	config[user_id]["range"] = None
	config[user_id]["duration"] = None
	config[user_id]["concentration"] = None
	config[user_id]["components"] = None
	config[user_id]["source"] = {
		"phb": True,
		"xge": True,
		"tce": False,
		"ua": False,
		"other": True
	}
	print(3)

config = {}

def lighten(hex_color):
	hex_color = hex_color.lstrip('#')
	rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
	new_rgb = tuple([int((255 - rgb[i]) / 2 + rgb[i]) for i in range(3)])
	return '#%02x%02x%02x' % new_rgb

def updateTable(config, scraped_data):
	# get added spells from cookie
	user_spells = added_spells[request.cookies["user_id"]]

	if config[request.cookies["user_id"]]["class"] is not None:
		spells = scraped_data[config[request.cookies["user_id"]]["class"]]
		spells = filter_spells(config[request.cookies["user_id"]], spells | user_spells)
		spells_data = [spell_to_dict(spell) for spell in spells]
		return render_template('spell_table.html', spells=spells_data, show=config[request.cookies["user_id"]]["show"])
	else:
		return render_template('spell_table.html', spells=[], show=0, header_color = "#ffffff")

app = Flask(__name__)

@app.route('/')
def index():
	# set cookie to track user
	resp = make_response(render_template("blocks.html"))
	if "user_id" not in request.cookies:
		user_id = str(uuid.uuid1())
		resp.set_cookie("user_id", user_id)
		print("New user: " + user_id)
		added_spells[user_id] = {}
		reset_config(config, user_id)
		return resp
	else:
		if request.cookies["user_id"] not in added_spells:
			added_spells[request.cookies["user_id"]] = {}
		user_id = request.cookies["user_id"]
		reset_config(config, user_id)
		return resp

@app.route('/updateTable', methods=['POST'])
def update():
	return updateTable(config, scraped_data)

@app.route('/spell/<spell_name>', methods=['GET'])
def spell(spell_name):
	try:
		content = scraped_data[config[request.cookies["user_id"]]["class"]][spell_name].description[0]
	except:
		content = added_spells[request.cookies["user_id"]][spell_name].description[0]
	return content

@app.route('/class/<class_name>', methods=['GET'])
def class_search(class_name):
	if class_name == "Select Class":
		config[request.cookies["user_id"]]["class"] = None
		return "", 200
	config[request.cookies["user_id"]]["class"] = class_name
	if class_name in ["Paladin", "Ranger"]:
		config[request.cookies["user_id"]]["show"] = 1
	else:
		config[request.cookies["user_id"]]["show"] = 2
	return updateTable(config, scraped_data)

@app.route('/search', methods=['POST'])
def search():
	config[request.cookies["user_id"]]["query"] = request.form["query"]
	return updateTable(config, scraped_data)

@app.route('/nameOnly', methods=['POST'])
def nameOnly():
	config[request.cookies["user_id"]]["name only"] = request.form["name-only"] == "true"
	return updateTable(config, scraped_data)

@app.route('/levelSearch', methods=['POST'])
def levelSearch():
	levels = request.form
	config[request.cookies["user_id"]]["levels"] = []
	for level in levels:
		if levels[level] == "true":
			level_num = level[5:]
			config[request.cookies["user_id"]]["levels"].append(int(level_num))
	return updateTable(config, scraped_data)

@app.route('/schoolSearch', methods=['POST'])
def schoolSearch():
	if request.form["school"] != "School":
		config[request.cookies["user_id"]]["school"] = request.form["school"]
	else:
		config[request.cookies["user_id"]]["school"] = None
	return updateTable(config, scraped_data)

@app.route('/castingTimeSearch', methods=['POST'])
def castingTimeSearch():
	if request.form["castingTime"] != "Casting Time":
		config[request.cookies["user_id"]]["casting_time"] = request.form["castingTime"]
	else:
		config[request.cookies["user_id"]]["casting_time"] = None
	return updateTable(config, scraped_data)

@app.route('/rangeSearch', methods=['POST'])
def rangeSearch():
	if request.form["range"] != "Range":
		config[request.cookies["user_id"]]["range"] = request.form["range"]
	else:
		config[request.cookies["user_id"]]["range"] = None
	return updateTable(config, scraped_data)

@app.route('/durationSearch', methods=['POST'])
def durationSearch():
	if request.form["duration"] != "Duration":
		config[request.cookies["user_id"]]["duration"] = request.form["duration"]
	else:
		config[request.cookies["user_id"]]["duration"] = None
	return updateTable(config, scraped_data)

@app.route('/componentsSearch', methods=['POST'])
def componentsSearch():
	if request.form["components"] != "Components":
		config[request.cookies["user_id"]]["components"] = request.form["components"]
	else:
		config[request.cookies["user_id"]]["components"] = None
	return updateTable(config, scraped_data)

@app.route('/concentrationSearch', methods=['POST'])
def concentrationSearch():
	if request.form["concentration"] != "Concentration":
		config[request.cookies["user_id"]]["concentration"] = request.form["concentration"]
	else:
		config[request.cookies["user_id"]]["concentration"] = None
	return updateTable(config, scraped_data)

@app.route('/sourceSearch', methods=['POST'])
def sourceSearch():
	sources = request.form
	for source in sources:
		config[request.cookies["user_id"]]["source"][source] = sources[source] == "true"
	return updateTable(config, scraped_data)

@app.route('/tryAddSpell', methods=['POST'])
def tryAddSpell():
	spell_link = request.form["spellLink"]
	# see if valid link
	try:
		spell = scrape_spell(spell_link)
		added_spells[request.cookies["user_id"]][spell.name] = spell
		return "Spell added", 200
	except:
		return "Invalid link", 200
	
@app.route('/resetAddedSpells', methods=['POST'])
def resetAllSpells():
	added_spells[request.cookies["user_id"]].clear()
	return "All added spells removed", 200

@app.route('/uploadSpells', methods=['POST'])
def uploadSpells():
	# read in form data
	file = request.files['file']
	# every line is a spell link
	any_added = False
	any_failed = False
	for line in file:
		spell_link = line.decode("utf-8").strip()
		# remove everything after #
		if "#" in spell_link:
			spell_link = spell_link[:spell_link.index("#")].strip()
		# or if empty line, skip
		if spell_link == "":
			continue
		# see if valid link
		try:
			spell = scrape_spell(spell_link)
			added_spells[request.cookies["user_id"]][spell.name] = spell
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
