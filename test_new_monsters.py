#!/usr/bin/env python3
"""Test the new monsters and level-based spawning system"""

from game.monsters.monsters import MonsterManager
from game.monsters.monster_database import MonsterDatabase
import random

def test_new_monsters():
    """Test spawning of new monsters"""
    print("=== TESTING LEVEL-BASED SPAWNING WITH NEW MONSTERS ===")
    print()

    mm = MonsterManager()

    # Test spawning for level 1 player (more variety now!)
    print("Spawning 15 monsters for Level 1 Player:")
    levels = []
    names = []

    for i in range(15):
        # Use the level-based spawning system (80% level 1, 20% level 2)
        if random.random() < 0.8:
            target_level = 1
        else:
            target_level = 2
        
        category, monster_type = MonsterDatabase.get_random_monster_by_level(target_level)
        monster_data = MonsterDatabase.MONSTERS[category][monster_type]
        monster_level = monster_data.get('level', 1)
        monster_name = monster_data['name']
        
        levels.append(monster_level)
        names.append(monster_name)
        print(f"  {i+1:2d}. {monster_name} (Level {monster_level})")

    # Show distribution
    level_counts = {}
    for level in levels:
        level_counts[level] = level_counts.get(level, 0) + 1

    print()
    print("Level Distribution:")
    same_level = level_counts.get(1, 0)
    higher_level = level_counts.get(2, 0)
    print(f"  Level 1: {same_level}/15 ({same_level/15*100:.1f}%)")
    print(f"  Level 2: {higher_level}/15 ({higher_level/15*100:.1f}%)")
    print()
    print("Target: ~80% Level 1, ~20% Level 2")

def show_monster_details():
    """Show details of the new monsters"""
    print("\n=== NEW MONSTER DETAILS ===")
    
    new_monsters = [
        ('beasts', 'cave_spider'),
        ('constructs', 'animated_armor'),
        ('humanoid', 'goblin_raider'),
        ('arcane', 'lightning_elemental'),
        ('humanoid', 'orc_berserker')
    ]
    
    for category, monster_type in new_monsters:
        monster_data = MonsterDatabase.MONSTERS[category][monster_type]
        print(f"\n{monster_data['name']} (Level {monster_data['level']}):")
        print(f"  Description: {monster_data['description']}")
        print(f"  Type: {monster_data['creature_type']}")
        print(f"  Symbol: '{monster_data['symbol']}' (Color: {monster_data['color']})")
        print(f"  EXP Reward: {monster_data['exp_reward']}")
        print(f"  Attacks: {len(monster_data['attacks'])}")
        for attack in monster_data['attacks']:
            print(f"    - {attack['name']}: {attack['description']}")

if __name__ == "__main__":
    test_new_monsters()
    show_monster_details()
