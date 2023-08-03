from bs4 import BeautifulSoup
import re

class Spell:
    def __init__(self, name, description):
        self.description = (str(description), str(description).replace("Source:", "").replace("Casting Time:", "").replace("Range:", "").replace("Components:", "").replace("Duration:", ""))
        self.level = scrape_property(description, "Level")
        self.name = name
        self.school = scrape_property(description, "School")
        self.casting_time = scrape_property(description, "Casting Time")
        self.range = scrape_property(description, "Range")
        self.duration = scrape_property(description, "Duration")
        self.components = scrape_property(description, "Components")
        self.source = scrape_property(description, "Source")

def spell_to_dict(spell):
    return {
        "level": spell.level,
        "name": spell.name,
        "school": spell.school,
        "casting_time": spell.casting_time,
        "range": spell.range,
        "duration": spell.duration,
        "components": spell.components,
        "description": spell.description
    }

def filter_spells(config, spell_dict):
    if config["class"] in ["Paladin", "Ranger"]:
        # remove 0, 6, 7, 8, 9 (these are not paladin/ranger spell levels)
        tmp_levels = [level for level in config["levels"] if level not in [0, 6, 7, 8, 9]]
    else:
        tmp_levels = config["levels"]
        
    spells = []
    for spell in spell_dict.values():
        if config["query"] is not None:
            if config["name only"]:
                if config["query"].lower() not in spell.name.lower():
                    continue
            else:
                if config["query"].lower() not in spell.name.lower() and config["query"].lower() not in spell.description[1].lower():
                    continue
        if tmp_levels != []:
            if int(spell.level) not in tmp_levels:
                continue
        if config["school"] is not None:
            if config["school"].lower() != spell.school.lower():
                continue
        if config["casting_time"] is not None:
            if config["casting_time"] != spell.casting_time.lower():
                continue
        if config["range"] is not None:
            if spell.range in ["Self", "Touch"]:
                if config["range"].lower() != spell.range.lower():
                    continue
            elif "Self" in spell.range:
                if config["range"] != "Self (aoe)":
                    continue
            elif spell.range in ["Sight", "Unlimited", "Special"]:
                if config["range"] not in ["10", "30", "60", "120"]:
                    continue
            else:
                if config["range"] in ["Self", "Touch", "Self (aoe)"]:
                    continue
                feet = int(spell.range.split(" ")[0].split("-")[0].replace(",", ""))
                if "mile" in spell.range:
                    feet *= 5280
                if feet < int(config["range"]):
                    continue
        if config["duration"] is not None:
            if config["duration"] == "Instantaneous":
                if spell.duration != "Instantaneous":
                    continue
            elif "Until dispelled" not in spell.duration:
                if spell.duration == "Instantaneous":
                    continue
                if spell.duration == "Special":
                    minutes_spell = 1440
                else:
                    minutes_spell = int(spell.duration.split(" ")[-2])
                    if "hour" in spell.duration:
                        minutes_spell *= 60
                    if "day" in spell.duration:
                        minutes_spell *= 1440
                    if "round" in spell.duration:
                        minutes_spell *= 0.1
                # same thing for config["duration"]
                minutes_config = int(config["duration"].split(" ")[-2])
                if "hour" in config["duration"]:
                    minutes_config *= 60
                if "day" in config["duration"]:
                    minutes_config *= 1440
                if "round" in config["duration"]:
                    minutes_config *= 0.1
                if minutes_spell < minutes_config:
                    continue
        if config["components"] is not None:
            if spell.components != config["components"]:
                continue
        if config["concentration"] is not None:
            if config["concentration"] == "Yes":
                if "Concentration" not in spell.duration:
                    continue
            elif "Concentration" in spell.duration:
                continue
        if not config["source"][spell.source]:
            continue

        spells.append(spell)

    return spells

def scrape_property(description, property):
    soup = BeautifulSoup(description, "html.parser")
    match property:
        case "Level":
            # get first <p> in <div> with id page-content
            div = soup.find("div", id="page-content")
            p = div.find_all("p")[1]
            if "cantrip" in p.text:
                return 0
            return p.text[0]
        case "School":
            div = soup.find("div", id="page-content")
            p = div.find_all("p")[1]
            # remove (ritual) from p.text, capitalize first letters of each word
            p_text = p.text.replace("(ritual)", "").strip()
            p_text = " ".join([word.capitalize() for word in p_text.split(" ")])
            if "Cantrip" in p_text:
                return p_text.strip().split(" ")[1]
            return p_text.strip().split(" ")[-1]
        case "Casting Time":
            div = soup.find("div", id="page-content")
            p = div.find_all("p")[2]
            ct =  str(p).split("</strong> ")[1].split("<strong>")[0].replace("</p>", "").replace("<br/>", "").strip()
            ct = ct.split(",")[0]
            return ct
        case "Range":
            div = soup.find("div", id="page-content")
            p = div.find_all("p")[2]
            range = str(p).split("</strong> ")[2].split("<strong>")[0].replace("</p>", "").replace("<br/>", "").strip()
            range = range.replace("ft", " feet")
            return range
        case "Components":
            div = soup.find("div", id="page-content")
            p = div.find_all("p")[2]
            components = str(p).split("</strong> ")[3].split("<strong>")[0].replace("</p>", "").replace("<br/>", "").strip()
            # remove stuff in parentheses
            return components.split(" (")[0]
        case "Duration":
            div = soup.find("div", id="page-content")
            p = div.find_all("p")[2]
            p_text = str(p).replace("(see below)", "")
            return p_text.split("</strong> ")[4].split("<strong>")[0].replace("</p>", "").replace("<br/>", "").strip()
        case "Source":
            source = soup.find("p", text=lambda x: x and "Source:" in x).text.lower()
            if "player's handbook" in source:
                return "phb"
            elif "xanathar's guide to everything" in source:
                return "xge"
            elif "tasha's cauldron of everything" in source:
                return "tce"
            elif "unearthed arcana" in source:
                return "ua"
            else:
                return "other"
