import random
import json
import os
from race_names import first_parts, second_parts, horse_first, horse_second, male_names, female_names, surnames, gender_trainer, t_specialty

owned_horses = {
    "Racing": [],
    "Retired": []
}

hired_trainers = []
available_trainers = []

money = 20000

calendar = {
    "day": 1,
    "month": 1,
    "year": 1999
}

month_names = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]


breed_costs = {
    "Thoroughbred": 300,
    "Arabian": 150,
    "Akhal-teke": 500
 }

facility_levels = {
    "Speed Facility": 1,
    "Power Facility": 1,
    "Stamina Facility": 1
}

####################################################

def save_game(filename="savegame.json"):
    save_data = {
        "owned_horses": owned_horses,
        "hired_trainers": hired_trainers,
        "available_trainers": available_trainers,
        "money": money,
        "calendar": calendar,
        "facility_levels": facility_levels,
        "horse_market": horse_market
    }
    with open(filename, "w") as f:
        json.dump(save_data, f, indent=4)
    print("Game saved successfully!")

def load_game(filename="savegame.json"):
    global owned_horses, hired_trainers, available_trainers, money, calendar, facility_levels, horse_market
    try:
        with open(filename, "r") as f:
            save_data = json.load(f)

        owned_horses = save_data.get("owned_horses", {"Racing": [], "Retired": []})
        hired_trainers = save_data.get("hired_trainers", [])
        available_trainers = save_data.get("available_trainers", [])
        money = save_data.get("money", 2000)
        calendar = save_data.get("calendar", save_data.get("calender", {"day": 1, "month": 1, "year": 1999}))  # Support both spellings
        facility_levels = save_data.get("facility_levels", {"Speed Facility": 1, "Power Facility": 1, "Stamina Facility": 1})
        horse_market = save_data.get("horse_market", [])
        print("Game loaded successfully!")
    except FileNotFoundError:
        print("No save file found, starting a new game.")

####################################################

def levelup_facility():
    facilities = list(facility_levels.items()) 
    
    for i, (facility, level) in enumerate(facilities, start=1):
        print(f"{i}. {facility} (Level {level})")

    choice = input("> ").strip()
    if not choice.isdigit():
        print("Invalid input.")
        return

    choice = int(choice)
    if 1 <= choice <= len(facilities):
        facility, level = facilities[choice - 1]

        cost = 1000 * level

        global money
        if money >= cost:
            money -= cost
            facility_levels[facility] = level + 1
            print(f"{facility} upgraded to Level {facility_levels[facility]}! (-${cost}, Balance: ${money})")
        else:
            print(f"Not enough money! You need ${cost}, but you only have ${money}.")
    else:
        print("Invalid choice.")



def trainer_generator():
    gender = random.choice(gender_trainer)
    if gender == "Male":
        t_firstname = random.choice(male_names)
    else:
        t_firstname = random.choice(female_names)
    t_surname = random.choice(surnames)
    name = t_firstname + ' ' + t_surname 
    skill_level = random.randint(1, 100)
    initial_cost = skill_level * 200
    salary = initial_cost / 10  
    specialty = random.choice(t_specialty)

    trainer = {
        "name": name,
        "skill": skill_level,
        "cost": initial_cost,
        "salary": salary,
        "specialty": specialty
        
    }
    return trainer

def generate_ran_trainer(num):
    return [trainer_generator() for _ in range(num)]

def trainer_to_string(trainer):
    return f"{trainer['name']} | Skill: ({trainer['skill']}) Hiring Cost: ${trainer['cost']}, Monthly Salary: ${trainer['salary']} (Specialty: {trainer["specialty"]})"
    
def race_rewards(category, difficulty):
    #base rewards
    if category == "G3":
        base = (500, 300, 100)
    elif category == "G2":
        base = (1000, 500, 300)
    elif category == "G1":
        base = (2000, 1000, 500)
    else:
        return (0, 0, 0)

    #scale rewards
    scale = max(1, difficulty / 1000)

    reward1 = int(base[0] * scale)
    reward2 = int(base[1] * scale)
    reward3 = int(base[2] * scale)

    return reward1, reward2, reward3

def horse_gen():
    first_name = random.choice(horse_first)
    second_name = random.choice(horse_second)
    name = first_name + " " + second_name

    horse = {
        "name": name,
        "speed": random.randint(1, 100),
        "power": random.randint(1, 100),
        "stamina": random.randint(1, 100)
    }
    return horse

def generate_ran_horse(num_horses):
    return [horse_gen() for _ in range(num_horses)]

def categorize_difficulty(total_difficulty):
    if total_difficulty <= 1000:
        return "G3"
    elif total_difficulty <= 3000:
        return "G2"
    else:
        return "G1"

def create_race():
    race_types = {
        "sprint": [1200, 1400],   
        "medium": [2000, 2400],   
        "long":   [2800, 3200, 3600]    
    }
    first_name = random.choice(first_parts)
    second_name = random.choice(second_parts)
    name = first_name + " " + second_name
    race_type = random.choice(list(race_types.keys()))
    distance = random.choice(race_types[race_type]) 

    if race_type == "sprint":
        opponents = generate_ran_horse(7)
    else:
        opponents = generate_ran_horse(14)

    total_difficulty = sum(h["speed"] + h["power"] + h["stamina"] for h in opponents)
    category = categorize_difficulty(total_difficulty)

    race = {
        "name": name,
        "type": race_type,
        "distance": distance,
        "difficulty": total_difficulty,
        "category": category
    }
    return race

def generate_race(number):
    races = []
    for _ in range(number):
        races.append(create_race())
    return races

races_today = generate_race(random.randint(2, 6))

horse_condition = "Healthy"

horse_gender = ["Stallion", "Mare"]

def create_horse(name, breed):
    horse = {"name": name, "breed": breed}
    if breed == "Thoroughbred":
        horse["speed"] = random.randint(1, 20)
        horse["power"] = random.randint(1, 20)
        horse["stamina"] = random.randint(1, 20)
        horse["energy"] = 20
        horse["health"] = 20 
        horse["condition"] = horse_condition
        horse["gender"] = random.choice(horse_gender)
    return horse

def create_horseformarket(name, breed):
    horse = {"name": name, "breed": breed}
    if breed == "Thoroughbred":
        horse["speed"] = random.randint(1, 100)
        horse["power"] = random.randint(1, 100)
        horse["stamina"] = random.randint(1, 100)
        horse["energy"] = 20
        horse["health"] = 20 
        horse["condition"] = horse_condition
        horse["gender"] = random.choice(horse_gender)
    return horse

condition = ["Muscle Strain", "Lameness", "Exhausted", "Stressed"] 

def horse_health(horse):
    if horse['health'] <= 0:
       horse["condition"] = random.choice(condition)
    if horse['health'] >= 1: 
        horse['condition'] = "Healthy"

def horse_to_string(horse):
    return f"{horse['name']} ({horse["gender"]}) ({horse['breed']}) | Speed: {horse['speed']}, Power: {horse['power']}, Stamina: {horse['stamina']}, Energy/Health: {horse['energy']}/{horse['health']} | Condition: {horse['condition']}"

def time_advance():
    past = calendar["day"]
    calendar["day"] += 1
    if calendar["day"] > 30:
        calendar["day"] = 1
        calendar["month"] += 1
        trainer_salary_pay()
        monthly_horse_cost()
        if calendar["month"] > 12:
            calendar["month"] = 1
            calendar["year"] += 1
    if calendar["day"] != past:
        global races_today, available_trainers, horse_market
        races_today = generate_race(random.randint(2, 6))
        available_trainers = generate_ran_trainer(random.randint(1, 5))
        horse_market = generate_market_horses(random.randint(2, 5))

def trainer_salary_pay():
    global money, hired_trainers
    if not hired_trainers:
        return
        
    total_salaries = sum(t["salary"] for t in hired_trainers)
    print(f"\n New month! Trainer salaries are due. Total wages: ${total_salaries}")

    if money >= total_salaries:
      money = money - total_salaries
      print(f"You paid all your trainers. Remaining balance is: ${money}")
    else:
        print("You don't have enough money to pay your trainers")
        unpaid_trainers = []
        for trainer in hired_trainers[:]:  # copy list to safely remove
            if money >= trainer["salary"]:
                money -= trainer["salary"]
                print(f"Paid {trainer['name']} (${trainer['salary']})")
            else:
                print(f"{trainer['name']} has quit because you couldn’t pay their salary (${trainer['salary']})")
                unpaid_trainers.append(trainer)
                hired_trainers.remove(trainer)
        
        print(f"Your balance after partial payments: ${money}")

def show_date():
    month_str = month_names[calendar["month"] - 1]
    print(f"Day {calendar['day']} of {month_str}, Year {calendar['year']}")

def trainer_train_bonus(trainers, stat):
    if not trainers:
        return 0

    def get_training_bonus(skill):
        if 1 <= skill <= 20:       # Tier 1
            return 1 + random.randint(1, 2)
        elif 21 <= skill <= 40:    # Tier 2
            return 2 + random.randint(1, 4)
        elif 41 <= skill <= 60:    # Tier 3
            return 3 + random.randint(1, 6)
        elif 61 <= skill <= 80:    # Tier 4
            return 4 + random.randint(1, 8)
        elif 81 <= skill <= 100:   # Tier 5
            return 5 + random.randint(1, 10)
        return 0

    total_bonus = 0
    for trainer in trainers:
        if trainer["specialty"] == stat:
            total_bonus += get_training_bonus(trainer["skill"])

    return total_bonus

def facility_train_bonus(stat):
    if stat == "speed":
        return facility_levels["Speed Facility"] * 1
    elif stat == "power":
        return facility_levels["Power Facility"] * 1
    elif stat == "stamina":
        return facility_levels["Stamina Facility"] * 1
    return 0

def train_horse(horse, trainers):
    if horse["energy"] <= 0:
        health_loss = random.randint(1, 8)
        horse["health"] = max(-20, horse["health"] - health_loss)
        print(f"{horse['name']} is too exhausted to train! Training forced at 0 energy → {health_loss} health lost.")
        horse_health(horse) 

    print("Please choose a stat to train.")
    print("1-Speed")
    print("2-Power")
    print("3-Stamina")
    choice = input("> ")

    if choice == "1":
        stat = "speed"
    elif choice == "2":
        stat = "power"
    elif choice == "3":
        stat = "stamina"
    else:
        print("Invalid Choice.")
        return


    gain = random.randint(1, 5)
    bonus_gain = trainer_train_bonus(trainers, stat)
    facility_gain = facility_train_bonus(stat)

    total_gain = gain + bonus_gain + facility_gain

    energy_loss = random.randint(1, 5)
    horse[stat] += total_gain

    horse["energy"] = max(0, horse["energy"] - energy_loss)
    time_advance()
    print(f"{horse['name']} trained in {stat}! Base gain: {gain} + Facility Gain: {facility_gain} + Trainer Specialty Bonus: {bonus_gain} → Total gain: {total_gain}")
    print(f"{horse['name']} lost {energy_loss} amount of energy!")


def rest_energy_recover(horse):
    if horse['health'] < 0:
        return
    energy_rest = random.randint(1, 5)
    horse['energy'] = min(20, horse['energy'] + energy_rest)
    horse['health'] = min(20, horse['health'] + random.randint(1, 5))

def retire_horse(horse):                                                              
    owned_horses["Racing"].remove(horse)
    owned_horses["Retired"].append(horse)
    print(f"{horse['name']} has been retired from racing.")

def retire_trainer():
    global hired_trainers
    if not hired_trainers:
        print("You have no trainers to retire.")
        return
    
    print("Which trainer do you want to retire?")
    for i, trainer in enumerate(hired_trainers, start=1):
        print(f"{i}. {trainer['name']} | Skill: {trainer['skill']} | Monthly Salary: ${trainer['salary']} | Specialty: {trainer['specialty']}")
    
    choice = input("> ").strip()
    if not choice.isdigit():
        print("Invalid input.")
        return
    
    choice = int(choice)
    if 1 <= choice <= len(hired_trainers):
        trainer_to_retire = hired_trainers.pop(choice - 1)
        print(f"{trainer_to_retire['name']} has been retired.")
    else:
        print("Invalid trainer number.")

def monthly_horse_cost():
    global money

    total_cost = 0
    for category, horses in owned_horses.items():
        for horse in horses:
            cost = breed_costs.get(horse['breed'], 150)
            total_cost += cost 
    if money >= total_cost:
        money -= total_cost
        print(f"You paid ${total_cost} for horse upkeep. New balance: ${money}")
    else:
        print(f"You can't afford the ${total_cost} upkeep! Your balance is ${money}")

def doctor():
    global money

    if not owned_horses["Racing"]:
        print("You have no horses to heal.")
        return

    print("Which horse do you want to get checked?")
    for i, horse in enumerate(owned_horses["Racing"], start=1):
        print(f"{i}. {horse_to_string(horse)}")

    horse_choice = input("> ").strip()
    if not horse_choice.isdigit():
        print("Invalid input.")
        return

    horse_choice = int(horse_choice)
    if 1 <= horse_choice <= len(owned_horses["Racing"]):
        chosen_horse = owned_horses["Racing"][horse_choice - 1]

        if chosen_horse['condition'] == "Healthy":
            print(f"There is nothing wrong with {chosen_horse['name']}.")
            return

        choice = input(f"{chosen_horse['name']} is injured. It will cost $5000 to heal. Do you want to pay? (yes/no) ").strip().lower()
        if choice == "yes":
            if money >= 5000:
                money -= 5000
                chosen_horse['health'] = 20
                chosen_horse['condition'] = "Healthy"
                print(f"{chosen_horse['name']} has been healed! Your remaining balance is ${money}.")
            else:
                print("You don't have enough money.")
        else:
            print(f"{chosen_horse['name']} was not healed.")
    else:
        print("Invalid horse number.")

def race_result(player_horse, race):
    if race["type"] == "sprint":
        opponents = generate_ran_horse(7)
    else:
        opponents = generate_ran_horse(14)

    all_horses = opponents + [player_horse]

    if race["type"] == "sprint":
        weights = {"speed": 0.6, "power": 0.2, "stamina": 0.2}
    elif race["type"] == "medium":
        weights = {"speed": 0.33, "power": 0.34, "stamina": 0.33}
    elif race["type"] == "long":
        weights = {"speed": 0.2, "power": 0.2, "stamina": 0.6}

    results = []
    for h in all_horses:
        score = (h["speed"] * weights["speed"] +
                 h["power"] * weights["power"] +
                 h["stamina"] * weights["stamina"])
        results.append((h, score))

    results.sort(key=lambda x: x[1], reverse=True)

    print("\nRace Results")
    player_place = None
    for place, (h, score) in enumerate(results, start=1):
        marker = " <= YOU" if h is player_horse else ""
        if h is player_horse:
            player_place = place
        print(f"{place}. {h['name']} (Score {score:.1f}){marker}")

    global money
    if player_place:
        reward1, reward2, reward3 = race_rewards(race["category"], race["difficulty"])
        if player_place == 1:
            money += reward1
            print(f"\nYou finished 1st! You won {reward1} bucks.")
        elif player_place == 2:
            money += reward2
            print(f"\nYou finished 2nd! You won {reward2} bucks.")
        elif player_place == 3:
            money += reward3
            print(f"\nYou finished 3rd! You won {reward3} bucks.")
        else:
            print("\nYou didn’t place in the top 3. No reward money was received.")
        time_advance()

    print(f"Your current balance: {money} bucks.")

def ran_horse_test(ran_horse):
    return f"{ran_horse['name']} | Speed: {ran_horse['speed']}, Power: {ran_horse['power']}, Stamina: {ran_horse['stamina']}"

def generate_ran_horse_test(num_horses):
    return [horse_gen() for _ in range(num_horses)]

def main():
    print("1 - New Game")
    print("2 - Load Game")
    print("3 - Exit")
    choice = input("> ")

    if choice == "1": 
        try:
            player_name = input("Please input your character name: ").strip()
            horse_name = input("Name your horse: ").strip()
            stable_name = input("Please enter a name for your stable: ").strip()
        except (UnicodeDecodeError, EOFError):
            print("Input error detected. Using default names.")
            player_name = "Player"
            horse_name = "Horse"
            stable_name = "My Stable"

        return player_name, horse_name, stable_name

    elif choice == "2":  
        if os.path.exists("savegame.json"):
            load_game()
            return None, None, None
        else:
            print("No save file found! Please start a new game.")
            return main()
    elif choice == "3":  
        exit()
    else:
        print("Invalid input.")
        return main()

player_name, horse_name, stable_name = main()

if player_name: 
    player = {"name": player_name}
    player_horse = create_horse(horse_name, "Thoroughbred")
    owned_horses["Racing"] = [player_horse] 

def generate_market_horses(num=3):
     return [create_horseformarket(random.choice(horse_first) + " " + random.choice(horse_second), "Thoroughbred") for _ in range(num)]

def price_horse(horse):
    total_stats = horse['speed'] + horse['power'] + horse['stamina']
    base_price = total_stats * 50
    return base_price

def price_horse_sell(horse):
    total_stats = horse['speed'] + horse['power'] + horse['stamina']
    base_price = total_stats * 30

    return int(base_price)

horse_market = generate_market_horses(random.randint(2, 5))

def horse_market_print():
    print("\n=== Horse Market ===")
    if not horse_market:
        print("No horses are currently available. Check back tomorrow!")
        return
    for i, horse in enumerate(horse_market, start=1):
        price = price_horse(horse)
        print(f"{i}. {horse_to_string(horse)} | Price: ${price}")

def buy_horse():
    global money
    if not horse_market:
        print("No horses are currently available. Check back tomorrow!")
        return
    
    horse_market_print()
    choice = input("Which horse would you like to buy? > ").strip()
    if not choice.isdigit():
        print("Invalid input.")
        return
    choice = int(choice)
    if 1 <= choice <= len(horse_market):
        chosen_horse = horse_market[choice - 1]
        cost = price_horse(chosen_horse)
        if money >= cost:
            money -= cost
            owned_horses["Racing"].append(chosen_horse)
            horse_market.remove(chosen_horse)
            print(f"You bought {chosen_horse['name']} for ${cost}! Remaining balance: ${money}")
        else:
            print("You don't have enough money to buy this horse.")
    else:
        print("Invalid horse number.")

def sell_horse():
    global money
    all_horses = []
    for category, horses in owned_horses.items():
        all_horses.extend(horses)
    if not all_horses:
        print("You do not own any horses to sell.")
        return
    
    print("Which horse do you want to sell?")
    for i, horse in enumerate(all_horses, start=1):
        price = price_horse_sell(horse)
        print(f"{i}. {horse_to_string(horse)} | Price: ${price}")

    choice = input("> ").strip()
    if not choice.isdigit():
        print("Invalid input.")
        return
    
    choice = int(choice)
    if 1 <= choice <= len(all_horses):
        chosen_horse = all_horses[choice - 1]
        price = price_horse_sell(chosen_horse)
        money += price

        for category, horses in owned_horses.items():
            if chosen_horse in horses:
                horses.remove(chosen_horse)
                break
        print(f"You sold {chosen_horse['name']} for ${price}. New balance: ${money}")
    else:
        print("Invalid horse number.")
    
def finances():
    global money, hired_trainers
    total_cost = 0
    for category, horses in owned_horses.items():
        for horse in horses:
            cost = breed_costs.get(horse['breed'], 150)
            total_cost += cost 
    total_salaries = sum(t["salary"] for t in hired_trainers)
    print("\n=== Monthly Cost ===")
    print(f"You pay a total of ${total_salaries} for hired trainers in wages.")
    print(f"You pay a total of ${total_cost} for the upkeep of your horses.")


def show_help():
    print("\n=== Available Commands ===")
    print("h, horses, owned horses - View your horses")
    print("m, money - Check your money")
    print("doc, doctor - Take horse to doctor")
    print("tr, train, training - Train a horse")
    print("rh, retire horse - Retire a horse")
    print("da, date - Show current date")
    print("rt, retire trainer - Retire a trainer")
    print("ra, race, races - View available races")
    print("t, trainer, trainers - View available trainers")
    print("ht, bt, hire trainer, buy trainer - Hire a trainer")
    print("e, employees, workers - View your employees")
    print("er, enter race - Enter a horse in a race")
    print("r, re, rest, sleep, skip - Rest and advance time")
    print("a, auction, buy horse, bh - Buy a new horse")
    print("market, horse market, hm - Show horses available to purchase")
    print("f, finances monthly, - Show your monthly payments")
    print("sh, sell horse, sell - Sell your horses")
    print("fa, facility, - Level up your facilities")
    print("help - Show this help message")
    print("quit, exit - Exit the game")
    print("===========================\n")

def player_input():
    global money
    print(f"\nWelcome to PyHorseManager, {player_name}!")
    print(f"Your stable: {stable_name}" + " " + "Stable")
    print("Type 'help' to see available commands.\n")
    
    while True:
        try:
            action = input("Please choose an action: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting game...")
            break
        
        if action in ["owned horses", "horses", "h"]:
            for category, horses in owned_horses.items():
                print(f"\n{category} Horses:")
                for h in horses:
                    print(" -", horse_to_string(h))
        
        elif action in ["money", "m"]:
            print("You got", money, "USD.")


        elif action in ["doctor", "doc"]:
            doctor()
        

        elif action in ["sh", "sell horse", "sell"]:
            sell_horse()


        elif action in ["train", "training", "tr"]:
            print("Which horse do you want to train?")
            all_horses = []
            for category, horses in owned_horses.items():
                all_horses.extend(horses)
            for i, h in enumerate(all_horses, start=1):
                print(f"{i}. {h['name']}")
            try:
                choice = input("> ").strip()
                if choice.isdigit():
                    choice = int(choice)
                    if 1 <= choice <= len(all_horses):
                       train_horse(all_horses[choice-1], hired_trainers)
                    else:
                        print("Invalid horse number.")
                else:
                    print("Please enter a valid number.")
            except (ValueError, IndexError):
                print("Invalid input. Please enter a number.")
        
        elif action in ["retire", "retire horse", "rh"]:
            print("Which horse do you want to retire?")
            all_horses = []
            for category, horses in owned_horses.items():
                all_horses.extend(horses)
            for i, h in enumerate(all_horses, start=1):
                print(f"{i}. {h['name']}")
            try:
                choice = input("> ").strip()
                if choice.isdigit():
                    choice = int(choice)
                    if 1 <= choice <= len(all_horses):
                        retire_horse(all_horses[choice-1])
                    else:
                        print("Invalid horse number.")
                else:
                    print("Please enter a valid number.")
            except (ValueError, IndexError):
                print("Invalid input. Please enter a number.")
        
        elif action in ["date", "da"]:
            show_date()
        
        elif action in ["retire trainer", "rt"]:
            retire_trainer()
            
        elif action in ["race", "races", "ra"]:
            for i, race in enumerate(races_today, start=1):
             print(f"{race['name']} {i}: {race['type'].capitalize()} — {race['distance']} meters | Difficulty: {race['difficulty']} | Category: {race['category']}")


        elif action in ["trainer", "trainers", "t"]:
                print("\nAvailable Trainers:")
                if not available_trainers:
                 print("No trainers available today. Check back tomorrow!")
                else:
                 for i, trainer in enumerate(available_trainers, start=1):
                    print(f"{i}. {trainer['name']} | Skill: {trainer['skill']} | Cost: ${trainer['cost']} | Monthly Salary: ${trainer['salary']} (Specialty: {trainer["specialty"]})")

        elif action in ["facility", "fa",]:
            levelup_facility()


        elif action in ["f", "finances", "monthly"]:
            finances()


        elif action in ["hire trainer", "buy trainer","bt","ht"]:
            if not available_trainers:
                print("No trainers available today. Check back tomorrow!")
            else:
                print("Which trainer would you like to hire?")
                for i, trainer in enumerate(available_trainers, start=1):
                    print(f"{i}. {trainer['name']} | Skill: {trainer['skill']} | Cost: ${trainer['cost']} | Monthly Salary: ${trainer['salary']} (Specialty: {trainer["specialty"]})")
                try:
                    choice = input("> ").strip()
                    if choice.isdigit():
                        choice = int(choice)
                        if 1 <= choice <= len(available_trainers):
                            chosen_trainer = available_trainers[choice - 1]
                            if money < chosen_trainer["cost"]:
                                print("You don't have enough money to pay the initial cost.")
                            else:
                                money = money - chosen_trainer["cost"]
                                hired_trainers.append(chosen_trainer)
                                available_trainers.remove(chosen_trainer)
                                print(f"You hired {chosen_trainer['name']} for ${chosen_trainer['cost']}!")
                        else:
                            print("Invalid trainer number.")
                    else:
                        print("Please enter a valid number.")
                except (ValueError, IndexError):
                    print("Invalid input. Please enter a number.")

        elif action in ["workers", "employees", "employee", "e"]:
            if not hired_trainers:
                print("You do not have anyone under you.")
            for i, trainer in enumerate(hired_trainers, start=1):
                print(f"{i}. {trainer['name']} | Skill: {trainer['skill']} | Monthly Salary: ${trainer['salary']} (Specialty: {trainer["specialty"]})")

        elif action in ["a", "auction", "buy horse", "bh"]:
            buy_horse()

        elif action in ["market", "horse market", "hm"]:
            horse_market_print()

        
        elif action in ["enter race", "er"]:
            if not owned_horses["Racing"]:
                print("You have no horses available to race.")
                continue

            print("Which horse would you like to enter?")
            for i, horse in enumerate(owned_horses["Racing"], start=1):
                print(f"{i}. {horse_to_string(horse)}")

            try:
                horse_choice = input("> ").strip()
                if not horse_choice.isdigit():
                    print("Invalid input. Please enter a number.")
                    continue

                horse_choice = int(horse_choice)
                if 1 <= horse_choice <= len(owned_horses["Racing"]):
                    chosen_horse = owned_horses["Racing"][horse_choice - 1]
                else:
                    print("Invalid horse number.")
                    continue
            except (ValueError, IndexError):
                print("Invalid input. Please enter a number.")
                continue
             
            if chosen_horse["condition"] == "Healthy":

                print("Which race would you like to enter?")
                for i, race in enumerate(races_today, start=1):
                    print(f"{i}. {race['name']} ({race['type'].capitalize()}, {race['distance']}m) | Difficulty: {race['difficulty']} | Category: {race['category']}")

                try:
                    race_choice = input("> ").strip()
                    if not race_choice.isdigit():
                        print("Invalid input. Please enter a number.")
                        continue

                    race_choice = int(race_choice)
                    if 1 <= race_choice <= len(races_today):
                        chosen_race = races_today[race_choice - 1]
                        print(f"\nYou entered {chosen_horse['name']} in the {chosen_race['name']} ({chosen_race['type']}, {chosen_race['distance']}m)")
                        race_result(chosen_horse, chosen_race)
                    else:
                        print("Invalid race number.")
                except (ValueError, IndexError):
                    print("Invalid input. Please enter a number.")
            else:
                print(f"{chosen_horse['name']} can't race because of the existing condition: {chosen_horse['condition']}")

        elif action in ["rest", "sleep", "skip","r","re"]:
            print("You rest for the day, time advances.")
            # Apply rest to all owned horses, not just the original player_horse
            for category, horses in owned_horses.items():
                for horse in horses:
                    rest_energy_recover(horse)
            time_advance()

        elif action in ["help", "?"]:
            show_help()

        elif action in ["save"]:
            save_game()

        elif action in ["load"]:
            load_game()

        elif action in ["quit", "exit", "q"]:
            print("Thanks for playing PyHorseManager!")
            break
            
        else:
            print("Invalid Input. Type 'help' for available commands.")

player_input()
