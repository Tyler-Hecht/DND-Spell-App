from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
from spell import Spell, spellize
from scrape_data import scrape_class, scrape_spell

CLASS = "paladin"
spell_cache = {}

app = Flask(__name__)
spells = spellize(scrape_class(CLASS))

@app.route('/')
def index(spells = spells):
	return render_template("spell_table.html", title='Paladin Spells', spells = spells)

@app.route('/spell/<spell_name>', methods=['GET'])
def spell(spell_name):
	if spell_name in spell_cache:
		content = spell_cache[spell_name]
	else:
		content = str(scrape_spell(spell_name))
		spell_cache[spell_name] = content
	return content

