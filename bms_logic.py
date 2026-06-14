import pandas as pd

#safety threshold
MAX_CELL_VOLTAGE = 4.25
MIN_CELL_VOLTAGE = 3.0
MAX_TEMPERATURE = 45.0
IMBALANCE_THRESHOLD = 0.05 #50mV differnce between cells

def calculate_soh(current_capacity, rated_capacity = 10.0):
  #soh = (current capacity / rated capacity) * 100
  soh = (current_capacity / rated_capacity) * 100
  return round(soh, 2)

def detect_fault(row):
  faults = []
  #check each cell voltages
  cell_voltage = [row[f'cell_{i+1}_voltage'] for i in range(8)]

  for i, v in enumerate(cell_voltage):
    if v > MAX_CELL_VOLTAGE:
      faults.append(f'OVERVOLTAGE: Cell {i+1} at {v}V')
    if v < MIN_CELL_VOLTAGE:
      faults.append(f'UNDERVOLTAGE: Cell {i+1} at {v}V')
      
  #check temperature
  if row['temperature'] > MAX_TEMPERATURE:
    faults.append(f'OVERTEMP: {row['temperature']}C exceeds {MAX_TEMPERATURE}C')
  
  #check cell imbalance
  avg_voltage = sum(cell_voltage) / len(cell_voltage)
  for i, v in enumerate(cell_voltage):
    if abs(v - avg_voltage) > IMBALANCE_THRESHOLD:
      faults.append(f"IMBALANCE: Cell {i+1} at {v}V vs avg {round(avg_voltage, 3)}V")
  return faults if faults else ['OK']

def analyze_pack(csv_path = 'bms_data.csv'):
  df = pd.read_csv(csv_path)

  #apply faut detection to every cell
  df['fault'] = df.apply(detect_fault, axis = 1)

  #calculate soh (simulation slight degradation)
  current_capacity = 8.6
  df['soh'] = calculate_soh(current_capacity)

  print(f"Total timesteps: {len(df)}")
  print(f"SOC range: {df['soc'].max()}% to {df['soc'].min()}%")
  print(f"SOH: {df['soh'].iloc[0]}%")
  print(f"Max Temperature: {df['temperature'].max()}C")
  print(f"Faults detected: {df[df['fault'].astype(str).str.contains('IMBALANCE|OVERVOLTAGE|UNDERVOLTAGE|OVERTEMP')].shape[0]} timesteps")

  return df
if __name__ == "__main__":
  df = analyze_pack()
  print(df[['time', 'soc', 'temperature', 'fault']].head(10))
