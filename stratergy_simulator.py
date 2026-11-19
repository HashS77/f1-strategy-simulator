def get_compound_stats(compound_name):
    while True:
        compound_name=compound_name.capitalize()
        if compound_name == "Soft":
            pace_offset = -1.20
            wear_rate = 9.5
            deg_multiplier = 0.02
            return pace_offset, wear_rate, deg_multiplier
        elif compound_name == "Medium":
            pace_offset = 0
            wear_rate = 6
            deg_multiplier = 0.015
            return pace_offset, wear_rate, deg_multiplier
        elif compound_name == "Hard":
            pace_offset = 0.8
            wear_rate = 3.5
            deg_multiplier = 0.01
            return pace_offset, wear_rate, deg_multiplier
        else:
            print("Invalid compound name.")
            compound_name = input("Enter Tire Compound Soft/Medium/Hard: ")

def calculate_lap_time(base_pace, compound, tire_wear, fuel_kg):
    pace_offset, _, deg_multiplier = get_compound_stats(compound)
    lap_time = base_pace+pace_offset + (fuel_kg*0.03) + tire_wear*deg_multiplier
    if tire_wear>=95:
        lap_time+=25.00
        status = "[!] Tire puncture (+25.00s)"
    elif tire_wear>75:
        lap_time+=2.50
        status = "[!] TIRE CLIFF (+2.50s)"
    else:
        status = "Optimal"
    return round(lap_time,2), status

def check_pit_decision(current_lap,tire_wear, pit_threshold, total_laps):
    if current_lap == total_laps:
        return False
    elif tire_wear >=95 or tire_wear>pit_threshold:
        return True
    return False

def execute_pit_stop():
    while True:
        compound = input("Choose next tire compound: ")
        compound = compound.capitalize()
        if compound == "Soft" or compound == "Medium" or compound == "Hard":
            break
        else:
            print("Invalid compound name.")
            
    tire_wear = 0
    pit_stop_time = 22.50
    return compound, tire_wear, pit_stop_time

def print_stint_summary(laps_in_stint, stint_time, stint_number):
    print( "-----------------------------------------------------------------------------------------------" )
    print(f"|                             Stint {stint_number} Summary                                     |")
    print(f"| Laps Completed: {laps_in_stint} | Stint Time: {stint_time:.2f} | Avg: {(stint_time/laps_in_stint):.2f} |")
    print( "-----------------------------------------------------------------------------------------------" )
    
total_laps = 22
base_pace = 85.00
fuel_kg = 33.0
tire_wear = 0.0
total_time = 0.0
current_lap = 1
stint_number = 1
pit_stops = 0
print('''
      --- PRE-RACE SETUP ---
Available Compounds: [Soft] [Medium] [Hard]
      ''')
while True: 
    compound = input("Select starting tire compound:")
    compound= compound.capitalize()
    if compound == "Soft" or compound == "Medium" or compound == "Hard":
        break
    else:
        print("[ERROR] Invalid compound. Please enter Soft, Medium, or Hard.")
        

while True:
    pit_threshold = float(input("Enter pit-stop tire wear threshold (10 - 95%): "))
    if 95>=pit_threshold>=10:
        break
    else:
        print("[ERROR] Invalid threshold. Please choose thershold in between 10 and 95%")
        
print(">>> LIGHTS OUT AND AWAY WE GO! <<<")

while current_lap<= total_laps:
    laps_in_stint = 0
    stint_time = 0
    print( "=====================================================================================" )
    print(f"STINT {stint_number} | COMPOUND: {compound.upper()} | STARTING FUEL: {fuel_kg:.1f} kg")
    print( "=====================================================================================" )
    
    _,wear_rate,_ = get_compound_stats(compound)
    while current_lap<=total_laps:
        tire_wear+=wear_rate
        fuel_kg-=1.5
        lap_time, status = calculate_lap_time(base_pace, compound, tire_wear, fuel_kg)
        print(f"Lap {current_lap} | Time: {lap_time:.2f} | Wear: {tire_wear:04.1f} | Fuel: {fuel_kg:04.1f} | Status: {status}")
        total_time += lap_time
        stint_time += lap_time
        laps_in_stint += 1
        if check_pit_decision(current_lap,tire_wear,pit_threshold,total_laps):
            print_stint_summary(laps_in_stint,stint_time,stint_number)
            print(f"\n>>> BOX BOX! Tire wear ({tire_wear:.1f}%) reached threshold ({pit_threshold}%). (+22.50s pit loss)")
            compound, tire_wear, pit_loss = execute_pit_stop()
            total_time +=pit_loss
            pit_stops +=1
            current_lap +=1
            stint_number+=1
            break
        else:
            current_lap+=1
            if current_lap>total_laps:
                print_stint_summary(laps_in_stint,stint_time,stint_number)
                break

print(f'''
============================================================
                    CHEQUERED FLAG!
============================================================
Total Laps Completed : {total_laps}
Total Pit Stops Made : {pit_stops} ({pit_stops*22.50} total pit loss)
Average Race Pace    : {(total_time/total_laps):.2f}s / lap
FINAL RACE TIME      : {total_time} ({int(total_time//60)}m {total_time%60}s)
============================================================
      ''')