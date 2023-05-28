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
                else:
                    info[property] = data.text
            info["Level"] = tab + 1

            if info["Casting Time"] == "1 Action R":
                info["Casting Time"] = "1 Action"
            if " T" in info["School"]:
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
    spell_name = spell_name.lower().replace(" ", "-")
    url = f"http://dnd5e.wikidot.com/spell:{spell_name}"
    
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")

    # get div with id "page-content"
    content = soup.find("div", {"id": "page-content"})
    # remove the last <p> tag
    content.find_all("p")[-1].decompose()

    return str(content)
