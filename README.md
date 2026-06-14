# Battery Management System (BMS) Simulator

A Python-based BMS simulation and live monitoring dashboard for an 8-cell 48V Li-ion battery pack.

## Features
- Realistic battery discharge simulation using Coulomb Counting and OCV methods
- Individual cell voltage monitoring with weak cell detection
- SOC, SOH, Temperature tracking
- Fault detection — overvoltage, undervoltage, overtemperature, cell imbalance
- Live Streamlit dashboard with interactive controls

## Tech Stack
Python, Pandas, NumPy, Plotly, Streamlit

## How to Run
streamlit run app.py