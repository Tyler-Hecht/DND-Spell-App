import json

class Spell:
    def __init__(self, level, name, school, casting_time, range, duration, components):
        self.level = level
        self.name = name
        self.school = school
        self.casting_time = casting_time
        self.range = range
        self.duration = duration
        self.components = components

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

def spellize(df):
    spells = []
    for row in df.itertuples():
        spell = Spell(row[1], row[2], row[3], row[4], row[5], row[6], row[7])
        spells.append(spell)
    return spells
