class Spell:
    def __init__(self, level, name, school, casting_time, range, duration, components):
        self.level = level
        self.name = name
        self.school = school
        self.casting_time = casting_time
        self.range = range
        self.duration = duration
        self.components = components

def spellize(df):
    spells = []
    for row in df.itertuples():
        spell = Spell(row[1], row[2], row[3], row[4], row[5], row[6], row[7])
        spells.append(spell)
    return spells

def spell_to_dict(spell):
    return {
        "level": spell.level,
        "name": spell.name,
        "school": spell.school,
        "casting_time": spell.casting_time,
        "range": spell.range,
        "duration": spell.duration,
        "components": spell.components
    }

def filter_spells(config, spell_list):
    spells = []
    for spell in spell_list:
        if config["query"] is not None:
            if config["query"].lower() not in spell.name.lower():
                continue
        if config["levels"] != []:
            if int(spell.level) not in config["levels"]:
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
                feet = int(spell.range.split(" ")[0])
                if "mile" in spell.range:
                    feet *= 5280
                if feet < int(config["range"]):
                    continue

        spells.append(spell)
    return spells
