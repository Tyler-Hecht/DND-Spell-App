from flask import Flask, render_template, request
from spell import spellize, spell_to_dict, filter_spells
from scrape_data import scrape_class
import pickle

'''
Uncomment this section to scrape new data (bs4, urllib, and pandas required)
'''
# scraped_data = {
#     "Paladin": {},
#     "Sorcerer": {},
#     "Bard": {}
# }
# for class_name in scraped_data:
# 	spell_list = spellize(scrape_class(class_name))
# 	for spell in spell_list:
# 		scraped_data[class_name][spell.name] = spell
# save scraped data to file
# with open('scraped_data.pkl', 'wb') as f:
# 	pickle.dump(scraped_data, f)

# load scraped data from file
with open('scraped_data.pkl', 'rb') as f:
	scraped_data = pickle.load(f)
print("Starting app")
print("Spell data loaded")
print("Connect to http://localhost:20 or an address listed below")
print()

config = {
	"query": None,
	"name only": True,
	"class": None,
	"show": 0,
	"levels": [],
	"school": None,
	"casting_time": None,
	"range": None,
	"duration": None,
	"concentration": None,
	"components": None
}

def lighten(hex_color):
	hex_color = hex_color.lstrip('#')
	rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
	new_rgb = tuple([int((255 - rgb[i]) / 2 + rgb[i]) for i in range(3)])
	return '#%02x%02x%02x' % new_rgb

def updateTable(config, scraped_data):
	if config["class"] is not None:
		spells = scraped_data[config["class"]]
		spells = filter_spells(config, spells)
		spells_data = [spell_to_dict(spell) for spell in spells]
		return render_template('spell_table.html', spells=spells_data, show=config["show"])
	else:
		return render_template('spell_table.html', spells=[], show=0, header_color = "#ffffff")

app = Flask(__name__)

@app.route('/')
def index():
	# reset config
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
	return render_template("blocks.html")

@app.route('/spell/<spell_name>', methods=['GET'])
def spell(spell_name):
	content = scraped_data[config["class"]][spell_name].description
	return content

@app.route('/class/<class_name>', methods=['GET'])
def class_spells(class_name):
	if class_name == "Select Class":
		config["class"] = None
		return "", 200
	config["class"] = class_name
	if class_name in ["Paladin", "Ranger"]:
		config["show"] = 1
	else:
		config["show"] = 2
	return updateTable(config, scraped_data)

@app.route('/search', methods=['POST'])
def search():
	config["query"] = request.form["query"]
	return updateTable(config, scraped_data)

@app.route('/levelSearch', methods=['POST'])
def levelSearch():
	levels = request.form
	config["levels"] = []
	for level in levels:
		if levels[level] == "true":
			level_num = level[5:]
			config["levels"].append(int(level_num))
	return updateTable(config, scraped_data)

@app.route('/schoolSearch', methods=['POST'])
def schoolSearch():
	if request.form["school"] != "School":
		config["school"] = request.form["school"]
	else:
		config["school"] = None
	return updateTable(config, scraped_data)

@app.route('/castingTimeSearch', methods=['POST'])
def castingTimeSearch():
	if request.form["castingTime"] != "Casting Time":
		config["casting_time"] = request.form["castingTime"]
	else:
		config["casting_time"] = None
	return updateTable(config, scraped_data)

@app.route('/rangeSearch', methods=['POST'])
def rangeSearch():
	if request.form["range"] != "Range":
		config["range"] = request.form["range"]
	else:
		config["range"] = None
	return updateTable(config, scraped_data)

@app.route('/durationSearch', methods=['POST'])
def durationSearch():
	if request.form["duration"] != "Duration":
		config["duration"] = request.form["duration"]
	else:
		config["duration"] = None
	return updateTable(config, scraped_data)

@app.route('/componentsSearch', methods=['POST'])
def componentsSearch():
	if request.form["components"] != "Components":
		config["components"] = request.form["components"]
	else:
		config["components"] = None
	return updateTable(config, scraped_data)

@app.route('/concentrationSearch', methods=['POST'])
def concentrationSearch():
	if request.form["concentration"] != "Concentration":
		config["concentration"] = request.form["concentration"]
	else:
		config["concentration"] = None
	return updateTable(config, scraped_data)
