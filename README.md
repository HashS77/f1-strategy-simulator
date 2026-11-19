# F1 Strategy Simulator

A command-line Formula 1 race strategy simulator written in Python. The program lets the user select a starting tire compound and pit-stop wear threshold, then simulates lap times, fuel burn, tire wear, pit stops, and the final race time.

## Features

- Soft, Medium, and Hard tire compounds
- Customizable pit-stop tire wear threshold
- Fuel effect on lap time
- Compound-specific tire wear and degradation
- Tire cliff and puncture penalties
- User-selected replacement tire compounds
- Stint summaries and final race statistics

## Requirements

- Python 3
- No third-party packages

## Running the Simulator

From the project folder, run:

```powershell
python stratergy_simulator.py
```

When prompted:

1. Choose `Soft`, `Medium`, or `Hard` as the starting compound.
2. Enter a pit-stop wear threshold from `10` to `95` percent.
3. Choose the next tire compound whenever the car enters the pits.

## Simulation Model

The race uses 22 laps and starts with 33 kg of fuel. Each lap reduces fuel by 1.5 kg.

Lap time is calculated with:

```text
lap time = base pace + compound pace offset
           + (fuel kg x 0.03)
           + (tire wear x degradation multiplier)
```

| Compound | Pace offset (s) | Wear per lap (%) | Degradation multiplier |
|---|---:|---:|---:|
| Soft | -1.20 | 9.5 | 0.020 |
| Medium | 0.00 | 6.0 | 0.015 |
| Hard | 0.80 | 3.5 | 0.010 |

Pace offsets are relative to the Medium compound. Negative values are faster.

## Tire Status

- **Optimal:** Wear is 75% or lower.
- **Tire cliff:** Above 75% wear adds 2.50 seconds to the lap.
- **Tire puncture:** Wear reaches 95% or higher and adds 25.00 seconds to the lap.

When a pit stop occurs, the program resets tire wear to 0% and adds a 22.50-second pit loss.

## Example Session

```text
--- PRE-RACE SETUP ---
Available Compounds: [Soft] [Medium] [Hard]

Select starting tire compound: medium
Enter pit-stop tire wear threshold (10 - 95%): 75
```

The simulator then prints each lap, a summary for every stint, and the final race result.