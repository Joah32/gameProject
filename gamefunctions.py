""" This program provides several functions for game

there is a function for purchasing an item, generating a monster, 
and printing a shop and welcome"""
import random
import sys 
#this function is for purchasing items
def purchase_item(itemPrice: int, startingMoney: int, quantityToPurchase: int = 1,): 
    """This function controls item purchases, verifies the item can be afforded and returns a purchase quantity and leftover money"""  
    #error condition
    if itemPrice <= 0:
        return 0, startingMoney
    #how much does the quantity cost
    total_cost_quant = itemPrice * quantityToPurchase
    #can afford
    if total_cost_quant <= startingMoney:
        quantity_purchased = quantityToPurchase
        leftover_money = startingMoney - total_cost_quant
    #too broke, how many can you afford
    else: 
        quantity_purchased = startingMoney // itemPrice
        cost_purchased = quantity_purchased * itemPrice
        leftover_money = startingMoney - cost_purchased
    #what just happened
    return quantity_purchased, leftover_money 

#this function is for a random monster 
def new_random_monster():
    """This makes a monster that has randomized health power and money"""
    monster_types = [ 
        {'name': 'Goblin',
         'description': 'A goblin who looks unhappy you are here',
         'health_range': (15, 30),
         'power_range': (5, 10),
         'money_range': (25,50)},
        {'name': 'Vulture',
         'description':'A smelly angry bird',
         'health_range': (5, 10),
         'power_range': (1, 5),
         'money_range': (5,10)},
         {'name': 'Troll',
         'description':'A large blue creature with a giant club',
         'health_range': (50, 100),
         'power_range': (30, 50),
         'money_range': (75,100)}]
    #choose a monster
    monster_data = random.choice(monster_types)
    health = random.randint(*monster_data['health_range'])
    power = random.randint(*monster_data['power_range'])
    base_money = random.randint(*monster_data['money_range'])
    money_modifier = random.random() * 0.2 + 0.9
    money = int(base_money * money_modifier)
    #put the random monster in a dictionary
    new_monster = {
        'name': monster_data['name'],
        'description': monster_data['description'],
        'health': health,
        'power' : power,
        'money': money
            }
    return new_monster
def print_welcome(name: str, width: int) -> None:
    """This function prints a centered welcome with a provided name"""
    message = f"Hello, {name}!"
    print(message.center(width))
    
def print_shop_menu(item1Name: str, item1Price: float, item2Name: str, item2Price: float) -> None:
    """prints a formatted bordered menu for two items and their prices"""
    print(",_______________________,")
    price1_str = f"${item1Price:.2f}"
    print(f"| {item1Name:<12}{price1_str:>8} |")
    price2_str = f"${item2Price:.2f}"
    print(f"| {item2Name:<12}{price2_str:>8} |")
    print(",_______________________,")
"""This function calls tests for the game functions above"""
def test_functions():
#this part will be a demonstration 
    print("---Demonstration of purchase_item---")
    #Shop Demo 1 using default quantity
    price_1 = 341
    money_1 = 2112
    print(f"\nTest 1: Price=${price_1}, Money=${money_1}, Purchase Quantity: Default (1)")
    num_purchased_1, leftover_money_1 = purchase_item(price_1, money_1)
    print(f"Items Purchased: {num_purchased_1}")
    print(f"Money Remaining: {leftover_money_1}")
    #Shop Demo 2 attempting to purchase too much
    price_2 = 123
    money_2 = 201
    quantity_2 = 3
    print(f"\nTest 2: Price=${price_2}, Money=${money_2}, Purchase Quantity: {quantity_2}")
    num_purchased_2, leftover_money_2 = purchase_item(price_2, money_2, quantity_2)
    print(f"Items Purchased: {num_purchased_2}")
    print(f"Money Remaining: {leftover_money_2}")
    #shop Demo 3 succesful full purchase
    price_3 = 123
    money_3 = 1000
    quantity_3 = 3
    print(f"\nTest 3: Price=${price_3}, Money=${money_3}, Purchase Quantity: {quantity_3}")
    num_purchased_3, leftover_money_3 = purchase_item(price_3, money_3, quantity_3)
    print(f"Items Purchased: {num_purchased_3}")
    print(f"Money Remaining: {leftover_money_3}")
    #Random monster demonstration
    print("---Demonstration of purchase_item---")
    #1st monster
    monster_a = new_random_monster()
    print("\nMonster A:")
    print(f"Name: {monster_a['name']}")
    print(f"Description: {monster_a['description']}")
    print(f"Health: {monster_a['health']}")
    print(f"Power: {monster_a['power']}")
    print(f"Money Drop: {monster_a['money']}")
    #2nd monster
    monster_b = new_random_monster()
    print("\nMonster B:")
    print(f"Name: {monster_b['name']}")
    print(f"Description: {monster_b['description']}")
    print(f"Health: {monster_b['health']}")
    print(f"Power: {monster_b['power']}")
    print(f"Money Drop: {monster_b['money']}")
    #3rd monster
    monster_c = new_random_monster()
    print("\nMonster C:")
    print(f"Name: {monster_c['name']}")
    print(f"Description: {monster_c['description']}")
    print(f"Health: {monster_c['health']}")
    print(f"Power: {monster_c['power']}")
    print(f"Money Drop: {monster_c['money']}")
    # shop menu examples
    print("--- Differing Item Name Lengths ---")
    print_shop_menu("Apples", 1.5, "Watermelon", 4.0)

    print("\n--- Differing Price Precisions ---")
    print_shop_menu("Milk", 3, "Bread", 2.349)
def display_fight_stats(player_hp: int, monster_name: str, monster_hp: int) -> None:
    """Shows player and monster HP during a fight"""
    print("-" * 20)
    print(f"Your HP: {player_hp}")
    print(f"{monster_name}'s HP: {monster_hp}")
    print("-" * 20)
def get_fight_action() -> str:
    """Asks the user for their action during a fight 
    and returns the choice."""
    print("What will you do?")
    print("  1) Fight")
    print("  2) Run")
    action = input("Enter your choice (1-2): ")
    return action
def handle_fight_turn(player_hp: int, player_power: int, monster_hp: int, monster_power: int, monster_name: str) -> tuple[int, int]:
    """ Does some math to handle one turn of combat, 
    returns new health values for player and monster
    """
    # Player's turn
    monster_hp -= player_power
    print(f"You attack the {monster_name}, dealing {player_power} damage.")

    # Monsters turn
    if monster_hp > 0:
        player_hp -= monster_power
        print(f"The {monster_name} attacks you, dealing {monster_power} damage.")
    
    return player_hp, monster_hp
def handle_fight_end(player_hp: int, player_gold: int, monster_hp: int, monster_name: str, monster_gold: int) -> tuple[int, int]:
    """
    This happens at the end of a fight
    """
    #Player loses
    if player_hp <= 0:
        print(f"The {monster_name} defeated you.")
    #Player wins       
    elif monster_hp <= 0:
        print(f"\nYou defeated the {monster_name}!")
        player_gold += monster_gold
        print(f"You found {monster_gold} gold! You now have {player_gold} gold.")
    
    print("You return to town.")
    return player_hp, player_gold
def handle_fight(player_hp: int, player_gold: int, player_power: int) -> tuple[int, int]:
    """
    Manages a single fight 
    Generates a monster and runs the fight loop
    Returns the player's updated HP and gold after the fight
    """
    #Make a monster
    monster = new_random_monster()
    monster_hp = monster['health']
    monster_power = monster['power']
    
    print(f"\nYou leave town and encounter a {monster['name']}!")
    print(f"> {monster['description']}")

    #fight loop
    while player_hp > 0 and monster_hp > 0:
        
        display_fight_stats(player_hp, monster['name'], monster_hp)
        user_action = get_fight_action()

        if user_action == "1":
            # Call the turn handler
            player_hp, monster_hp = handle_fight_turn(
                player_hp, player_power, 
                monster_hp, monster_power, monster['name']
            )
        elif user_action == "2":
            print("\nYou successfully ran away!")
            break  # Exit the 'while' loop
        else:
            print("\nUnrecognized command. Try again.")

    #end fight
    player_hp, player_gold = handle_fight_end(
        player_hp, player_gold, 
        monster_hp, monster['name'], monster['money']
    )
    
    # Return new gold and HP
    return player_hp, player_gold
def handle_sleep(player_hp: int, player_gold: int, max_hp: int, sleep_cost: int) -> tuple[int, int]:
    """
    Function for sleeping, 
    returns refreshed HP and reduced gold
    """
    if player_gold >= sleep_cost:
        if player_hp == max_hp:
            print("\nYou are already at full health.")
        else:
            player_gold -= sleep_cost
            player_hp = max_hp
            print(f"\nYou sleep and feel better.\n Your health is restored to {max_hp} HP.")
            print(f"You paid {sleep_cost} gold and have {player_gold} gold remaining.")
    else:
        print(f"\nYou need {sleep_cost} gold to sleep, but you only have {player_gold}.")
    return player_hp, player_gold
if __name__ == "__main__":
   test_functions()