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
        if config["query"] is not None and config["query"] != "":
            if config["query"].lower() not in spell.name.lower():
                continue
        if config["levels"] != []:
            if int(spell.level) not in config["levels"]:
                continue
        spells.append(spell)
    return spells
