from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
from spell import Spell, spellize
from scrape_data import scrape_data

CLASS = "paladin"

app = Flask(__name__)
spells = spellize(scrape_data(CLASS))

@app.route('/')
def index(spells = spells):
	return render_template("spell_table.html", title='Paladin Spells', spells = spells)



