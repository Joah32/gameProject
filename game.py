"""
This file runs the main game loop.
It tracks player stats and calls functions from the gamefunctions module.
"""
import gamefunctions

def main():
    """Main game loop"""
    player_name = input("What is your name? ")
    gamefunctions.print_welcome(player_name, 50)

    player_hp = 30
    player_max_hp = 30  
    player_gold = 10
    player_power = 5    
    
    # New: Inventory and Equipped Item
    # The inventory will hold dictionaries representing items
    player_inventory = []
    # This will hold the currently equipped weapon (or an empty dict/None)
    equipped_weapon = {} 

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
            print(f"Equipped Weapon: {equipped_weapon['name'].capitalize()} (Durability: {equipped_weapon['currentDurability']}/{equipped_weapon['maxDurability']})")
        else:
             print("Equipped Weapon: None")

        print("\nWhat would you like to do?")
        print("  1) Leave town (Fight Monster)")
        print("  2) Sleep (Restore HP for 5 Gold)")
        print("  3) Visit Shop") # New Menu Option
        print("  4) Equip Item") # New Menu Option
        print("  5) Quit")       # Renumbered
        
        #Validate User input
        choice = input("Enter your choice (1-5): ")

        #Handle User Choice
        if choice == "1":
            # Pass inventory and equipped item to fight handler
            player_hp, player_gold, equipped_weapon, player_inventory = gamefunctions.handle_fight(
                player_hp=player_hp,
                player_gold=player_gold,
                player_power=player_power,
                equipped_weapon=equipped_weapon,  # New parameter
                player_inventory=player_inventory # New parameter
            )
            
        elif choice == "2":
            # Call the sleep function
            player_hp, player_gold = gamefunctions.handle_sleep(
                player_hp=player_hp,
                player_gold=player_gold,
                max_hp=player_max_hp,
                sleep_cost=5
            )

        elif choice == "3":
            # Call the new shop function
            player_gold, player_inventory = gamefunctions.handle_shop(
                player_gold=player_gold,
                player_inventory=player_inventory
            )
            
        elif choice == "4":
            # Call the new equip function
            equipped_weapon, player_inventory = gamefunctions.handle_equip(
                player_inventory=player_inventory,
                equipped_weapon=equipped_weapon
            )

        elif choice == "5":
            # Quit the game
            print(f"\nGoodbye, {player_name}!")
            break 

        else:
            # Handle invalid input
            print("\nInvalid choice. Please enter 1, 2, 3, 4, or 5.")

# Run the main function when the script is executed
if __name__ == "__main__":
    main()