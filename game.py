"""This file imports and executes functions from the gamefunctions module"""
import gamefunctions
def main():
    """Test loop"""
    #use user input
    player_name = input("What is your name?")
    #welcome module
    gamefunctions.print_welcome(player_name, 40)
    player_money = 100
    print(f"\nYou have {player_money} gold.")
    #Call shop function
    print("\nYou enter a shop. There are potions for sale")
    gamefunctions.print_shop_menu("Health Potion", 25.0, "Mana Potion", 15.0)

    print("\n You buy 3 health potions.")
    potions_bought, money_left = gamefunctions.purchase_item(3, player_money, 25)
    player_money = money_left
    print(f"You bought {potions_bought} potions.")
    print(f"you have {player_money} gold left")
    #call monster function
    print("\nYou encounter a monster leaving town")
    monster = gamefunctions.new_random_monster()
    print(f"A wild {monster['name']}!")
    print(f"  > It has {monster['health']} HP and {monster['power']} Power.")

if __name__ == "__main__":
    main()