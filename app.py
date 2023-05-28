from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
from spell import Spell, spellize
from scrape_data import scrape_class, scrape_spell

CLASS = "Paladin"
spell_cache = {}

app = Flask(__name__)

@app.route('/')
def index(class_name = "DND"):
	return render_template("spell_table.html", title=f'{class_name} Spells', spells = [], show = 0)

@app.route('/class/<class_name>', methods=['GET'])
def class_spells(class_name):
	spells = spellize(scrape_class(class_name.lower()))
	if class_name in ["Paladin", "Ranger"]:
		show = 1
	else:
		show = 2
	return render_template("spell_table.html", title=f'{class_name} Spells', spells = spells, show = show)

@app.route('/spell/<spell_name>', methods=['GET'])
def spell(spell_name):
	if spell_name in spell_cache:
		content = spell_cache[spell_name]
	else:
		content = scrape_spell(spell_name)
		spell_cache[spell_name] = content
	return content
