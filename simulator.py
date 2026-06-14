import numpy as np
import pandas as pd
import time

NUM_CELLS = 8
CELL_CAPACITY_AH = 10.0
NOMINAL_VOLTAGE = 3.7
MAX_VOLTAGE = 4.2
MIN_VOLTAGE = 3.0
PACK_NOMINAL_VOLTAGE = NUM_CELLS * NOMINAL_VOLTAGE

WEAK_CELL = 6

def get_ocv_from_soc(soc):
  soc_points = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
  ocv_points = [3.0, 3.3, 3.5, 3.6, 3.65, 3.7, 3.75, 3.8, 3.9, 4.0, 4.2]
  return np.interp(soc, soc_points, ocv_points)

def simulate_pack(soc, current, dt= 1.0):
  soc_new = soc - (current*dt) / (CELL_CAPACITY_AH * 3600)  #Update soc using coulomb counting
  soc_new = np.clip(soc_new, 0.0, 1.0)

  base_voltage = get_ocv_from_soc(soc_new)  #get base cell voltage from ocv curve

  #simulate individual cell voltage with small noise

  cell_voltage = []
  for i in range(NUM_CELLS):
    noise = np.random.normal(0, 0.005)
    if i== WEAK_CELL:
      voltage = base_voltage - 0.15 + noise
    else:
      voltage = base_voltage + noise
    cell_voltage.append(round(voltage, 3))

  #temparature rises with current draw

  temperature = 25 + (current * 0.8) + np.random.normal(0, 0.3)
  return soc_new, cell_voltage, round(temperature, 2)


def run_simulation(duration_seconds = 300, current = 5.0):
  soc = 1.0
  records = []
  for t in range(duration_seconds):
    soc, cell_voltage, temperature = simulate_pack(soc, current)

    record = {
      'time' : t,
      'soc' : round(soc * 100, 2),
      'current' : current,
      'temperature' : temperature,
      'pack_voltage' : round(sum(cell_voltage), 3)
    }
    #add individual cell voltages

    for i, v in enumerate(cell_voltage):
      record[f'cell_{i+1}_voltage'] = v
    
    records.append(record)
  df = pd.DataFrame(records)
  df.to_csv('bms_data.csv', index = False)
  print("Simulation complete and bms data saved.")
  return df
if __name__ == "__main__":
  run_simulation()