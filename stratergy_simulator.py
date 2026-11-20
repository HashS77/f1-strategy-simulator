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

def get_engine_mode_stats(mode_name):
    while True:
        mode_name = mode_name.capitalize()
        if mode_name == "Push":
            lap_time_offset = -0.45
            fuel_burn = 1.80
            tire_wear_multiplier = 1.20
            return lap_time_offset, fuel_burn, tire_wear_multiplier
        elif mode_name == "Balanced":
            lap_time_offset = 0.00
            fuel_burn = 1.50
            tire_wear_multiplier = 1.00
            return lap_time_offset, fuel_burn, tire_wear_multiplier
        elif mode_name == "Conserve":
            lap_time_offset = 0.35
            fuel_burn = 1.20
            tire_wear_multiplier = 0.85
            return lap_time_offset, fuel_burn, tire_wear_multiplier
        else:
            print("Invalid Engine mode name.")
            mode_name = input("Enter Mode name Push/Balanced/Conserve: ")

def calculate_lap_time(base_pace, compound, tire_wear, fuel_kg, mode):
    lap_time_offset, _, _ = get_engine_mode_stats(mode)
    pace_offset, _, deg_multiplier = get_compound_stats(compound)
    lap_time = base_pace+pace_offset + lap_time_offset + (fuel_kg*0.03) + tire_wear*deg_multiplier
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
    
    while True:
        mode = input("Choose the engine mode for this stint: ")
        mode = mode.capitalize()
        if mode == "Push" or mode == "Balanced" or mode == "Conserve":
            break
        else:
            print("Invalid mode name.")
            
    tire_wear = 0
    pit_stop_time = 22.50
    return compound, tire_wear, pit_stop_time, mode

def print_stint_summary(laps_in_stint, stint_time, stint_number):
    print( "-----------------------------------------------------------------------------------------------" )
    print(f"|                             Stint {stint_number} Summary                                     |")
    print(f"| Laps Completed: {laps_in_stint} | Stint Time: {stint_time:.2f} | Avg: {(stint_time/laps_in_stint):.2f} |")
    print( "-----------------------------------------------------------------------------------------------" )
    
total_laps = 22
base_pace = 85.00
tire_wear = 0.0
total_time = 0.0
current_lap = 1
stint_number = 1
pit_stops = 0
dnf = False

print('''
    --- PRE-RACE SETUP ---
Available Compounds: [Soft] [Medium] [Hard]
Available Engine modes: [Push] [Balanced] [Conserve]
    ''')

while True:
    fuel_kg = float(input("Enter the fuel load for the car in Kg: "))
    if fuel_kg > 0:
        break
    else:
        print("Please enter a positive number.")

while True: 
    compound = input("Select starting tire compound: ")
    compound= compound.capitalize()
    if compound == "Soft" or compound == "Medium" or compound == "Hard":
        break
    else:
        print("[ERROR] Invalid compound. Please enter Soft, Medium, or Hard.")
            
while True:
    engine_mode = input("Select starting engine mode: ")
    engine_mode = engine_mode.capitalize()
    if engine_mode == "Push" or engine_mode == "Balanced" or engine_mode == "Conserve":
        break
    else:
        print("Invalid mode name.")


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
    _,fuel_burn,tire_wear_multiplier = get_engine_mode_stats(engine_mode)
    while current_lap<=total_laps:
        tire_wear+=wear_rate*tire_wear_multiplier
        fuel_kg-=fuel_burn
        lap_time, status = calculate_lap_time(base_pace, compound, tire_wear, fuel_kg, engine_mode)
        print(f"Lap {current_lap} | Time: {lap_time:.2f} | Wear: {tire_wear:04.1f} | Fuel: {fuel_kg:04.1f} | Status: {status}")
        total_time += lap_time
        stint_time += lap_time
        laps_in_stint += 1
        if fuel_kg <=0:
            print("Car out of fuel. Stopping on track")
            print(f"Lap {current_lap} car ran out of fuel, causing DNF")
            dnf = True
        if dnf:
            print_stint_summary(laps_in_stint, stint_time,stint_number)
            print("Car did not finish the race")
            print("")
            print(f'''
                  ============================================================
                                          DNF Summary
                  ============================================================
                    Total Laps Completed : {current_lap}
                    Total Pit Stops Made : {pit_stops} ({pit_stops*22.50} total pit loss)
                    Average Race Pace    : {(total_time/current_lap):.2f}s / lap
                    FINAL RACE TIME      : {total_time} ({int(total_time//60)}m {total_time%60:.2f}s)
                  ============================================================
                          ''')
            break
        if check_pit_decision(current_lap,tire_wear,pit_threshold,total_laps):
            print_stint_summary(laps_in_stint,stint_time,stint_number)
            print(f"\n>>> BOX BOX! Tire wear ({tire_wear:.1f}%) reached threshold ({pit_threshold}%). (+22.50s pit loss)")
            compound, tire_wear, pit_loss, engine_mode = execute_pit_stop()
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
        
    
    if dnf:
        break
        
if not dnf:       
    print(f'''
    ============================================================
                        CHEQUERED FLAG!
    ============================================================
    Total Laps Completed : {total_laps}
    Total Pit Stops Made : {pit_stops} ({pit_stops*22.50} total pit loss)
    Average Race Pace    : {(total_time/total_laps):.2f}s / lap
    FINAL RACE TIME      : {total_time} ({int(total_time//60)}m {total_time%60:.2f}s)
    ============================================================
        ''')

