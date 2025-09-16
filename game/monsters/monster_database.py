"""
Monster Database - All game monster definitions with drop chances and attacks
"""

import random
import ast
import operator

class MonsterStatsSystem:
    """Stats calculation system for monsters using formulas"""
    
    def __init__(self):
        self.operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.FloorDiv: operator.floordiv,
            ast.Mod: operator.mod,
            ast.Pow: operator.pow,
        }
    
    def _safe_eval(self, node, stats_dict):
        """Safely evaluate mathematical expressions"""
        if isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.Name):
            return stats_dict.get(node.id, 0)
        elif isinstance(node, ast.BinOp):
            left = self._safe_eval(node.left, stats_dict)
            right = self._safe_eval(node.right, stats_dict)
            op = self.operators.get(type(node.op))
            if op:
                return op(left, right)
        return 0
    
    def calculate_stats(self, base_stats, creature_type, level=1):
        """Calculate all stats for a monster"""
        # Get creature type data
        creature_data = MonsterDatabase.CREATURE_TYPES.get(creature_type, MonsterDatabase.CREATURE_TYPES['brute'])
        
        # Calculate main stats with creature type affinities
        main_stats = {}
        for stat_name, base_value in base_stats.items():
            if stat_name in MonsterDatabase.MAIN_STATS:
                affinity = creature_data['affinities'].get(stat_name, 1.0)
                main_stats[stat_name] = int(base_value * affinity * level)
        
        # Calculate derived stats using formulas
        derived_stats = {}
        for stat_name, formula in MonsterDatabase.DERIVED_STATS.items():
            try:
                tree = ast.parse(formula, mode='eval')
                derived_stats[stat_name] = int(self._safe_eval(tree.body, main_stats))
            except:
                derived_stats[stat_name] = 0
        
        return {**main_stats, **derived_stats}
    
    def calculate_attack_stats(self, attack_data, main_stats):
        """Calculate dynamic attack damage and accuracy from formulas"""
        result = attack_data.copy()
        
        # Calculate damage if formula provided
        if 'damage_formula' in attack_data:
            try:
                tree = ast.parse(attack_data['damage_formula'], mode='eval')
                result['damage'] = int(self._safe_eval(tree.body, main_stats))
            except:
                result['damage'] = 5  # Fallback damage
        
        # Calculate accuracy if formula provided  
        if 'accuracy_formula' in attack_data:
            try:
                tree = ast.parse(attack_data['accuracy_formula'], mode='eval')
                accuracy = self._safe_eval(tree.body, main_stats)
                result['accuracy'] = min(0.95, max(0.05, accuracy / 100.0))  # Convert to decimal, clamp
            except:
                result['accuracy'] = 0.75  # Fallback accuracy
        
        # Calculate special effect values if formulas provided
        if 'special_effects' in attack_data and attack_data['special_effects']:
            effects = result['special_effects'] = attack_data['special_effects'].copy()
            
            # Handle damage per turn formulas
            if 'damage_per_turn_formula' in effects:
                try:
                    tree = ast.parse(effects['damage_per_turn_formula'], mode='eval')
                    effects['damage_per_turn'] = int(self._safe_eval(tree.body, main_stats))
                    del effects['damage_per_turn_formula']  # Remove formula after calculation
                except:
                    effects['damage_per_turn'] = 2  # Fallback
        
        return result

class MonsterDatabase:
    """Central database of all monsters and related functionality"""
    
    # Main stats that define a monster's base abilities
    MAIN_STATS = {
        'might': 'Physical strength and raw power',
        'agility': 'Speed, reflexes, and dexterity', 
        'cunning': 'Intelligence, tactics, and problem-solving',
        'vitality': 'Health, endurance, and resilience',
        'ferocity': 'Aggression, damage potential, and combat instinct',
        'mysticism': 'Magical power and supernatural abilities'
    }
    
    # Derived stats calculated from main stats using formulas
    DERIVED_STATS = {
        'hp': 'vitality * 8 + might * 2',
        'attack': 'might * 2 + ferocity * 3',
        'defense': 'vitality * 1 + might * 1', 
        'speed': 'agility * 2 + vitality * 1',
        'accuracy': '70 + agility * 2 + cunning * 1',
        'dodge': 'agility * 3 + cunning * 1',
        'intimidation': 'ferocity * 2 + might * 1',
        'magic_power': 'mysticism * 4 + cunning * 1',
        'detection_range': 'cunning * 1 + agility * 1'
    }
    
    # Creature types with stat affinities (multipliers for main stats)
    CREATURE_TYPES = {
        'brute': {
            'description': 'Raw physical power, high health and attack',
            'affinities': {
                'might': 1.4, 'agility': 0.7, 'cunning': 0.6,
                'vitality': 1.3, 'ferocity': 1.2, 'mysticism': 0.5
            }
        },
        'predator': {
            'description': 'Fast, agile hunters with keen senses', 
            'affinities': {
                'might': 1.1, 'agility': 1.5, 'cunning': 1.2,
                'vitality': 0.9, 'ferocity': 1.3, 'mysticism': 0.7
            }
        },
        'caster': {
            'description': 'Magical creatures with supernatural abilities',
            'affinities': {
                'might': 0.7, 'agility': 1.0, 'cunning': 1.4,
                'vitality': 0.8, 'ferocity': 0.9, 'mysticism': 1.6
            }
        },
        'tank': {
            'description': 'Heavily armored defensive creatures',
            'affinities': {
                'might': 1.2, 'agility': 0.6, 'cunning': 0.8,
                'vitality': 1.6, 'ferocity': 0.9, 'mysticism': 0.7
            }
        },
        'swarm': {
            'description': 'Fast, numerous creatures that overwhelm',
            'affinities': {
                'might': 0.8, 'agility': 1.4, 'cunning': 1.1,
                'vitality': 0.7, 'ferocity': 1.2, 'mysticism': 0.9
            }
        },
        'undead': {
            'description': 'Reanimated creatures with unnatural resilience',
            'affinities': {
                'might': 1.0, 'agility': 0.8, 'cunning': 0.7,
                'vitality': 1.2, 'ferocity': 1.1, 'mysticism': 1.3
            }
        }
    }
    
    MONSTERS = {
        'undead': {
            'skeleton_warrior': {
                'name': 'Skeleton Warrior', 'type': 'undead', 'symbol': 'S', 'color': 'white',
                'description': 'An undead warrior wielding ancient weapons, bones clicking with each movement.',
                'creature_type': 'undead', 'level': 1,
                'base_stats': {'might': 7, 'agility': 6, 'cunning': 4, 'vitality': 6, 'ferocity': 7, 'mysticism': 5},
                'exp_reward': 20,
                'drop_chances': {'weapons': 0.20, 'armor': 0.10, 'shields': 0.15, 'potions': 0.25},
                'attacks': [
                    {'name': 'Bone Blade Strike', 'damage_formula': 'might * 2 + ferocity * 1', 'accuracy_formula': '80 + agility * 2', 'description': 'Slashes with a blade of sharpened bone', 'type': 'special', 'cooldown': 1, 'special_effects': None},
                    {'name': 'Death Rattle', 'damage_formula': 'mysticism * 2 + cunning * 1', 'accuracy_formula': '90 + mysticism * 1', 'description': 'Emits a chilling rattle that weakens the living', 'type': 'special', 'cooldown': 3, 'special_effects': {'type': 'fear', 'duration': 2, 'effect': 'reduces_player_attack'}}
                ]
            },
            'plague_zombie': {
                'name': 'Plague Zombie', 'type': 'undead', 'symbol': 'Z', 'color': 'green',
                'description': 'A rotting corpse seeping with disease, shambling with relentless hunger.',
                'creature_type': 'brute', 'level': 1,
                'base_stats': {'might': 9, 'agility': 3, 'cunning': 2, 'vitality': 10, 'ferocity': 7, 'mysticism': 4},
                'exp_reward': 25,
                'drop_chances': {'weapons': 0.05, 'armor': 0.20, 'shields': 0.05, 'potions': 0.35},
                'attacks': [
                    {'name': 'Infected Bite', 'damage_formula': 'ferocity * 2 + mysticism * 1', 'accuracy_formula': '70 + vitality * 2', 'description': 'Bites with diseased teeth, spreading infection', 'type': 'special', 'cooldown': 2, 'special_effects': {'type': 'poison', 'duration': 4, 'damage_per_turn_formula': 'mysticism * 2 + 2'}},
                    {'name': 'Corpse Slam', 'damage_formula': 'might * 2 + vitality * 1', 'accuracy_formula': '65 + might * 1', 'description': 'Slams with the full weight of undeath', 'type': 'special', 'cooldown': 1, 'special_effects': None}
                ]
            },
            'shadow_wraith': {
                'name': 'Shadow Wraith', 'type': 'undead', 'symbol': 'W', 'color': 'black',
                'description': 'A being of pure shadow and malice, existing between life and death.',
                'creature_type': 'caster', 'level': 2,
                'base_stats': {'might': 4, 'agility': 8, 'cunning': 9, 'vitality': 5, 'ferocity': 6, 'mysticism': 12},
                'exp_reward': 45,
                'drop_chances': {'weapons': 0.30, 'armor': 0.15, 'shields': 0.20, 'potions': 0.25},
                'attacks': [
                    {'name': 'Shadow Drain', 'damage_formula': 'mysticism * 2 + cunning * 1', 'accuracy_formula': '85 + mysticism * 1', 'description': 'Drains life force through dark magic', 'type': 'special', 'cooldown': 2, 'special_effects': {'type': 'heal_self', 'amount_formula': 'damage / 2'}},
                    {'name': 'Phase Strike', 'damage_formula': 'agility * 2 + mysticism * 1', 'accuracy_formula': '90 + agility * 1', 'description': 'Phases through defenses to strike directly', 'type': 'special', 'cooldown': 1, 'special_effects': {'type': 'phase_through_armor', 'effect': 'ignores_defense'}},
                    {'name': 'Terror Scream', 'damage_formula': 'mysticism * 1 + ferocity * 1', 'accuracy_formula': '95 + cunning * 1', 'description': 'Unleashes a soul-rending scream', 'type': 'special', 'cooldown': 3, 'special_effects': {'type': 'fear', 'duration': 3, 'effect': 'reduces_all_stats'}}
                ]
            }
        },
        'arcane': {
            'fire_imp': {
                'name': 'Fire Imp', 'type': 'arcane', 'symbol': 'i', 'color': 'red',
                'description': 'A mischievous demon wreathed in flames, crackling with chaotic energy.',
                'creature_type': 'swarm', 'level': 1,
                'base_stats': {'might': 3, 'agility': 7, 'cunning': 6, 'vitality': 4, 'ferocity': 8, 'mysticism': 7},
                'exp_reward': 18,
                'drop_chances': {'weapons': 0.25, 'armor': 0.10, 'shields': 0.15, 'potions': 0.30},
                'attacks': [
                    {'name': 'Flame Bolt', 'damage_formula': 'mysticism * 2 + ferocity * 1', 'accuracy_formula': '80 + cunning * 2', 'description': 'Hurls a searing bolt of hellfire', 'type': 'special', 'cooldown': 1, 'special_effects': {'type': 'burn', 'duration': 3, 'damage_per_turn_formula': 'mysticism / 2 + 2'}},
                    {'name': 'Chaos Leap', 'damage_formula': 'agility * 2 + ferocity * 1', 'accuracy_formula': '90 + agility * 1', 'description': 'Teleports through hellish flames to strike', 'type': 'special', 'cooldown': 2, 'special_effects': {'type': 'surprise_attack', 'effect': 'cannot_be_dodged'}}
                ]
            },
            'frost_mage': {
                'name': 'Frost Mage', 'type': 'arcane', 'symbol': 'M', 'color': 'cyan',
                'description': 'A spellcaster wielding the power of ice and winter storms.',
                'creature_type': 'caster', 'level': 2,
                'base_stats': {'might': 4, 'agility': 7, 'cunning': 11, 'vitality': 6, 'ferocity': 5, 'mysticism': 13},
                'exp_reward': 35, 'multi_attack': {'chance': 0.25, 'max_attacks': 2},
                'drop_chances': {'weapons': 0.35, 'armor': 0.25, 'shields': 0.20, 'potions': 0.40},
                'attacks': [
                    {'name': 'Ice Shard', 'damage_formula': 'mysticism * 2 + cunning * 1', 'accuracy_formula': '85 + cunning * 1', 'description': 'Launches a piercing shard of ice', 'type': 'special', 'cooldown': 1, 'special_effects': None},
                    {'name': 'Frost Armor', 'damage_formula': 'mysticism * 1', 'accuracy_formula': '75 + mysticism * 2', 'description': 'Creates armor that slows attackers', 'type': 'special', 'cooldown': 3, 'special_effects': {'type': 'defensive_buff', 'duration': 4, 'effect': 'increases_defense_slows_attackers'}},
                    {'name': 'Blizzard', 'damage_formula': 'mysticism * 2 + ferocity * 1', 'accuracy_formula': '70 + mysticism * 1', 'description': 'Summons a localized blizzard', 'type': 'special', 'cooldown': 2, 'special_effects': {'type': 'freeze', 'duration': 2, 'effect': 'reduces_speed_and_accuracy'}}
                ]
            },
            'storm_elemental': {
                'name': 'Storm Elemental', 'type': 'arcane', 'symbol': 'E', 'color': 'yellow',
                'description': 'A crackling being of pure lightning and thunder, constantly shifting and sparking.',
                'creature_type': 'caster', 'level': 2,
                'base_stats': {'might': 6, 'agility': 9, 'cunning': 7, 'vitality': 7, 'ferocity': 8, 'mysticism': 11},
                'exp_reward': 50,
                'drop_chances': {'weapons': 0.30, 'armor': 0.35, 'shields': 0.25, 'potions': 0.30},
                'attacks': [
                    {'name': 'Lightning Bolt', 'damage_formula': 'mysticism * 3 + agility * 1', 'accuracy_formula': '75 + mysticism * 1', 'description': 'Strikes with pure electrical energy', 'type': 'special', 'cooldown': 1, 'special_effects': {'type': 'stun', 'duration': 1, 'effect': 'skip_next_turn'}},
                    {'name': 'Thunder Clap', 'damage_formula': 'mysticism * 2 + ferocity * 1', 'accuracy_formula': '85 + might * 1', 'description': 'Creates a deafening boom of thunder', 'type': 'special', 'cooldown': 2, 'special_effects': {'type': 'disorient', 'duration': 2, 'effect': 'reduces_accuracy_and_speed'}},
                    {'name': 'Chain Lightning', 'damage_formula': 'mysticism * 2 + agility * 2', 'accuracy_formula': '90 + agility * 1', 'description': 'Lightning that jumps between targets', 'type': 'special', 'cooldown': 3, 'special_effects': {'type': 'chain_attack', 'effect': 'hits_multiple_times'}}
                ]
            }
        },
        'beasts': {
            'dire_wolf': {
                'name': 'Dire Wolf', 'type': 'beasts', 'symbol': 'w', 'color': 'gray',
                'description': 'A massive wolf with glowing red eyes and razor-sharp fangs.',
                'creature_type': 'predator', 'level': 1,
                'base_stats': {'might': 8, 'agility': 10, 'cunning': 7, 'vitality': 8, 'ferocity': 11, 'mysticism': 2},
                'exp_reward': 22, 'multi_attack': {'chance': 0.20, 'max_attacks': 2},
                'drop_chances': {'weapons': 0.15, 'armor': 0.10, 'shields': 0.08, 'potions': 0.18},
                'attacks': [
                    {'name': 'Pack Strike', 'damage_formula': 'ferocity * 2 + might * 1', 'accuracy_formula': '80 + agility * 2', 'description': 'Strikes with the fury of the pack', 'type': 'special', 'cooldown': 1, 'special_effects': None},
                    {'name': 'Savage Bite', 'damage_formula': 'ferocity * 3 + might * 1', 'accuracy_formula': '75 + cunning * 2', 'description': 'Bites with crushing jaws', 'type': 'special', 'cooldown': 2, 'special_effects': {'type': 'bleed', 'duration': 3, 'damage_per_turn_formula': 'ferocity / 3 + 2'}},
                    {'name': 'Howl of Fear', 'damage_formula': 'cunning * 1', 'accuracy_formula': '90 + cunning * 2', 'description': 'Lets out a bone-chilling howl', 'type': 'special', 'cooldown': 3, 'special_effects': {'type': 'fear', 'duration': 2, 'effect': 'reduces_player_attack'}}
                ]
            },
            'shadow_panther': {
                'name': 'Shadow Panther',  
                'type': 'beasts',
                'symbol': 'P',
                'color': 'black',
                'description': 'A sleek predator that stalks through shadows with deadly grace.',
                'creature_type': 'predator',
                'level': 2,
                'base_stats': {'might': 7, 'agility': 12, 'cunning': 9, 'vitality': 6, 'ferocity': 10, 'mysticism': 4},
                'exp_reward': 30,
                'drop_chances': { 'weapons': 0.25, 'armor': 0.15, 'shields': 0.10, 'potions': 0.20 },
                'attacks': [
                    {'name': 'Shadow Strike', 'damage_formula': 'agility * 2 + ferocity * 1', 'accuracy_formula': '85 + agility * 1', 'description': 'Strikes from the shadows with deadly precision', 'type': 'special', 'cooldown': 1, 'special_effects': {'type': 'surprise_attack', 'effect': 'cannot_be_blocked'}},
                    {'name': 'Pounce', 'damage_formula': 'might * 2 + agility * 2', 'accuracy_formula': '75 + agility * 2', 'description': 'Leaps forward with claws extended', 'type': 'special', 'cooldown': 2, 'special_effects': {'type': 'knockdown', 'duration': 1, 'effect': 'reduces_defense'}}
                ]
            },
            'crystal_dragon': {
                'name': 'Crystal Dragon', 'type': 'beasts', 'symbol': 'D', 'color': 'magenta',
                'description': 'A majestic dragon with crystalline scales that refract light into deadly beams.',
                'creature_type': 'brute', 'level': 3,
                'base_stats': {'might': 12, 'agility': 6, 'cunning': 10, 'vitality': 14, 'ferocity': 11, 'mysticism': 8},
                'exp_reward': 120, 'multi_attack': {'chance': 0.45, 'max_attacks': 3},
                'drop_chances': {'weapons': 0.50, 'armor': 0.45, 'shields': 0.40, 'potions': 0.60},
                'attacks': [
                    {'name': 'Crystal Breath', 'damage_formula': 'mysticism * 3 + might * 2', 'accuracy_formula': '80 + cunning * 1', 'description': 'Breathes shards of razor-sharp crystal', 'type': 'special', 'cooldown': 2, 'special_effects': {'type': 'armor_pierce', 'effect': 'ignores_partial_armor'}},
                    {'name': 'Dragon Claw', 'damage_formula': 'might * 3 + ferocity * 2', 'accuracy_formula': '85 + might * 1', 'description': 'Slashes with crystalline claws', 'type': 'special', 'cooldown': 1, 'special_effects': {'type': 'deep_wound', 'duration': 3, 'damage_per_turn_formula': 'might / 2 + 3'}},
                    {'name': 'Prismatic Roar', 'damage_formula': 'mysticism * 2 + cunning * 2', 'accuracy_formula': '90 + mysticism * 1', 'description': 'Roars with the power of refracted light', 'type': 'special', 'cooldown': 3, 'special_effects': {'type': 'blind', 'duration': 2, 'effect': 'greatly_reduces_accuracy'}}
                ]
            }
        },
        'constructs': {
            'iron_sentinel': {
                'name': 'Iron Sentinel', 'type': 'constructs', 'symbol': 'S', 'color': 'gray',
                'description': 'A towering construct of iron and steel, built to guard ancient secrets.',
                'creature_type': 'tank', 'level': 2,
                'base_stats': {'might': 10, 'agility': 3, 'cunning': 4, 'vitality': 12, 'ferocity': 6, 'mysticism': 5},
                'exp_reward': 40,
                'drop_chances': {'weapons': 0.20, 'armor': 0.40, 'shields': 0.35, 'potions': 0.15},
                'attacks': [
                    {'name': 'Iron Fist', 'damage_formula': 'might * 3 + vitality * 1', 'accuracy_formula': '70 + might * 1', 'description': 'Pounds with massive metal fists', 'type': 'special', 'cooldown': 1, 'special_effects': {'type': 'armor_break', 'duration': 2, 'effect': 'reduces_defense'}},
                    {'name': 'Guard Stance', 'damage_formula': 'vitality * 1', 'accuracy_formula': '85 + vitality * 2', 'description': 'Takes a defensive position and counterattacks', 'type': 'special', 'cooldown': 3, 'special_effects': {'type': 'defensive_counter', 'duration': 2, 'effect': 'increases_defense_counters_attacks'}}
                ]
            },
            'war_golem': {
                'name': 'War Golem', 'type': 'constructs', 'symbol': 'G', 'color': 'brown',
                'description': 'A massive stone golem carved with ancient runes of war and destruction.',
                'creature_type': 'brute', 'level': 3,
                'base_stats': {'might': 14, 'agility': 2, 'cunning': 6, 'vitality': 16, 'ferocity': 8, 'mysticism': 7},
                'exp_reward': 70, 'multi_attack': {'chance': 0.30, 'max_attacks': 2},
                'drop_chances': {'weapons': 0.15, 'armor': 0.50, 'shields': 0.40, 'potions': 0.10},
                'attacks': [
                    {'name': 'Earthshaker', 'damage_formula': 'might * 3 + vitality * 2', 'accuracy_formula': '75 + might * 1', 'description': 'Pounds the ground with tremendous force', 'type': 'special', 'cooldown': 2, 'special_effects': {'type': 'tremor', 'duration': 2, 'effect': 'reduces_accuracy_and_speed'}},
                    {'name': 'Rune Blast', 'damage_formula': 'mysticism * 3 + cunning * 2', 'accuracy_formula': '80 + mysticism * 1', 'description': 'Ancient runes flare with magical energy', 'type': 'special', 'cooldown': 3, 'special_effects': {'type': 'magic_damage', 'effect': 'ignores_all_armor'}}
                ]
            }
        },
        'abyssal': {
            'void_stalker': {
                'name': 'Void Stalker', 'type': 'abyssal', 'symbol': 'V', 'color': 'black',
                'description': 'A creature from the void between worlds, existing partially outside reality.',
                'creature_type': 'swarm', 'level': 2,
                'base_stats': {'might': 5, 'agility': 11, 'cunning': 8, 'vitality': 5, 'ferocity': 9, 'mysticism': 10},
                'exp_reward': 35,
                'drop_chances': {'weapons': 0.30, 'armor': 0.20, 'shields': 0.25, 'potions': 0.35},
                'attacks': [
                    {'name': 'Void Slash', 'damage_formula': 'mysticism * 2 + agility * 1', 'accuracy_formula': '85 + agility * 1', 'description': 'Slashes with claws that cut through reality', 'type': 'special', 'cooldown': 1, 'special_effects': {'type': 'void_damage', 'effect': 'ignores_partial_armor'}},
                    {'name': 'Phase Step', 'damage_formula': 'agility * 2 + cunning * 1', 'accuracy_formula': '90 + mysticism * 1', 'description': 'Steps through dimensions to strike', 'type': 'special', 'cooldown': 2, 'special_effects': {'type': 'dimensional_strike', 'effect': 'cannot_be_blocked_or_dodged'}}
                ]
            },
                        'chaos_spawn': {
                'name': 'Chaos Spawn', 'type': 'abyssal', 'symbol': 'C', 'color': 'magenta',
                'description': 'A twisted amalgamation of flesh and magic, constantly shifting form.',
                'creature_type': 'caster', 'level': 3,
                'base_stats': {'might': 7, 'agility': 6, 'cunning': 9, 'vitality': 8, 'ferocity': 10, 'mysticism': 12},
                'exp_reward': 55,
                'drop_chances': {'weapons': 0.35, 'armor': 0.30, 'shields': 0.20, 'potions': 0.40},
                'attacks': [
                    {'name': 'Chaos Bolt', 'damage_formula': 'mysticism * 2 + cunning * 1', 'accuracy_formula': '80 + mysticism * 1', 'description': 'Hurls unpredictable magical energy', 'type': 'magical', 'cooldown': 0},
                    {'name': 'Reality Warp', 'damage_formula': 'mysticism * 3 + ferocity * 1', 'accuracy_formula': '75 + cunning * 2', 'description': 'Warps reality to inflict chaotic damage', 'type': 'special', 'cooldown': 3, 'special_effects': {'type': 'chaos_damage', 'effect': 'random_damage_type'}}
                ]
            }
        }
    }

    @classmethod
    def get_all_categories(cls):
        """Get all available monster categories"""
        return list(cls.MONSTERS.keys())
    
    @classmethod
    def get_monsters_in_category(cls, category):
        """Get all monster types in a specific category"""
        return list(cls.MONSTERS.get(category, {}).keys())
    
    @classmethod
    def get_all_monster_types(cls):
        """Get all available monster types with their categories"""
        all_types = []
        for category, monsters in cls.MONSTERS.items():
            for monster_type in monsters.keys():
                all_types.append((category, monster_type))
        return all_types
    
    @classmethod
    def get_random_monster_by_difficulty(cls, min_exp=0, max_exp=float('inf')):
        """Get a random monster within exp reward range"""
        valid_monsters = []
        for category, monsters in cls.MONSTERS.items():
            for monster_type, data in monsters.items():
                # Check both new and legacy stat formats
                if 'legacy_stats' in data:
                    exp_reward = data['legacy_stats']['exp_reward']
                elif 'stats' in data:
                    exp_reward = data['stats']['exp_reward']
                else:
                    exp_reward = 10  # Default fallback
                    
                if min_exp <= exp_reward <= max_exp:
                    valid_monsters.append((category, monster_type))
        
        if not valid_monsters:
            # Fallback to skeleton if no monsters match criteria
            return ("undead", "skeleton")
        
        import random
        return random.choice(valid_monsters)
    
    @classmethod
    def get_monsters_by_difficulty_tier(cls, tier="easy"):
        """Get monsters by difficulty tier based on exp reward"""
        tiers = {
            "easy": (0, 20),      # 0-20 exp
            "medium": (21, 40),   # 21-40 exp  
            "hard": (41, 60),     # 41-60 exp
            "boss": (61, 999)     # 61+ exp
        }
        
        min_exp, max_exp = tiers.get(tier, (0, 20))
        monsters = []
        
        for category, monster_dict in cls.MONSTERS.items():
            for monster_type, data in monster_dict.items():
                # Check both new and legacy stat formats
                if 'legacy_stats' in data:
                    exp_reward = data['legacy_stats']['exp_reward']
                elif 'stats' in data:
                    exp_reward = data['stats']['exp_reward']
                else:
                    exp_reward = 10  # Default fallback
                    
                if min_exp <= exp_reward <= max_exp:
                    monsters.append((category, monster_type))
        
        return monsters
    
    @classmethod
    def get_random_monster_by_tier(cls, tier="easy"):
        """Get a random monster from a specific difficulty tier"""
        monsters = cls.get_monsters_by_difficulty_tier(tier)
        if not monsters:
            return ("undead", "skeleton")  # Fallback
        
        import random
        return random.choice(monsters)
    
    @classmethod
    def monster_exists(cls, category, monster_type):
        """Check if a specific monster exists in the database"""
        return category in cls.MONSTERS and monster_type in cls.MONSTERS[category]
