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
import asteroid


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
    equipped_weapon: dict,
    total_defense: int = 0,
    monster_crit_chance: float = 0.05,
    monster_crit_multiplier: float = 1.5,
    monster_miss_chance: float = 0.05
) -> tuple[int, int, dict]:
    """ 
    Does some math for one turn of combat, 
    returns updated health values for player and monster, and the updated equipped_weapon.
    """
    # Unarmed defaults
    weapon_bonus = 0
    crit_chance = 0.05
    crit_multiplier = 1.5
    miss_chance = 0.05

    # Check equipped weapon
    if equipped_weapon and equipped_weapon.get('currentDurability', 0) > 0:
        weapon_bonus = equipped_weapon.get('damageBonus', 0)
        crit_chance = equipped_weapon.get('crit_chance', 0.05)
        crit_multiplier = equipped_weapon.get('crit_multiplier', 1.5)
        miss_chance = equipped_weapon.get('miss_chance', 0.05)
        
        # Durability/ammo reduction
        equipped_weapon['currentDurability'] -= 1    
        if equipped_weapon['currentDurability'] == 0:
             print(f"\n*** Your {equipped_weapon['name'].capitalize()} is not functional! ***")

    # Calculate Base Damage
    base_damage = player_power + weapon_bonus
    final_damage = base_damage
    
    # Roll for Crits/Misses
    hit_roll = random.random() 

    if hit_roll < miss_chance:
        # Miss
        final_damage = 0
        print(f"\nYou fired at the {monster_name}, but missed!")
        
    elif random.random() < crit_chance: 
        # Crit
        final_damage = int(base_damage * crit_multiplier)
        print(f"\nCRITICAL HIT!! You hit a weak spot!")
        print(f"You attack the {monster_name}, dealing {final_damage} damage.")
        
    else:
        # Standard Hit
        print(f"You attack the {monster_name}, dealing {final_damage} damage.")

    monster_hp -= final_damage

    # Enemy Attack Turn
    if monster_hp > 0:
        monster_damage = monster_power
        
        # Roll for Monster Hit/Miss
        hit_roll = random.random()
        
        if hit_roll < monster_miss_chance:
            monster_damage = 0
            print(f"The {monster_name} attacks, but misses you!")
            
        elif random.random() < monster_crit_chance:
            monster_damage = int(monster_power * monster_crit_multiplier)
            print(f"The {monster_name} lands a critical hit! Dealing {monster_damage} damage.")
            
        else:
            print(f"The {monster_name} attacks you, dealing {monster_damage} damage.")
        #Shield Logic    
        if monster_damage > 0:
            original_damage = monster_damage
            monster_damage = max(0, monster_damage - total_defense)
            
            if total_defense > 0 and original_damage > 0:
                print(f"   (Your shield system blocks {total_defense} damage!)")
                print(f"   ...you still take {monster_damage} damage.")
            
        player_hp -= monster_damage
      
    return player_hp, monster_hp, equipped_weapon
      
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
        print(f"You found {monster_gold} credits! You now have {player_gold} credits.")
    
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
    
    print(f"\nYou encounter a {monster_name} ship!")
    print(f"> {monster_desc}")
    
    # Check for consumables that instantly end the fight
    emp_index = next(
        (i for i, item in enumerate(player_inventory) if item.get('name') == 'emp'), 
        -1
    )
    m_crit_chance = getattr(monster, 'crit_chance', 0.05)
    m_crit_mult = getattr(monster, 'crit_multiplier', 1.5)
    m_miss_chance = getattr(monster, 'miss_chance', 0.05)
    # fight loop
    while player_hp > 0 and monster_hp > 0:
        
        display_fight_stats(player_hp, monster_name, monster_hp)
        
        print("What will you do?")
        print("  1) Fight")
        print("  2) Run")
        
        has_emp = emp_index != -1
        
        if has_emp:
            print("  3) Use EMP (Destroy Enemy)")
            user_action = input("Enter your choice (1-3): ")
        else:
            user_action = input("Enter your choice (1-2): ")
            

        if user_action == "1":
            #defense
            current_defense = 0
            for item in player_inventory:
                current_defense += item.get('defense_bonus', 0)
            # Call the turn handler
            player_hp, monster_hp, equipped_weapon = handle_fight_turn(
                player_hp, player_power, 
                monster_hp, monster_power, monster_name,
                equipped_weapon,
                total_defense=current_defense,
                monster_crit_chance=m_crit_chance,
                monster_crit_multiplier=m_crit_mult,
                monster_miss_chance=m_miss_chance 
            )
            
        elif user_action == "2":
            #make fleeing only work sometimes
            flee_chance = random.randrange(0, 100, 1)
            if flee_chance <= 80:
                print("\nYou successfully Fled!")
                break 
            else:
                print("\nYou did not get away!")
                player_hp -= monster_power
                print(f"The {monster_name} attacks you in your failed attempt to flee, dealing {monster_power} damage.")
            
        elif user_action == "3" and has_emp:
            print(f"\nYou sent an EMP! The {monster_name} ship is destroyed.")
            player_inventory.pop(emp_index)
            monster_hp = 0
            break
            
        else:
            print("\nUnrecognized command. Try again.")
    
    # If the equipped weapon broke during the fight, unequip it here.
    if equipped_weapon and equipped_weapon.get('currentDurability', 0) <= 0:
        print(f"\nYour {equipped_weapon['name'].capitalize()} has burned out!")
        print("You discard the scrap.")
        if equipped_weapon in player_inventory:
            player_inventory.remove(equipped_weapon)
        else:
            for item in player_inventory:
                if item['name'] == equipped_weapon['name']:
                    player_inventory.remove(item)
                    break
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
            print("\nYour ship already looks great.")
        else:
            player_gold -= sleep_cost
            player_hp = max_hp
            print(f"\nYou eat a sandwich while the mechanic works on your ship.\n Your health is restored to {max_hp} HP.")
            print(f"You paid {sleep_cost} credits and have {player_gold} credits remaining.")
    else:
        print(f"\nYou need {sleep_cost} credits to get repairs, but you only have {player_gold}.")
    return player_hp, player_gold
# This dictionary stores the base stats for the items in the shop
ITEM_TEMPLATES = {
    "rocket": {
        "name": "Rocket Launcher", 
        "type": "weapon", 
        "price": 30,
        "desc": "Above average crit and damage.",
        "maxDurability": 15, 
        "currentDurability": 15, 
        "damageBonus": 5,
        "crit_chance": 0.25,
        "crit_multiplier": 1.5,
        "miss_chance": .05

    },
    "laser": {
        "name": "Sighted Laser", 
        "type": "weapon", 
        "price": 50,
        "desc": "Limited uses, High Damage, High Crit, Does not miss.",
        "maxDurability": 5, 
        "currentDurability": 5, 
        "damageBonus": 8,
        "crit_chance": 0.75,
        "crit_multiplier": 2.0,
        "miss_chance": 0.0

    },
    "shield": {
        "name": "Shield System",
        "type": "passive",
        "price": 50,
        "desc": "Passive. Reduces Incoming Damage",
        "defense_bonus": 3,
        "unique": True
    },    
    "emp": {
        "name": "EMP Charge", 
        "type": "consumable", 
        "price": 10,
        "desc": "A one time use item that destroys an enemy ship",
        "note": "A electrical pulse that can disable a ship instantly."
    }
}
SHOP_KEYS = ["rocket","laser", "emp", "shield"]
def handle_shop(player_gold: int, player_inventory: list) -> tuple[int, list]:
    """
    Manages the shop interface for purchasing items.
    Returns the updated player_gold and player_inventory.
    """
    
    while True:
        print("\n" + "="*40)
        print(f"      SHOP | Credits: {player_gold}")
        print("="*40)
        
        # Display shop items from SHOP_KEYS
        print(f"{'#':<4} {'Item':<18} {'Price':<8} {'Description'}")
        print("-" * 40)
        
        for i, key in enumerate(SHOP_KEYS):
            item = ITEM_TEMPLATES.get(key)
            if item:
                name = item['name']
                price = item['price']
                desc = item.get('desc', '')
                print(f"{i+1:<4} {name:<18} {price:<8} {desc}")
                
        print("-" * 40)
        print("0)   Exit Shop")
        
        choice = input("\nEnter choice: ")
        
        if choice == "0":
            break
        
        if choice.isdigit():
            index = int(choice) - 1
            
            if 0 <= index < len(SHOP_KEYS):
                key = SHOP_KEYS[index]
                item_template = ITEM_TEMPLATES[key]
                price = item_template['price']
                is_unique = item_template.get("unique", False)
                already_owns = False
                if is_unique:
                    for inv_item in player_inventory:
                        if inv_item['name'] == item_template['name']:
                            already_owns = True
                            break
                if already_owns:
                    print(f"\nYou already have a {item_template['name']} installed. You cannot carry another.")
                    continue
                # Check affordability
                if player_gold >= price:
                    player_gold -= price
                    
                    # Create an item to add to inventory
                    new_item = item_template.copy()
                    player_inventory.append(new_item)
                    
                    print(f"\n*** Purchased {new_item['name']} for {price} credits! ***")
                else:
                    print(f"\nNot enough credits! You need {price} credits.")
            else:
                print("\nInvalid selection.")
        else:
            print("\nInvalid input.")
            
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
        and item.get("currentDurability", 1) > 0
    ]
    
    if not equipable_items:
        print(f"\nYou have no functioning {item_type_to_equip}s to equip.")
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
        unequip_option = len(equipable_items) + 1
        
        print(f"  {unequip_option}) Unequip Current Weapon")
        print("  0) Back to Town Menu")
        print("=" * 30)

        choice = input(f"Enter choice (0-{unequip_option}): ")
        if choice == "0":
            break 

        if choice.isdigit():
            choice_num = int(choice)
            if choice_num == unequip_option:
                if equipped_weapon:
                    print(f"\n{equipped_weapon['name'].capitalize()} has been unequipped.")
                    equipped_weapon = {}
                else:
                    print("\nNothing is currently equipped.")
            elif 1 <= choice_num <= len(equipable_items):
                item_index = choice_num - 1
                item_to_equip = equipable_items[item_index]
                equipped_weapon = item_to_equip 
                print(f"\n** {equipped_weapon['name'].capitalize()} is now equipped! **")
            else: 
                print("\nInvalid selection number.")
        else:
            print("\nInvalid input. Please enter a number.")
    return equipped_weapon, player_inventory
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
    pygame.display.set_caption("Space")
    #Fix the annoying thing where the window for pygame is in the background
    try:
        import sys
        if sys.platform.startswith('win'):
            import ctypes
            hwnd = pygame.display.get_wm_info()['window']
            ctypes.windll.user32.SetForegroundWindow(hwnd)
        else:
            pass
    except Exception as e:
        print(f"Note: Could not force window focus: {e}")    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sprites_dir = os.path.join(current_dir, "sprites")
    #Map background
    bg_variants = []
    try:
        raw_bg = pygame.image.load(os.path.join(sprites_dir, "Background.png"))
        scaled_bg = pygame.transform.scale(raw_bg, (TILE_SIZE, TILE_SIZE))
        for angle in [0, 90, 180, 270]:
            bg_variants.append(pygame.transform.rotate(scaled_bg, angle))
    except (pygame.error, FileNotFoundError):
        print("Warning: 'Background.png' not found. Defaulting to black.")
    #Store background
    if 'bg_grid' not in map_state:
        map_state['bg_grid'] = [
            [random.randint(0, 3) for _ in range(GRID_SIZE)] 
            for _ in range(GRID_SIZE)
        ]
    player_sprite = None
    try:
        raw_player = pygame.image.load(os.path.join(sprites_dir, "Player.png"))
        player_sprite = pygame.transform.scale(raw_player, (TILE_SIZE, TILE_SIZE))
    except (pygame.error, FileNotFoundError) as e:
        print(f"Failed to load 'Player.png'")
    town_sprite = None
    try:
        raw_town = pygame.image.load(os.path.join(sprites_dir, "SpaceStation.png"))
        town_sprite = pygame.transform.scale(raw_town, (TILE_SIZE, TILE_SIZE))
    except (pygame.error, FileNotFoundError) as e:
        print(f"Failed to load 'SpaceStation.png'")
        if 'asteroids' not in map_state:
            map_state['asteroids'] = []
    # Extract locations from state
    player_x, player_y = map_state['player_pos']
    town_x, town_y = map_state['town_pos']
    monsters = map_state['monsters']
    asteroids = map_state['asteroids']
    
    running = True
    action = None # Default action if window is closed by 'X'

    while running:
        asteroid_coords = {a.get_pos() for a in asteroids}
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # User hit the 'x' button, resulting in abrupt exit
                action = ACTION_QUIT
                running = False
            
            if event.type == pygame.KEYDOWN:
                dx, dy = 0, 0
                #prevent softlock
                if event.key == pygame.K_RETURN:
                    if (player_x, player_y) == (town_x, town_y):
                        action = ACTION_RETURN_TO_TOWN
                        running = False
                
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
                #Bounds and asteroid collision
                if (0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE 
                    and (new_x, new_y) not in asteroid_coords):
                    
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

                    
                    #Increment turn counter for each player move
                    map_state['turn_count'] += 1
                    #move asteroids
                    blocked_spots = {m.get_pos() for m in monsters}
                    blocked_spots.add((player_x, player_y))
                    blocked_spots.add((town_x, town_y))
                    for a in asteroids:
                        blocked_spots.add(a.get_pos())
                    for ast in asteroids[:]:
                        blocked_spots.discard(ast.get_pos())
                        ast.move(blocked_spots)
                        if ast.is_out_of_bounds():
                            asteroids.remove(ast)
                        else:
                            blocked_spots.add(ast.get_pos())

                    #Spawn and maintain # of asteroids
                    while len(asteroids) < 3:
                        current_unsafe_spawns = {(player_x, player_y), (town_x, town_y)}
                        for a in asteroids:
                            current_unsafe_spawns.add(a.get_pos())
                        new_ast = asteroid.Asteroid(GRID_SIZE, current_unsafe_spawns)
                        asteroids.append(new_ast)
                        
                    asteroid_coords = {a.get_pos() for a in asteroids}

                    #Monster Movement
                    for monster in monsters:
                        # Pass the global turn count to the move function
                        monster.move((town_x, town_y), map_state['turn_count'], obstacles=asteroid_coords)
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
                            # Drawing
        screen.fill((0, 0, 0)) #Black background
        #Tiled Background
        if bg_variants:
            bg_grid = map_state['bg_grid']
            for x in range(GRID_SIZE):
                for y in range(GRID_SIZE):
                    variant_index = bg_grid[x][y]
                    screen.blit(bg_variants[variant_index], (x * TILE_SIZE, y * TILE_SIZE))
        #Draw Town 
        if town_sprite:
            screen.blit(town_sprite, (town_x * TILE_SIZE, town_y * TILE_SIZE))
        else:
            town_center = (town_x * TILE_SIZE + TILE_SIZE // 2, town_y * TILE_SIZE + TILE_SIZE // 2)
            pygame.draw.circle(screen, (0, 150, 0), town_center, TILE_SIZE // 3)
        #Draw asteroid
        for ast in asteroids:
            ax, ay = ast.get_pos()
            if ast.sprite:
                screen.blit(ast.sprite, (ax * TILE_SIZE, ay * TILE_SIZE))
            else:
                # Draw grey circle if no sprite
                a_center = (ax * TILE_SIZE + TILE_SIZE // 2, ay * TILE_SIZE + TILE_SIZE // 2)
                pygame.draw.circle(screen, (100, 100, 100), a_center, TILE_SIZE // 3)
        #Draw Monsters 
        for monster in monsters:
            monster_x, monster_y = monster.get_pos()
            if (monster_x, monster_y) != (town_x, town_y):
                 if hasattr(monster, 'sprite') and monster.sprite:
                     screen.blit(monster.sprite, (monster_x * TILE_SIZE, monster_y * TILE_SIZE))
                 else:
                     monster_center = (monster_x * TILE_SIZE + TILE_SIZE // 2, monster_y * TILE_SIZE + TILE_SIZE // 2)
                     pygame.draw.circle(screen, monster.color, monster_center, TILE_SIZE // 3)
        
        #Draw Player 
        if player_sprite:
            screen.blit(player_sprite, (player_x * TILE_SIZE, player_y * TILE_SIZE))
        else:
            player_rect = pygame.Rect(player_x * TILE_SIZE, player_y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, (255, 255, 255), player_rect, 2) #Draw white border
        
        pygame.display.flip() #Update the full screen

    pygame.quit() #Close Pygame window
    
    #Update map state with new position before returning
    map_state['player_pos'] = (player_x, player_y)
    
    return action, map_state