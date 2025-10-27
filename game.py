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
        print("\nWhat would you like to do?")
        print("  1) Leave town (Fight Monster)")
        print("  2) Sleep (Restore HP for 5 Gold)")
        print("  3) Quit")
        
        #Validate User input
        choice = input("Enter your choice (1-3): ")

        #Handle User Choice
        if choice == "1":
            # Call the fight function
            # Returns updated stats
            player_hp, player_gold = gamefunctions.handle_fight(
                player_hp=player_hp,
                player_gold=player_gold,
                player_power=player_power
            )
            
        elif choice == "2":
            # Call the sleep function
            # Refreshes health and charges gold
            player_hp, player_gold = gamefunctions.handle_sleep(
                player_hp=player_hp,
                player_gold=player_gold,
                max_hp=player_max_hp,
                sleep_cost=5
            )

        elif choice == "3":
            # Quit the game
            print(f"\nGoodbye, {player_name}!")
            break 

        else:
            # Handle invalid input
            print("\nInvalid choice. Please enter 1, 2, or 3.")

# Run the main function when the script is executed
if __name__ == "__main__":
    main()