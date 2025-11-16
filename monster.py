MONSTER_STATS = {
    "Normal":   {"HP": 50, "ATK": 15, "DEF": 5},
    "Tank(HP)": {"HP": 200, "ATK": 10,  "DEF": 4},
    "Tank(DEF)": {"HP": 30, "ATK": 10, "DEF": 20},
    "Attack":   {"HP": 30, "ATK": 40, "DEF": 2},
    "BOSS":     {"HP": 220, "ATK": 40, "DEF": 12},
}


class Monster:
    def __init__(self, name):
        stats = MONSTER_STATS[name]
        self.name = name
        self.hp = stats["HP"]
        self.atk = stats["ATK"]

        self.defense = stats["DEF"]
