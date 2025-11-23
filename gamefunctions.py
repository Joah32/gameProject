""" This program provides several functions for game

there is a function for purchasing an item, generating a monster, 
and printing a shop and welcome"""
import random
import sys 
import json
import os
from typing import Union
import pygame
import wanderingMonster

GRID_SIZE = 10
TILE_SIZE = 32
SCREEN_WIDTH = GRID_SIZE * TILE_SIZE
SCREEN_HEIGHT = GRID_SIZE * TILE_SIZE
ACTION_RETURN_TO_TOWN = "return_to_town"
ACTION_MONSTER_ENCOUNTER = "monster_encounter"
ACTION_QUIT = "quit"
def save_game_data(filename: str, player_data: dict) -> None:
    """Saves the game"""
    try:
        with open(filename, 'w') as f:
            json.dump(player_data, f, indent=4)
        print(f"\nGame successfully saved to '{filename}'.")
    except IOError as e:
        print(f"\nError saving game: {e}") 
def load_game_data(filename: str) -> Union[dict, None]:
    """
   Loads the game and provides fail condition 
    """
    if not os.path.exists(filename):
        return None
    
    try:
        with open(filename, 'r') as f:
            player_data = json.load(f)
        print(f"\nGame successfully loaded from '{filename}'.")
        return player_data
    except json.JSONDecodeError:
        print(f"\nError: The file '{filename}' is corrupted or not a valid JSON file.")
        return None
    except IOError as e:
        print(f"\nError loading game: {e}")
        return None   
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
def handle_fight_turn(
    player_hp: int, 
    player_power: int, 
    monster_hp: int, 
    monster_power: int, 
    monster_name: str, 
    equipped_weapon: dict
) -> tuple[int, int, dict]:
    """ 
    Does some math for one turn of combat, 
    returns updated health values for player and monster, and the updated equipped_weapon.
    """
    
    # Apply weapon bonus damage
    weapon_bonus = 0
    if equipped_weapon:
        # Check if it has a damage bonus and durability
        if 'damageBonus' in equipped_weapon and equipped_weapon['currentDurability'] > 0:
            weapon_bonus = equipped_weapon['damageBonus']
            
            # Reduce durability
            equipped_weapon['currentDurability'] -= 1
            
            if equipped_weapon['currentDurability'] == 0:
                print(f"\n*** Your {equipped_weapon['name'].capitalize()} broke! ***")
            
    
    total_player_damage = player_power + weapon_bonus
    
    # Player's turn
    monster_hp -= total_player_damage
    print(f"You attack the {monster_name}, dealing {total_player_damage} damage (Base: {player_power}, Weapon Bonus: {weapon_bonus}).")

    # Monsters turn
    if monster_hp > 0:
        player_hp -= monster_power
        print(f"The {monster_name} attacks you, dealing {monster_power} damage.")
    
    # **Return the updated equipped_weapon**
    return player_hp, monster_hp, equipped_weapon
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
    
    return player_hp, player_gold
def populate_monsters(count, town_pos):
    """Creates a list of WanderingMonster objects."""
    monsters = []
    for _ in range(count):
        m = wanderingMonster.WanderingMonster(GRID_SIZE, town_pos)
        monsters.append(m)
    return monsters

def handle_fight(
    player_hp: int, 
    player_gold: int, 
    player_power: int,
    equipped_weapon: dict,       
    player_inventory: list,
    monster: dict 
) -> tuple[int, int, dict, list, bool]:
    """
    Manages a single fight with a specific monster.
    Returns updated stats and a boolean indicating if the monster was defeated.
    """
    
    # Use attributes from the passed monster object
    monster_hp = monster.health
    monster_power = monster.power
    monster_name = monster.name
    monster_desc = monster.description
    monster_money = monster.money
    
    print(f"\nYou encounter a {monster_name}!")
    print(f"> {monster_desc}")
    
    # Check for consumables that instantly end the fight
    smoke_bomb_index = next(
        (i for i, item in enumerate(player_inventory) if item.get('name') == 'smoke_bomb'), 
        -1
    )

    # fight loop
    while player_hp > 0 and monster_hp > 0:
        
        display_fight_stats(player_hp, monster_name, monster_hp)
        
        print("What will you do?")
        print("  1) Fight")
        print("  2) Run")
        
        has_smoke_bomb = smoke_bomb_index != -1
        
        if has_smoke_bomb:
            print("  3) Use Smoke Bomb (Defeat Monster)")
            user_action = input("Enter your choice (1-3): ")
        else:
            user_action = input("Enter your choice (1-2): ")
            

        if user_action == "1":
            # Call the turn handler
            player_hp, monster_hp, equipped_weapon = handle_fight_turn(
                player_hp, player_power, 
                monster_hp, monster_power, monster_name,
                equipped_weapon 
            )
            
        elif user_action == "2":
            print("\nYou successfully ran away!")
            break 
            
        elif user_action == "3" and has_smoke_bomb:
            print(f"\nYou threw a Smoke Bomb! The {monster_name} is confused and defeated!")
            player_inventory.pop(smoke_bomb_index)
            monster_hp = 0
            break
            
        else:
            print("\nUnrecognized command. Try again.")
    
    # If the equipped weapon broke during the fight, unequip it here.
    if equipped_weapon and equipped_weapon['currentDurability'] <= 0:
        print(f"You unequip the broken {equipped_weapon['name'].capitalize()}.")
        equipped_weapon = {} 
    
    # end fight
    player_hp, player_gold = handle_fight_end(
        player_hp, player_gold, 
        monster_hp, monster_name, monster_money
    )
    
    # Return updated gold, HP, equipped_weapon, inventory, and win status
    return player_hp, player_gold, equipped_weapon, player_inventory, monster_hp <= 0
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
# This dictionary stores the base stats for the items in the shop
ITEM_TEMPLATES = {
    "sword": {
        "name": "sword", 
        "type": "weapon", 
        "maxDurability": 15, 
        "currentDurability": 15, 
        "damageBonus": 5
    },
    "smoke_bomb": {
        "name": "smoke_bomb", 
        "type": "consumable", 
        "note": "A thick smoke that helps you escape a difficult fight."
    }
}
# This dictionary stores the base stats for the items in the shop
SHOP_INVENTORY = [
    {"template_key": "sword", "price": 30, "display_name": "A Shiny Sword"},
    {"template_key": "smoke_bomb", "price": 10, "display_name": "Smoke Bomb"}
]
def handle_shop(player_gold: int, player_inventory: list) -> tuple[int, list]:
    """
    Manages the shop interface for purchasing items.
    Returns the updated player_gold and player_inventory.
    """
    
    while True:
        print("\n" + "="*30)
        print("Welcome to the Shop!")
        print(f"Your Gold: {player_gold}")
        
        # Display shop items
        print("\nAvailable Items:")
        for i, item in enumerate(SHOP_INVENTORY):
            # Using the item's display name and price
            print(f"  {i+1}) {item['display_name']} - {item['price']} Gold")
        print("  0) Exit Shop")
        print("="*30)

        # Get and validate choice
        choice = input("Enter the number of the item to buy (or 0 to exit): ")
        
        if choice == "0":
            break
        
        if choice.isdigit():
            item_index = int(choice) - 1
            
            if 0 <= item_index < len(SHOP_INVENTORY):
                # Get the item info
                shop_item = SHOP_INVENTORY[item_index]
                item_price = shop_item['price']
                item_key = shop_item['template_key']
                
                # Use the existing purchase_item function (quantity=1)
                quantity_purchased, new_gold = purchase_item(
                    itemPrice=item_price, 
                    startingMoney=player_gold, 
                    quantityToPurchase=1
                )

                if quantity_purchased > 0:
                    player_gold = new_gold
                    # Create a deep copy of the item template to add to inventory
                    new_item = ITEM_TEMPLATES[item_key].copy()
                    player_inventory.append(new_item)
                    print(f"\n**Purchased {shop_item['display_name']}!** It's yours now!.")
                    print(f"Remaining Gold: {player_gold}")
                else:
                    print(f"\nNot enough gold! You need {item_price} gold for that item.")
            else:
                print("\nInvalid selection number.")
        else:
            print("\nInvalid input. Please enter a number.")
            
    print("\nThanks for shopping!")
    return player_gold, player_inventory
def handle_equip(player_inventory: list, equipped_weapon: dict) -> tuple[dict, list]:
    """
    Handles equipping a 'weapon' item from the inventory.
    Returns the updated equipped_weapon and player_inventory.
    """
    
    item_type_to_equip = "weapon"
    
    #Find all equipable items in inventory
    equipable_items = [
        item for item in player_inventory 
        if item.get("type") == item_type_to_equip
    ]
    
    if not equipable_items:
        print(f"\nYou have no {item_type_to_equip}s to equip.")
        return equipped_weapon, player_inventory
    
    while True:
        print("\n--- Equip Weapon ---")
        print(f"Currently Equipped: {equipped_weapon.get('name', 'None').capitalize()}")

        #Display equipable items
        print(f"\nAvailable {item_type_to_equip.capitalize()}s:")
        for i, item in enumerate(equipable_items):
            display_name = item['name'].capitalize()
            # Special check for durability items
            if 'currentDurability' in item:
                display_name += f" (Durability: {item['currentDurability']}/{item['maxDurability']})"
            
            print(f"  {i+1}) {display_name}")
        
        print("  0) Unequip Current Weapon")
        print("  -1) Back to Town Menu")
        print("-" * 20)

        choice = input(f"Enter the number of the {item_type_to_equip} to equip (or 0/-1): ")

        if choice == "-1":
            return equipped_weapon, player_inventory
        
        if choice == "0":
            if equipped_weapon:
                print(f"\n{equipped_weapon['name'].capitalize()} has been unequipped.")
                equipped_weapon = {}
            else:
                print("\nNothing is currently equipped.")
            continue # Go back to the equip menu

        if choice.isdigit():
            item_index = int(choice) - 1
            
            if 0 <= item_index < len(equipable_items):
                item_to_equip = equipable_items[item_index]
                
                #Equip the item
                equipped_weapon = item_to_equip 
                print(f"\n**{equipped_weapon['name'].capitalize()} is now equipped!**")
                return equipped_weapon, player_inventory
            else:
                print("\nInvalid selection number.")
        else:
            print("\nInvalid input. Please enter a number.")
def handle_map(map_state: dict) -> tuple[str, dict]:
    """
    Initializes and runs the Pygame map screen.
    Handles movement, drawing, and encounter/return logic.
    Returns the action taken and the updated map state.
    """
    
    # Initialize Pygame if not already initialized
    if not pygame.get_init():
        try:
            pygame.init()
        except pygame.error as e:
            print(f"Pygame initialization failed: {e}")
            print("Cannot display map. Returning to town menu.")
            return ACTION_RETURN_TO_TOWN, map_state

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("World Map")
    # Extract locations from state
    player_x, player_y = map_state['player_pos']
    town_x, town_y = map_state['town_pos']
    monsters = map_state['monsters']
    
    running = True
    action = None # Default action if window is closed by 'X'

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # User hit the 'x' button, resulting in abrupt exit
                action = ACTION_QUIT
                running = False
            
            if event.type == pygame.KEYDOWN:
                dx, dy = 0, 0
                
                # Handle Movement
                if event.key == pygame.K_UP:
                    dy = -1
                elif event.key == pygame.K_DOWN:
                    dy = 1
                elif event.key == pygame.K_LEFT:
                    dx = -1
                elif event.key == pygame.K_RIGHT:
                    dx = 1
                
                #Calculate new potential position
                new_x = player_x + dx
                new_y = player_y + dy
                #Clamp position to grid bounds (0 to GRID_SIZE - 1)
                if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
                    player_x = new_x
                    player_y = new_y
                    
                    #Player-initiated Encounter Check
                    #Check if player moved onto a monster's square
                    for monster in monsters:
                        if (player_x, player_y) == monster.get_pos():
                            map_state['active_encounter'] = monster
                            action = ACTION_MONSTER_ENCOUNTER
                            running = False
                            break #Exit monster loop
                    if not running:
                        break #Exit event loop

                    # --- Monster Movement ---
                    # Increment turn counter for each player move
                    map_state['turn_count'] += 1
                    
                    for monster in monsters:
                        # Pass the global turn count to the move function
                        monster.move((town_x, town_y), map_state['turn_count'])
                        #Monster-initiated Encounter Check
                        # Check if a monster moved onto the player's square
                        if (player_x, player_y) == monster.get_pos():
                            map_state['active_encounter'] = monster
                            action = ACTION_MONSTER_ENCOUNTER
                            running = False
                            break #Exit monster loop
                    if not running:
                        break #Exit event loop
                    
                    #Check for Town Return
                    if (player_x, player_y) == (town_x, town_y):
                        #Only return to town if they've moved away first
                        if map_state['moved_from_town']:
                            action = ACTION_RETURN_TO_TOWN
                            running = False
                        #Mark that the player has moved away from town for the first time
                    elif dx != 0 or dy != 0:
                        map_state['moved_from_town'] = True               
                            # --- Drawing ---
        screen.fill((0, 0, 0)) #Black background
        
        #Draw Grid Lines 
        line_color = (50, 50, 50)
        for i in range(GRID_SIZE):
            pygame.draw.line(screen, line_color, (i * TILE_SIZE, 0), (i * TILE_SIZE, SCREEN_HEIGHT))
            pygame.draw.line(screen, line_color, (0, i * TILE_SIZE), (SCREEN_WIDTH, i * TILE_SIZE))

        #Draw Town 
        town_center = (town_x * TILE_SIZE + TILE_SIZE // 2, town_y * TILE_SIZE + TILE_SIZE // 2)
        pygame.draw.circle(screen, (0, 150, 0), town_center, TILE_SIZE // 3)

        #Draw Monsters 
        for monster in monsters:
            monster_x, monster_y = monster.get_pos()
            if (monster_x, monster_y) != (town_x, town_y):
                 monster_center = (monster_x * TILE_SIZE + TILE_SIZE // 2, monster_y * TILE_SIZE + TILE_SIZE // 2)
                 pygame.draw.circle(screen, monster.color, monster_center, TILE_SIZE // 3)
        
        #Draw Player 
        player_rect = pygame.Rect(player_x * TILE_SIZE, player_y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(screen, (255, 255, 255), player_rect, 2) #Draw white border
        
        pygame.display.flip() #Update the full screen

    pygame.quit() #Close Pygame window
    
    #Update map state with new position before returning
    map_state['player_pos'] = (player_x, player_y)
    
    return action, map_state