"""
This file runs the main game loop.
It tracks player stats and calls functions from the gamefunctions module.
"""
import gamefunctions
import sys 
import os
import pygame

DEFAULT_SAVE_FILE = "savegame.json"

def generate_unique_pos(town_pos):
    """Generates a random position not equal to the town position."""
    # Uses random from gamefunctions to ensure it's available
    while True:
        x = gamefunctions.random.randint(0, gamefunctions.GRID_SIZE - 1)
        y = gamefunctions.random.randint(0, gamefunctions.GRID_SIZE - 1)
        if (x, y) != town_pos:
            return (x, y)

def main():
    """Main game loop and game state initialization/loading."""
    
    # Define initial map state constants
    initial_town_pos = (0, 0)
    initial_monster_pos = generate_unique_pos(initial_town_pos)
    
    # Default map state for a new game
    initial_map_state = {
        'player_pos': initial_town_pos,
        'town_pos': initial_town_pos,
        'monster_pos': initial_monster_pos,
        'moved_from_town': False
    }

    # --- 1. Startup: New Game or Load Game ---
    print("Welcome to the Adventure Game!")
    
    save_exists = os.path.exists(DEFAULT_SAVE_FILE)
    
    # Initialize variables with default (new game) values
    player_name = ""
    player_hp = 30
    player_max_hp = 30  
    player_gold = 10
    player_power = 5    
    player_inventory = []
    equipped_weapon = {} 
    current_map_state = initial_map_state

    while True:
        print("\nWhat would you like to do?")
        print("  1) Start New Game")
        if save_exists:
            print(f"  2) Load Game ({DEFAULT_SAVE_FILE})")
        
        choice = input(f"Enter your choice ({'1-2' if save_exists else '1'}): ")
        
        if choice == "1":
            # New Game Initialization (using defaults)
            player_name = input("What is your name? ")
            gamefunctions.print_welcome(player_name, 50)
            break
            
        elif choice == "2" and save_exists:
            # Load Game
            loaded_data = gamefunctions.load_game_data(DEFAULT_SAVE_FILE)
            
            if loaded_data:
                player_name = input("What is your name? ")
                gamefunctions.print_welcome(player_name, 50)
                
                # Load all required variables
                player_hp = loaded_data.get('player_hp', 30)
                player_max_hp = loaded_data.get('player_max_hp', 30)
                player_gold = loaded_data.get('player_gold', 10)
                player_power = loaded_data.get('player_power', 5)
                player_inventory = loaded_data.get('player_inventory', [])
                equipped_weapon = loaded_data.get('equipped_weapon', {}) 
                
                # Load Map State (New)
                current_map_state = loaded_data.get('map_state', initial_map_state)
                # JSON saves tuples as lists, convert back for consistency
                current_map_state['player_pos'] = tuple(current_map_state['player_pos'])
                current_map_state['town_pos'] = tuple(current_map_state['town_pos'])
                current_map_state['monster_pos'] = tuple(current_map_state['monster_pos'])
                
                break # Exit the startup loop
            else:
                print("Failed to load game data. Starting new game instead.")
                continue
                
        else:
            print("\nInvalid choice. Please enter 1 or 2.")
    
    # --- Main Game Loop ---
    while True:
        # Dead check
        if player_hp <= 0:
            print("You have no HP left, whoops!")
            print("Do better.")
            break 

        # Check if the player is at the Town's position
        is_at_town = current_map_state['player_pos'] == current_map_state['town_pos']

        # --- Determine Action Source (Town Menu vs Auto-Explore) ---
        if is_at_town:
            # Show Town Menu
            print("\n" + "-"*20)
            print("You are in town.")
            print(f"Current HP: {player_hp}/{player_max_hp}")
            print(f"Current Gold: {player_gold}")
            
            # Display equipped weapon if one exists
            if equipped_weapon:
                current_dur = equipped_weapon.get('currentDurability', 0)
                max_dur = equipped_weapon.get('maxDurability', 0)
                name = equipped_weapon.get('name', 'Unknown')
                print(f"Equipped Weapon: {name.capitalize()} (Durability: {current_dur}/{max_dur})")
            else:
                 print("Equipped Weapon: None")

            print("\nWhat would you like to do?")
            print("  1) Leave town (Explore Map)") 
            print("  2) Sleep (Restore HP for 5 Gold)")
            print("  3) Visit Shop") 
            print("  4) Equip Item") 
            print("  5) Save and Quit")
            print("  6) Quit (No Save)")
            
            # Validate User input
            choice = input("Enter your choice (1-6): ")
        else:
            # If not in town, automatically set choice to "1" to trigger map exploration
            choice = "1"


        # --- Handle User Choice (Common logic for map action or town actions) ---
        if choice == "1":
            # Map/Explore/Continue
            
            #Call the map
            action, current_map_state = gamefunctions.handle_map(current_map_state)
            
            if action == gamefunctions.ACTION_QUIT:
                 print("\nGame closed abruptly.")
                 break
            
            if action == gamefunctions.ACTION_MONSTER_ENCOUNTER:
                #Monster Encounter logic
                print("\nA monster has appeared!")
                player_hp, player_gold, equipped_weapon, player_inventory = gamefunctions.handle_fight(
                    player_hp=player_hp,
                    player_gold=player_gold,
                    player_power=player_power,
                    equipped_weapon=equipped_weapon,
                    player_inventory=player_inventory
                )
                #After the fight/flee, spawn a new monster elsewhere
                current_map_state['monster_pos'] = generate_unique_pos(current_map_state['town_pos'])
                
                # Loop continues immediately, sending player back to map (because is_at_town is False)
                continue

        elif choice == "2" and is_at_town:
            # Sleep handler 
            player_hp, player_gold = gamefunctions.handle_sleep(
                player_hp=player_hp,
                player_gold=player_gold,
                max_hp=player_max_hp,
                sleep_cost=5
            )

        elif choice == "3" and is_at_town:
            # Shop handler
            player_gold, player_inventory = gamefunctions.handle_shop(
                player_gold=player_gold,
                player_inventory=player_inventory
            )
            
        elif choice == "4" and is_at_town:
            # Equip handler
            equipped_weapon, player_inventory = gamefunctions.handle_equip(
                player_inventory=player_inventory,
                equipped_weapon=equipped_weapon
            )

        elif choice == "5" and is_at_town:
            # Save Game and Quit 
            save_data = {
                'player_hp': player_hp,
                'player_max_hp': player_max_hp,
                'player_gold': player_gold,
                'player_power': player_power,
                'equipped_weapon': equipped_weapon,
                'player_inventory': player_inventory,
                'map_state': current_map_state 
            }
            gamefunctions.save_game_data(DEFAULT_SAVE_FILE, save_data)
            print(f"\nGoodbye, {player_name}!")
            break 
            
        elif choice == "6" and is_at_town:
            # Quit the game without saving
            print(f"\nGoodbye, {player_name}!")
            break 
            
        else:
            # Handle invalid input
            print("\nInvalid choice. Please enter a valid number.")

# Run the main function when the script is executed
if __name__ == "__main__":
    main()