"""
Player Character - Handles player stats, inventory, and actions
"""

from ..items.items import Equipment
from .player_database import PlayerDatabase
from .stats_system import StatsSystem, LEGACY_ALIASES

class Player:
    """Player character class"""

    def __init__(self, x=0, y=0, archetype='warrior', allocated_main=None):
        # Position
        self.x = x
        self.y = y

        # Stats system (class/archetype + allocation)
        self.archetype = archetype
        self.stats = StatsSystem(
            db=PlayerDatabase,
            class_name=self.archetype,
            allocated_main=allocated_main or {},
            equipment_bonuses={}
        )

        # Legacy properties for backwards compatibility (will be deprecated)
        self.base_max_hp = self.stats.get_base_stat('hp')
        self.base_attack = self.stats.get_base_stat('attack')
        self.base_defense = self.stats.get_base_stat('defense')
        self.base_speed = self.stats.get_base_stat('speed')

        # Current stats (including equipment bonuses)
        self.max_hp = self.stats.get_stat('hp')
        self.hp = self.max_hp
        self.attack = self.stats.get_stat('attack')
        self.defense = self.stats.get_stat('defense')
        self.speed = self.stats.get_stat('speed')

        # Extended examples (access any as needed)
        self.intelligence = self.stats.get_stat('intelligence')
        self.accuracy = self.stats.get_stat('accuracy')
        self.dodge = self.stats.get_stat('dodge')
        self.parry = self.stats.get_stat('parry')
        self.athletism = self.stats.get_stat('athletism')
        self.cunning = self.stats.get_stat('cunning')

        # Character progression
        self.level = 1
        self.exp = 0
        self.exp_to_next = 100

        # Display
        self.symbol = '@'
        self.name = "Hero"

        # Inventory and Equipment
        self.inventory = []
        self.max_inventory = 20
        self.equipment = Equipment()

        # Starting item
        self.starting_item = None

    # ---- class/archetype & allocation hooks ----
    def set_class(self, class_name):
        self.archetype = class_name
        self.stats.set_class(class_name)
        self.recalculate_stats()

    def allocate_points(self, **kwargs):
        """Example: player.allocate_points(strength=2, vitality=1)"""
        alloc = dict(self.stats.allocated_main)
        for k, v in kwargs.items():
            alloc[k] = alloc.get(k, 0) + int(v)
        self.stats.set_allocated_main(alloc)
        self.recalculate_stats()

    # ---- items & equipment ----
    def set_starting_item(self, item):
        """Set and auto-equip starting item."""
        self.starting_item = item
        self.add_item(item)
        success, message = self.equipment.equip_item(item, self)
        return success, message

    def recalculate_stats(self):
        """Recalculate all stats based on base + class + equipment"""
        bonuses = self.equipment.get_total_stat_bonuses()  # dict of stat -> bonus
        self.stats.set_equipment_bonuses(bonuses)

        # Update legacy properties (compat)
        self.base_max_hp = self.stats.get_base_stat('hp')
        self.base_attack = self.stats.get_base_stat('attack')
        self.base_defense = self.stats.get_stat('defense')
        self.base_speed = self.stats.get_stat('speed')

        # Update current stats
        old_max = getattr(self, "max_hp", self.stats.get_stat('hp'))
        old_ratio = (self.hp / old_max) if old_max else 1.0

        self.max_hp = self.stats.get_stat('hp')
        self.attack = self.stats.get_stat('attack')
        self.defense = self.stats.get_stat('defense')
        self.speed = self.stats.get_stat('speed')

        # Extended examples
        self.intelligence = self.stats.get_stat('intelligence')
        self.accuracy = self.stats.get_stat('accuracy')
        self.dodge = self.stats.get_stat('dodge')
        self.parry = self.stats.get_stat('parry')
        self.athletism = self.stats.get_stat('athletism')
        self.cunning = self.stats.get_stat('cunning')

        # Keep current HP proportionally within new max
        self.hp = min(self.max_hp, int(round(self.max_hp * old_ratio)))

    def move(self, new_x, new_y):
        """Move player to new position"""
        self.x = new_x
        self.y = new_y

    def is_alive(self):
        """Check if player is still alive"""
        return self.hp > 0

    def take_damage(self, damage):
        """Player takes damage and returns damage info"""
        # Simple flat reduction by 'defense'. If you later change to % models,
        # adjust here (e.g., damage *= (100 - defense%) / 100).
        actual_damage = max(1, damage - self.defense)
        deflected_damage = damage - actual_damage
        self.hp -= actual_damage

        died = False
        if self.hp <= 0:
            self.hp = 0
            died = True

        return {
            "died": died,
            "deflected": deflected_damage
        }

    def heal(self, amount):
        """Heal the player"""
        self.hp = min(self.max_hp, self.hp + amount)

    def gain_exp(self, amount):
        """Gain experience points and handle level-ups"""
        self.exp += amount
        while self.exp >= self.exp_to_next:
            self.level_up()

    def level_up(self):
        """Level up the player (no auto-stat growth; you allocate points manually)"""
        self.level += 1
        self.exp -= self.exp_to_next
        self.exp_to_next = int(self.exp_to_next * 1.5)

        # Preserve HP ratio through the stat recompute
        old_ratio = (self.hp / self.max_hp) if self.max_hp else 1.0
        self.recalculate_stats()
        self.hp = min(self.max_hp, int(round(self.max_hp * old_ratio)))

    def attack_enemy(self, enemy):
        """Attack an enemy"""
        import random
        # Use derived 'attack' as scaler; add some variance
        damage = max(1, int(self.attack + random.randint(-2, 3)))
        result = enemy.take_damage(damage)

        enemy_died = result["died"]
        if enemy_died:
            self.gain_exp(getattr(enemy, "exp_reward", 0))

        return {
            "type": "combat",
            "attacker": self.name,
            "target": enemy.name,
            "damage": damage,
            "enemy_died": enemy_died,
            "exp_gained": getattr(enemy, "exp_reward", 0) if enemy_died else 0
        }

    # ---- inventory & equipment passthroughs ----
    def add_item(self, item):
        """Add item to inventory"""
        if len(self.inventory) < self.max_inventory:
            self.inventory.append(item)
            return True
        return False  # Inventory full

    def remove_item(self, item):
        """Remove item from inventory"""
        if item in self.inventory:
            self.inventory.remove(item)
            return True
        return False

    def equip_item(self, item):
        """Equip an item"""
        if item not in self.inventory:
            return False, "Item not in inventory"

        success, message = self.equipment.equip_item(item, self)
        if success:
            self.recalculate_stats()
        return success, message

    def unequip_item(self, item):
        """Unequip an item"""
        success, message = self.equipment.unequip_item(item, self)
        if success:
            self.recalculate_stats()
        return success, message

    def use_item(self, item):
        """Use/consume an item"""
        if item not in self.inventory:
            return False, "Item not in inventory"

        result = item.use_item(self)
        if result:
            if getattr(item, "type", None) == 'consumable':
                self.remove_item(item)
            return True, result
        return False, "Cannot use this item"

    # ---- public getters for UI/debug ----
    def get_stats(self):
        """Get formatted player stats (legacy + a few extended fields)"""
        return {
            'name': self.name,
            'level': self.level,
            'hp': self.hp,
            'max_hp': self.max_hp,
            'attack': self.attack,
            'defense': self.defense,
            'speed': self.speed,
            'intelligence': self.intelligence,
            'accuracy': self.accuracy,
            'dodge': self.dodge,
            'parry': self.parry,
            'athletism': self.athletism,
            'cunning': self.cunning,
            'exp': self.exp,
            'exp_to_next': self.exp_to_next,
            'position': (self.x, self.y)
        }

    def get_detailed_stats(self):
        """Get detailed stats including base and equipment bonuses"""
        return {
            'base_stats': self.stats.get_all_base_stats(),
            'equipment_bonuses': self.stats.get_all_equipment_bonuses(),
            'total_stats': self.stats.get_all_stats()
        }

    def get_stat_breakdown(self, stat_name):
        """Get detailed breakdown of a specific stat"""
        return self.stats.get_stat_breakdown(stat_name)

    def get_all_available_stats(self):
        """Get list of all available stat names"""
        mains = list(PlayerDatabase.STATS["main"].keys())
        derived = list(PlayerDatabase.STATS["derived"].keys())
        return mains + derived

    def get_equipped_items_summary(self):
        """Get a summary of equipped items"""
        equipped = self.equipment.get_equipped_items()
        summary = {}
        for slot, item in equipped.items():
            summary[slot] = {
                'name': item.name,
                'stats': getattr(item, "stats", {}),
                'quality': getattr(item, "quality", None),
            }
        return summary
