import streamlit as st
import pandas as pd
import plotly.express as px
from simulator import run_simulation
from bms_logic import analyze_pack

st.set_page_config(
  page_title = "BMS Live Monitor",
  page_icon = "🔋",
  layout = "wide"
)

st.title("Battery Management System Monitor")
st.markdown("Real-time simulatiom of 8-cell 48V Li-ion battery pack")

#sidebar controls
st.sidebar.header("Simluation Controls")

duration = st.sidebar.slider(
  "Duration (seconds)",
  min_value = 60,
  max_value = 600,
  value = 300,
  step = 60
)

current = st.sidebar.slider(
  "Current Draw (Amps)",
  min_value = 1.0,
  max_value = 20.0,
  value = 5.0,
  step = 1.0
)

if st.sidebar.button("Run Simulation"):
  with st.spinner("Simulating Battery pack...."):
    run_simulation(duration_seconds = duration, current = current)
    df = analyze_pack()
    st.session_state['df'] = df
df = st.session_state.get('df', None)

if df is not None:
  col1, col2, col3, col4 = st.columns(4)

  with col1:
    st.metric("State of Charge", f"{df['soc'].iloc[-1]}%")

  with col2:
    st.metric("Pack voltage", f"{df['pack_voltage'].iloc[-1]}V")
  
  with col3:
    st.metric("Temperature", f"{df['temperature'].iloc[-1]}C")
  
  with col4:
    st.metric("State of Health", f"{df['soh'].iloc[-1]}%")

  st.divider()

  st.subheader("State of Charge over Time")
  fig1 = px.line(df, x = 'time', y = 'soc',
                 labels = {'time' : 'Time (s)', 'soc' : 'SOC (%)'},
                 color_discrete_sequence = ['#00CC96'])
  st.plotly_chart(fig1, use_container_width = True)


  #cell voltage chart
  st.subheader("Individual Cell Voltages")
  cell_cols = [f'cell_{i+1}_voltage' for i in range (8)]
  latest_cells = df[cell_cols].iloc[-1]
  cell_df = pd.DataFrame({
    'Cell' : [f'Cell {i+1}' for i in range (8)],
    'Voltage' : latest_cells.values
  })

  fig2 = px.bar(cell_df, x = 'Cell', y = 'Voltage', color = 'Voltage',
                color_continuous_scale = 'RdYlGn', range_y = [3.0, 4.3],
                labels = {'Voltage': 'Voltage (v)'})
  st.plotly_chart(fig2, use_container_width = True)

  st.subheader("Temperature over Time")
  fig3 = px.line(df, x = 'time', y = 'temperature',
                labels = {'time' : 'Time (s)', 'temperature' : 'Temperature (C)'},
                color_discrete_sequence = ['#EF553B'])
  fig3.add_hline(y = 45, line_dash = "dash",
                line_color = "red", annotation_text = "Max Safe Temp")
  st.plotly_chart(fig3, use_container_width = True)

  st.subheader("Fault Alerts")
  latest_faults = df['fault'].iloc[-1]
  for fault in latest_faults:
    if fault == 'OK':
      st.success("All systems normal")
    else:
      st.warning(f"{fault}")

else:
  st.info("configure setttings and click Run Simulation to start")