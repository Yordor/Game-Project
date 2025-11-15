MONSTER_STATS = {
    "Normal":   {"HP": 50, "ATK": 10, "DEF": 3},
    "Tank(HP)": {"HP": 90, "ATK": 5,  "DEF": 4},
    "Tank(DEF)": {"HP": 50, "ATK": 5, "DEF": 20},
    "Attack":   {"HP": 40, "ATK": 50, "DEF": 2},
    "BOSS":     {"HP": 220, "ATK": 40, "DEF": 12},
}


class Monster:
    def __init__(self, name):
        stats = MONSTER_STATS[name]
        self.name = name
        self.hp = stats["HP"]
        self.atk = stats["ATK"]
        self.defense = stats["DEF"]