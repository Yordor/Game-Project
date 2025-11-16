ITEM_STATS = {
    "Atk Gem":     {"ATK": 2},
    "Def Gem":     {"DEF": 1},
    "Heal Potion": {"HP": 50},
}

class Item:
    def __init__(self, name):
        self.name = name
        self.stats = ITEM_STATS[name]

def apply_item(player, item_name):
    stats = ITEM_STATS[item_name]

    if "HP" in stats:
        player.hp += stats["HP"]

    if "ATK" in stats:
        player.atk += stats["ATK"]

    if "DEF" in stats:

        player.defense += stats["DEF"]
