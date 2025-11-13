"""
This file runs the main game loop.
It tracks player stats and calls functions from the gamefunctions module.
"""
import gamefunctions
import sys 
import os
DEFAULT_SAVE_FILE = "savegame.json"

def main():
    """Main game loop and game state initialization/loading."""
    print("Welcome to the Adventure Game!")
     # check for a save 
    save_exists = os.path.exists(DEFAULT_SAVE_FILE)
    
    while True:
        print("\nWhat would you like to do?")
        print("  1) Start New Game")
        if save_exists:
            print(f"  2) Load Game ({DEFAULT_SAVE_FILE})")
        
        choice = input(f"Enter your choice ({'1-2' if save_exists else '1'}): ")
        
        if choice == "1":
            # New Game Initialization
            player_name = input("What is your name? ")
            gamefunctions.print_welcome(player_name, 50)
            
            player_hp = 30
            player_max_hp = 30  
            player_gold = 10
            player_power = 5    
            player_inventory = []
            equipped_weapon = {} 
            break
            
        elif choice == "2" and save_exists:
            # Load Game
            loaded_data = gamefunctions.load_game_data(DEFAULT_SAVE_FILE)
            
            if loaded_data:
                player_name = input("What is your name? ") # Name is not saved, so we ask again
                gamefunctions.print_welcome(player_name, 50)
                
                # Load all required variables from the saved data
                player_hp = loaded_data.get('player_hp', 30)
                player_max_hp = loaded_data.get('player_max_hp', 30)
                player_gold = loaded_data.get('player_gold', 10)
                player_power = loaded_data.get('player_power', 5)
                player_inventory = loaded_data.get('player_inventory', [])
                # Handle equipped weapon which might be an empty dict if nothing was equipped
                equipped_weapon = loaded_data.get('equipped_weapon', {}) 
                
                break # Exit the startup loop
            else:
                print("Failed to load game data. Starting new game instead.")
                # We could break and start a new game or continue the loop. 
                # For safety, let's continue the loop and let the user try 1.
                continue
                
        else:
            print("\nInvalid choice. Please enter 1 or 2.")
            
    #Main Loop

    while True:
        # Dead check
        if player_hp <= 0:
            print("You have no HP left, whoops!")
            print("Do better.")
            break 

        #Menu for in town
        print("\n" + "-"*20)
        print("You are in town.")
        print(f"Current HP: {player_hp}/{player_max_hp}")
        print(f"Current Gold: {player_gold}")
        
        # Display equipped weapon if one exists
        if equipped_weapon:
            # Note: Using .get() for safe access to prevent key errors if data is malformed
            current_dur = equipped_weapon.get('currentDurability', 0)
            max_dur = equipped_weapon.get('maxDurability', 0)
            name = equipped_weapon.get('name', 'Unknown')
            print(f"Equipped Weapon: {name.capitalize()} (Durability: {current_dur}/{max_dur})")
        else:
             print("Equipped Weapon: None")

        print("\nWhat would you like to do?")
        print("  1) Leave town (Fight Monster)")
        print("  2) Sleep (Restore HP for 5 Gold)")
        print("  3) Visit Shop") 
        print("  4) Equip Item") 
        print("  5) Save and Quit") # New Menu Option
        print("  6) Quit (No Save)") # Renumbered
        
        #Validate User input
        choice = input("Enter your choice (1-6): ")

        #Handle User Choice
        if choice == "1":
            # Fight handler returns updated stats
            player_hp, player_gold, equipped_weapon, player_inventory = gamefunctions.handle_fight(
                player_hp=player_hp,
                player_gold=player_gold,
                player_power=player_power,
                equipped_weapon=equipped_weapon,  
                player_inventory=player_inventory 
            )
            
        elif choice == "2":
            # Sleep handler returns updated HP and gold
            player_hp, player_gold = gamefunctions.handle_sleep(
                player_hp=player_hp,
                player_gold=player_gold,
                max_hp=player_max_hp,
                sleep_cost=5
            )

        elif choice == "3":
            # Shop handler returns updated gold and inventory
            player_gold, player_inventory = gamefunctions.handle_shop(
                player_gold=player_gold,
                player_inventory=player_inventory
            )
            
        elif choice == "4":
            # Equip handler returns updated equipped weapon and inventory
            equipped_weapon, player_inventory = gamefunctions.handle_equip(
                player_inventory=player_inventory,
                equipped_weapon=equipped_weapon
            )

        elif choice == "5":
            # New: Save Game and Quit
            save_data = {
                'player_hp': player_hp,
                'player_max_hp': player_max_hp,
                'player_gold': player_gold,
                'player_power': player_power,
                'equipped_weapon': equipped_weapon,
                'player_inventory': player_inventory,
            }
            gamefunctions.save_game_data(DEFAULT_SAVE_FILE, save_data)
            print(f"\nGoodbye, {player_name}!")
            break 
            
        elif choice == "6":
            # Quit the game without saving
            print(f"\nGoodbye, {player_name}!")
            break 

        else:
            # Handle invalid input
            print("\nInvalid choice. Please enter 1, 2, 3, 4, 5, or 6.")

# Run the main function when the script is executed
if __name__ == "__main__":
    main()