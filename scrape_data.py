import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd

def scrape_class(class_name):
    url = f"http://dnd5e.wikidot.com/spells:{class_name}"
    properties = ["Spell Name", "School", "Casting Time", "Range", "Duration", "Components"]

    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    spells = []

    # get list of li tags in ul tag with class "yui-nav"
    spell_levels = soup.find("ul", {"class": "yui-nav"}).find_all("li")
    # get list of spell names
    spell_levels = [spell_level.text for spell_level in spell_levels]

    for tab in range(len(soup.find_all("div", {"id": lambda x: x and "wiki-tab-0-" in x}))):
        spell_list = soup.find_all("div", {"id": f"wiki-tab-0-{tab}"})
        spell_names = spell_list[0].find_all("a")
        spell_names.insert(0, "properties")
        first = True
        for name, spell in zip(spell_names, spell_list[0].find_all("tr")):
            if first:
                first = False
                continue
            name = name.text
            info = {}

            for property, data in zip(properties, spell.find_all("td")):
                if "Feet" in data.text:
                    info[property] = data.text.lower()
                elif "Days" in data.text:
                    info[property] = data.text.replace("Days", "days")
                elif "action" in data.text:
                    info[property] = data.text.replace("action", "Action")
                else:
                    info[property] = data.text

            # if name is Melf's Minute Meteors, casting time is 1 Action and range is Self
            if name == "Melf's Minute Meteors":
                info["Casting Time"] = "1 Action"
                info["Range"] = "Self"
            
            level = spell_levels[tab]
            if level != "Cantrip":
                level = level[0]
            else:
                level = 0
            info["Level"] = level

            if info["Casting Time"][-2:] == " R":
                info["Casting Time"] = info["Casting Time"][:-2]
            if info["School"][-2:] == " R":
                info["School"] = info["School"][:-2]

            spells.append(info)

    df = pd.DataFrame(spells)
    # make level the first column
    cols = df.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    df = df[cols]
    return df

def scrape_spell(spell_name):
    # make sure spell name is lowercase and has no spaces
    spell_name2 = spell_name.lower().replace(" ", "-").replace("'", "").replace(":", "").replace("-(ua)", "").replace("-(hb)", "")
    url = f"http://dnd5e.wikidot.com/spell:{spell_name2}"
    
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")

    # get div with id "page-content"
    content = soup.find("div", {"id": "page-content"})
    # remove the last <p> tag
    content.find_all("p")[-1].decompose()

    # add spell name to the top of the page
    content.insert(0, soup.new_tag("h3"))
    content.h3.string = spell_name

    # make all hyperlinks into normal text (no longer clickable)
    for link in content.find_all("a"):
        link.replaceWithChildren()

    return str(content)
