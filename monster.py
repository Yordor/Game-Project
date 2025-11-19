MONSTER_STATS = {
    "Slime":   {"HP": 80, "ATK": 20, "DEF": 5},
    "Ghost": {"HP": 200, "ATK": 10,  "DEF": 4},
    "Spider": {"HP": 50, "ATK": 15, "DEF": 15},
    "Bat":   {"HP": 30, "ATK": 40, "DEF": 2},
    "BOSS":     {"HP": 220, "ATK": 40, "DEF": 12},
}


class Monster:
    def __init__(self, name):
        stats = MONSTER_STATS[name]
        self.name = name
        self.hp = stats["HP"]
        self.atk = stats["ATK"]

        self.defense = stats["DEF"]

