"""
Player Database - Defines base stats and stat configurations for players
"""

class PlayerDatabase:
    """Central database for player stat & class definitions"""

    STATS = {
        "main": {
            "strength":     {"name": "Strength", "description": "Physical power & parry", "base_value": 10, "min_value": 1, "max_value": 99},
            "dexterity":    {"name": "Dexterity", "description": "Accuracy, finesse, speed", "base_value": 10, "min_value": 1, "max_value": 99},
            "cunning":      {"name": "Cunning", "description": "Trickery, crits, stealth", "base_value": 10, "min_value": 1, "max_value": 99},
            "athletism":    {"name": "Athletism", "description": "Stamina & mobility", "base_value": 10, "min_value": 1, "max_value": 99},
            "vitality":     {"name": "Vitality", "description": "Health & resilience", "base_value": 10, "min_value": 1, "max_value": 120},
            "intelligence": {"name": "Intelligence", "description": "Mana & magic", "base_value": 10, "min_value": 1, "max_value": 99},
            "willpower":    {"name": "Willpower", "description": "Focus & status resist", "base_value": 8,  "min_value": 1, "max_value": 99},
            "charisma":     {"name": "Charisma", "description": "Persuasion & trading", "base_value": 5,  "min_value": 1, "max_value": 99},
            "luck":         {"name": "Luck", "description": "Loot & random rolls", "base_value": 5,  "min_value": 1, "max_value": 99},
        },
        "derived": {
            # existing
            "health":           {"name": "Health", "description": "HP pool", "formula": "vitality * 10 + strength * 2", "min_value": 1,  "max_value": 9999},
            "mana":             {"name": "Mana", "description": "Spell resource", "formula": "intelligence * 12 + willpower * 5", "min_value": 0, "max_value": 999},
            "stamina":          {"name": "Stamina", "description": "Action energy", "formula": "athletism * 8 + vitality * 2", "min_value": 0,  "max_value": 500},
            "parry":            {"name": "Parry Chance", "description": "Deflect hits", "formula": "strength * 0.5", "min_value": 0,  "max_value": 90},
            "dodge":            {"name": "Dodge Chance", "description": "Avoid hits", "formula": "dexterity * 0.4 + athletism * 0.2", "min_value": 0, "max_value": 95},
            "accuracy":         {"name": "Accuracy", "description": "Hit chance", "formula": "dexterity * 0.6 + cunning * 0.3", "min_value": 10, "max_value": 100},
            "crit_chance":      {"name": "Critical Hit Chance", "description": "Crit probability", "formula": "cunning * 0.5 + luck * 0.2", "min_value": 0, "max_value": 100},
            "crit_damage":      {"name": "Critical Damage", "description": "Crit multiplier %", "formula": "150 + (cunning * 0.3)", "min_value": 100, "max_value": 300},
            "defense":          {"name": "Defense", "description": "Reduce physical dmg (%)", "formula": "vitality * 0.5 + strength * 0.3 + athletism * 0.2", "min_value": 0, "max_value": 999},
            # "magic_resistance": {"name": "Magic Resistance", "description": "Reduce magic dmg (%)", "formula": "willpower * 0.5 + intelligence * 0.2", "min_value": 0, "max_value": 90},
            "resilience":       {"name": "Resilience", "description": "Status effect resistance", "formula": "vitality * 0.3 + willpower * 0.5", "min_value": 0, "max_value": 95},
            "attack":           {"name": "Attack", "description": "Physical damage scaler", "formula": "strength * 2 + dexterity * 0.5", "min_value": 1, "max_value": 999},
            "speed":            {"name": "Speed", "description": "Movement/turn pacing", "formula": "dexterity * 0.5 + athletism * 0.5", "min_value": 1, "max_value": 200},
            # new high-impact
            "initiative":   {"name": "Initiative", "description": "Turn order / action speed", "formula": "dexterity * 0.7 + athletism * 0.3", "min_value": 0, "max_value": 200},
            "armor":        {"name": "Armor", "description": "Flat physical damage reduction", "formula": "vitality * 0.4 + strength * 0.2", "min_value": 0, "max_value": 500},
            "block_chance": {"name": "Block Chance", "description": "Chance to block with a shield", "formula": "strength * 0.2 + athletism * 0.1", "min_value": 0, "max_value": 80},
            "block_amount": {"name": "Block Amount", "description": "Damage reduced on block", "formula": "armor * 0.6 + defense * 0.4", "min_value": 0, "max_value": 400},

            "hp_regen":     {"name": "HP Regeneration", "description": "HP per turn", "formula": "max(0, vitality * 0.2 + willpower * 0.05)", "min_value": 0, "max_value": 50},
            "mana_regen":   {"name": "Mana Regeneration", "description": "Mana per turn", "formula": "max(0, intelligence * 0.3 + willpower * 0.2)", "min_value": 0, "max_value": 50},
            "stamina_regen":{"name": "Stamina Regeneration", "description": "Stamina per turn", "formula": "max(0, athletism * 0.3 + vitality * 0.1)", "min_value": 0, "max_value": 50},

            "spell_power":  {"name": "Spell Power", "description": "Spell damage/healing scaler", "formula": "intelligence * 1.0 + willpower * 0.5", "min_value": 0, "max_value": 999},
            "status_power": {"name": "Status Power", "description": "Potency of DoTs/CC", "formula": "cunning * 0.6 + intelligence * 0.4", "min_value": 0, "max_value": 100},
            "healing_power":{"name": "Healing Power", "description": "Effectiveness of healing", "formula": "willpower * 0.8 + intelligence * 0.4", "min_value": 0, "max_value": 300},

            "stealth":      {"name": "Stealth", "description": "Avoid detection / ambush", "formula": "cunning * 0.7 + dexterity * 0.3", "min_value": 0, "max_value": 100},
            "perception":   {"name": "Perception", "description": "Detect traps & secrets", "formula": "cunning * 0.5 + luck * 0.5", "min_value": 0, "max_value": 100},
            "light_radius": {"name": "Light Radius", "description": "Sight distance in darkness", "formula": "perception * 0.3 + (luck * 0.1)", "min_value": 1, "max_value": 15},
            "carry_capacity":{"name": "Carry Capacity", "description": "Encumbrance threshold", "formula": "50 + strength * 5 + athletism * 2", "min_value": 10, "max_value": 999},
        },
    }

    CLASSES = {
        # melee bruiser / off-tank
        "warrior": {
            "labels": ["melee", "bruiser", "tankish"],
            "starting_main_bonus": {"strength": +4, "vitality": +4},
            "main_affinity": {
                "strength": 1.15, "vitality": 1.10, "athletism": 1.05,
                "dexterity": 1.00, "cunning": 0.95, "intelligence": 0.90,
                "willpower": 1.00, "charisma": 1.00, "luck": 1.00,
            },
            "derived_affinity": {
                # existing
                "health": 1.20, "defense": 1.30, "parry": 1.25, "stamina": 1.20,
                "accuracy": 1.00, "dodge": 0.95, "crit_chance": 0.95, "crit_damage": 1.00,
                "mana": 0.80, "magic_resistance": 1.00, "resilience": 1.10,
                # new
                "initiative": 1.00, "armor": 1.25, "block_chance": 1.25, "block_amount": 1.20,
                "hp_regen": 1.15, "mana_regen": 0.85, "stamina_regen": 1.10,
                "spell_power": 0.85, "status_power": 0.95, "healing_power": 0.95,
                "stealth": 0.90, "perception": 1.00, "light_radius": 1.00, "carry_capacity": 1.25,
            },
        },

        # glass cannon caster
        "mage": {
            "labels": ["caster", "glass_cannon"],
            "starting_main_bonus": {"intelligence": +3, "willpower": +1},
            "main_affinity": {
                "intelligence": 1.20, "willpower": 1.10, "luck": 1.05,
                "dexterity": 1.00, "cunning": 1.00, "strength": 0.85,
                "athletism": 0.95, "vitality": 0.95, "charisma": 1.00,
            },
            "derived_affinity": {
                "mana": 1.25, "magic_resistance": 1.10, "accuracy": 1.05,
                "crit_chance": 1.05, "crit_damage": 1.10,
                "health": 0.90, "defense": 0.85, "parry": 0.85, "dodge": 0.95, "stamina": 0.95, "resilience": 1.00,
                # new
                "initiative": 1.00, "armor": 0.85, "block_chance": 0.80, "block_amount": 0.85,
                "hp_regen": 0.95, "mana_regen": 1.25, "stamina_regen": 0.95,
                "spell_power": 1.30, "status_power": 1.20, "healing_power": 1.10,
                "stealth": 0.95, "perception": 1.05, "light_radius": 1.10, "carry_capacity": 0.85,
            },
        },

        # stealth assassin (note: 'rogue', not 'rouge')
        "rogue": {
            "labels": ["stealth", "assassin"],
            "starting_main_bonus": {"dexterity": +3, "cunning": +3, "luck": +2},
            "main_affinity": {
                "dexterity": 1.20, "cunning": 1.15, "luck": 1.10,
                "strength": 0.95, "athletism": 1.05, "vitality": 0.95,
                "intelligence": 1.00, "willpower": 1.00, "charisma": 1.00,
            },
            "derived_affinity": {
                "accuracy": 1.15, "dodge": 1.20, "crit_chance": 1.20, "crit_damage": 1.10,
                "parry": 0.95, "defense": 0.90, "health": 0.95, "mana": 1.00, "stamina": 1.10,
                "magic_resistance": 0.95, "resilience": 1.00,
                # new
                "initiative": 1.20, "armor": 0.90, "block_chance": 0.85, "block_amount": 0.85,
                "hp_regen": 1.00, "mana_regen": 1.00, "stamina_regen": 1.10,
                "spell_power": 0.95, "status_power": 1.10, "healing_power": 0.95,
                "stealth": 1.30, "perception": 1.20, "light_radius": 1.05, "carry_capacity": 1.00,
            },
        },

        # trickster skirmisher
        "bandit": {
            "labels": ["skirmisher", "trickster"],
            "starting_main_bonus": {"dexterity": +1, "cunning": +2, "luck": +4},
            "main_affinity": {
                "cunning": 1.15, "dexterity": 1.10, "luck": 1.15,
                "strength": 1.00, "athletism": 1.05, "vitality": 0.95,
                "intelligence": 1.00, "willpower": 0.95, "charisma": 1.05,
            },
            "derived_affinity": {
                "accuracy": 1.10, "crit_chance": 1.25, "crit_damage": 1.05, "dodge": 1.10,
                "parry": 0.95, "defense": 0.90, "health": 0.95, "stamina": 1.05, "mana": 0.95,
                "magic_resistance": 0.95, "resilience": 0.95,
                # new
                "initiative": 1.15, "armor": 0.90, "block_chance": 0.90, "block_amount": 0.90,
                "hp_regen": 1.00, "mana_regen": 0.95, "stamina_regen": 1.05,
                "spell_power": 0.95, "status_power": 1.15, "healing_power": 0.95,
                "stealth": 1.20, "perception": 1.15, "light_radius": 1.00, "carry_capacity": 1.05,
            },
        },

        # drainy caster with resilience
        "warlock": {
            "labels": ["dark_caster", "drains"],
            "starting_main_bonus": {"intelligence": +2, "willpower": +2, "vitality": +3},
            "main_affinity": {
                "intelligence": 1.15, "willpower": 1.20, "luck": 1.05,
                "cunning": 1.05, "vitality": 0.95, "strength": 0.90,
                "dexterity": 0.95, "athletism": 0.95, "charisma": 1.00,
            },
            "derived_affinity": {
                "mana": 1.20, "magic_resistance": 1.15, "resilience": 1.10,
                "crit_chance": 1.05, "crit_damage": 1.05,
                "health": 0.95, "defense": 0.90, "parry": 0.90, "dodge": 0.95, "accuracy": 1.00, "stamina": 0.95,
                # new
                "initiative": 0.95, "armor": 0.90, "block_chance": 0.85, "block_amount": 0.85,
                "hp_regen": 1.05, "mana_regen": 1.20, "stamina_regen": 0.95,
                "spell_power": 1.25, "status_power": 1.30, "healing_power": 1.00,
                "stealth": 1.00, "perception": 1.05, "light_radius": 1.05, "carry_capacity": 0.90,
            },
        },

        # holy knight: tank/support hybrid
        "paladin": {
            "labels": ["holy_knight", "tank_support"],
            "starting_main_bonus": {"strength": +1, "vitality": +5, "willpower": +3},
            "main_affinity": {
                "vitality": 1.15, "willpower": 1.10, "strength": 1.10,
                "dexterity": 1.00, "athletism": 1.05, "intelligence": 1.00,
                "cunning": 0.95, "charisma": 1.05, "luck": 1.00,
            },
            "derived_affinity": {
                "health": 1.15, "defense": 1.20, "parry": 1.10, "resilience": 1.15, "magic_resistance": 1.10,
                "mana": 1.05, "accuracy": 1.00, "dodge": 0.95, "crit_chance": 0.95, "crit_damage": 1.00, "stamina": 1.10,
                # new
                "initiative": 1.00, "armor": 1.25, "block_chance": 1.25, "block_amount": 1.25,
                "hp_regen": 1.15, "mana_regen": 1.10, "stamina_regen": 1.10,
                "spell_power": 1.05, "status_power": 0.95, "healing_power": 1.25,
                "stealth": 0.90, "perception": 1.05, "light_radius": 1.10, "carry_capacity": 1.10,
            },
        },
    }

    @classmethod
    def get_all_stat_names(cls):
        """Get all available stat names (main + derived)"""
        main_stats = list(cls.STATS["main"].keys())
        derived_stats = list(cls.STATS["derived"].keys())
        return main_stats + derived_stats
