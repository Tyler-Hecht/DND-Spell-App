# this file is not needed if the scraped data is already saved in a file

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

            # special cases, often due to inconsistent formatting
            for property, data in zip(properties, spell.find_all("td")):
                if "Feet" in data.text and property == "Range":
                    info[property] = data.text.lower()
                elif "ft" in data.text and property == "Range":
                    info[property] = data.text.replace("ft", " feet")
                elif "Days" in data.text and property == "Duration":
                    info[property] = data.text.replace("Days", "days")
                elif data.text == "Reaction" and property == "Casting Time":
                    info[property] = "1 Reaction"
                elif "action" in data.text and "reaction" not in data.text.lower() and property == "Casting Time":
                    info[property] = data.text.replace("action", "Action")
                elif data.text == "15-foot cone" and property == "Range":
                    info[property] = "Self (15-foot cone)"
                else: # normal case
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

            for property in properties:
                if info[property][-2:] in [" R", " T"]:
                    info[property] = info[property][:-2]

            spells.append(info)

    df = pd.DataFrame(spells)
    # make level the first column
    cols = df.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    df = df[cols]
    return df

def scrape_spell(spell_name):
    print(spell_name)
    spell_name2 = spell_name
    if spell_name == "Icingdeath's Frost (UA)": # special case
        spell_name2 = spell_name.lower().replace("'", "-")
    spell_name2 = spell_name2.lower().replace(" ", "-").replace("'", "").replace(":", "").replace("-(ua)", "").replace("-(hb)", "").replace("/", "-")
    if spell_name2 in ["antagonize", "house-of-cards", "guiding-hand"]: # special cases
        spell_name2 += "-ua"
    url = f"http://dnd5e.wikidot.com/spell:{spell_name2}"
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")

    # get div with id "page-content"
    content = soup.find("div", {"id": "page-content"})
    # remove the last <p> tag
    content.find_all("p")[-1].decompose()

    # make all hyperlinks into normal text (no longer clickable)
    for link in content.find_all("a"):
        link.replaceWithChildren()
    
    return str(content)
