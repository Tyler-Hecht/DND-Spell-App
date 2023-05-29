from flask import Flask, render_template, request
from spell import spellize, spell_to_dict, filter_spells
from scrape_data import scrape_class, scrape_spell

CLASS = "Paladin"
spell_cache = {}
spell_list_cache = {}
config = {
	"query": None,
    "class": None,
    "show": 0,
    "levels": [],
    "school": None,
    "casting_time": None,
    "range": None
}

def updateTable(config, spell_list_cache):
	if config["class"] is not None:
		spells = spell_list_cache[config["class"]]
		spells = filter_spells(config, spells)
		spells_data = [spell_to_dict(spell) for spell in spells]
		return render_template('spell_table.html', spells=spells_data, show=config["show"])
	else:
		return render_template('spell_table.html', spells=[], show=0)

app = Flask(__name__)

@app.route('/')
def index():
	return render_template("blocks.html")

@app.route('/class/<class_name>', methods=['GET'])
def class_spells(class_name):
	if class_name == "Select Class":
		config["class"] = None
		return "", 200
	config["class"] = class_name
	if class_name in spell_list_cache:
		spells = spell_list_cache[class_name]
	else:
		spells = spellize(scrape_class(class_name.lower()))
		spell_list_cache[class_name] = spells
	spells_data = [spell_to_dict(spell) for spell in spells]
	if class_name in ["Paladin", "Ranger"]:
		config["show"] = 1
	else:
		config["show"] = 2
	return updateTable(config, spell_list_cache)

@app.route('/search', methods=['POST'])
def search():
	config["query"] = request.form["query"]
	return updateTable(config, spell_list_cache)

@app.route('/levelSearch', methods=['POST'])
def levelSearch():
	levels = request.form
	config["levels"] = []
	for level in levels:
		if levels[level] == "true":
			level_num = level[5:]
			config["levels"].append(int(level_num))
	return updateTable(config, spell_list_cache)

@app.route('/schoolSearch', methods=['POST'])
def schoolSearch():
	if request.form["school"] != "School":
		config["school"] = request.form["school"]
	else:
		config["school"] = None
	return updateTable(config, spell_list_cache)

@app.route('/castingTimeSearch', methods=['POST'])
def castingTimeSearch():
	if request.form["castingTime"] != "Casting Time":
		config["casting_time"] = request.form["castingTime"]
	else:
		config["casting_time"] = None
	return updateTable(config, spell_list_cache)

@app.route('/rangeSearch', methods=['POST'])
def rangeSearch():
	if request.form["range"] != "Range":
		config["range"] = request.form["range"]
	else:
		config["range"] = None
	return updateTable(config, spell_list_cache)

@app.route('/spell/<spell_name>', methods=['GET'])
def spell(spell_name):
	if spell_name in spell_cache:
		content = spell_cache[spell_name]
	else:
		content = scrape_spell(spell_name)
	spell_cache[spell_name] = content
	return content
