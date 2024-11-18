import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Load the dataset
@st.cache_data
def load_data():
    # Replace with the path to your dataset
    data = pd.read_csv("https://raw.githubusercontent.com/JoseProanioM/predict_ventas/refs/heads/main/data/predicci%C3%B3n_ventas.csv", parse_dates=["Periodo"])
    return data

# Load data
ventas_industria_extended = load_data()

# Streamlit App Layout
st.title("Ventas Totales por Industria: Predicciones 2025")

# Dropdown filter for CIIU_industria
ciiu_options = ventas_industria_extended['CIIU_industria'].unique()
selected_ciiu = st.selectbox("Seleccionar Industria:", ciiu_options)

# Dropdown filter for type of prediction
prediction_options = ["ARIMA", "RW", "Combined"]
selected_prediction = st.selectbox("Seleccionar Tipo de Predicción:", prediction_options)

# Filter the data based on the selected industry
filtered_data = ventas_industria_extended[ventas_industria_extended['CIIU_industria'] == selected_ciiu]

# Plot using Plotly
fig = go.Figure()

# Add the original data
fig.add_trace(go.Scatter(
    x=filtered_data['Periodo'], 
    y=filtered_data['ventasTotales'], 
    mode='lines', 
    name='Serie Original', 
    line=dict(color='#002A5C')
))

# Add ARIMA forecast if selected
if selected_prediction == "ARIMA":
    fig.add_trace(go.Scatter(
        x=filtered_data['Periodo'], 
        y=filtered_data['ARIMA_Forecast'], 
        mode='lines', 
        name='Predicción ARIMA', 
        line=dict(color='#017DC3', dash='dash')
    ))
    
    # Add ARIMA confidence intervals (80% and 95%), without displaying them in the legend
    fig.add_trace(go.Scatter(
        x=filtered_data['Periodo'].tolist() + filtered_data['Periodo'][::-1].tolist(),
        y=filtered_data['ARIMA_Upper80'].tolist() + filtered_data['ARIMA_Lower80'][::-1].tolist(),
        fill='toself',
        fillcolor='rgba(255, 165, 0, 0.2)',  # Light orange for 80% interval
        line=dict(color='rgba(255, 165, 0, 0)'),
        showlegend=False
    ))
    
    fig.add_trace(go.Scatter(
        x=filtered_data['Periodo'].tolist() + filtered_data['Periodo'][::-1].tolist(),
        y=filtered_data['ARIMA_Upper95'].tolist() + filtered_data['ARIMA_Lower95'][::-1].tolist(),
        fill='toself',
        fillcolor='rgba(128, 0, 128, 0.1)',  # Light purple for 95% interval
        line=dict(color='rgba(128, 0, 128, 0)'),
        showlegend=False
    ))

# Add RW forecast if selected
if selected_prediction == "RW":
    fig.add_trace(go.Scatter(
        x=filtered_data['Periodo'], 
        y=filtered_data['RW_Forecast'], 
        mode='lines', 
        name='Predicción RW', 
        line=dict(color='#FF5733', dash='dot')
    ))
    
    # Add RW confidence intervals (80% and 95%), without displaying them in the legend
    fig.add_trace(go.Scatter(
        x=filtered_data['Periodo'].tolist() + filtered_data['Periodo'][::-1].tolist(),
        y=filtered_data['RW_Upper80'].tolist() + filtered_data['RW_Lower80'][::-1].tolist(),
        fill='toself',
        fillcolor='rgba(50, 205, 50, 0.2)',  # Light green for 80% interval
        line=dict(color='rgba(50, 205, 50, 0)'),
        showlegend=False
    ))
    
    fig.add_trace(go.Scatter(
        x=filtered_data['Periodo'].tolist() + filtered_data['Periodo'][::-1].tolist(),
        y=filtered_data['RW_Upper95'].tolist() + filtered_data['RW_Lower95'][::-1].tolist(),
        fill='toself',
        fillcolor='rgba(255, 0, 0, 0.1)',  # Light red for 95% interval
        line=dict(color='rgba(255, 0, 0, 0)'),
        showlegend=False
    ))

# Add Combined forecast if selected
if selected_prediction == "Combined":
    fig.add_trace(go.Scatter(
        x=filtered_data['Periodo'], 
        y=filtered_data['Combined_Forecast'], 
        mode='lines', 
        name='Predicción Combinada', 
        line=dict(color='#800080', dash='dashdot')
    ))
    
    # Add Combined confidence intervals (80% and 95%), without displaying them in the legend
    fig.add_trace(go.Scatter(
        x=filtered_data['Periodo'].tolist() + filtered_data['Periodo'][::-1].tolist(),
        y=filtered_data['Combined_Upper80'].tolist() + filtered_data['Combined_Lower80'][::-1].tolist(),
        fill='toself',
        fillcolor='rgba(0, 191, 255, 0.2)',  # Light blue for 80% interval
        line=dict(color='rgba(0, 191, 255, 0)'),
        showlegend=False
    ))
    
    fig.add_trace(go.Scatter(
        x=filtered_data['Periodo'].tolist() + filtered_data['Periodo'][::-1].tolist(),
        y=filtered_data['Combined_Upper95'].tolist() + filtered_data['Combined_Lower95'][::-1].tolist(),
        fill='toself',
        fillcolor='rgba(0, 0, 255, 0.1)',  # Light blue for 95% interval
        line=dict(color='rgba(0, 0, 255, 0)'),
        showlegend=False
    ))

# Update layout
fig.update_layout(
    title=f"{selected_ciiu}",
    xaxis_title="Periodo",
    yaxis_title="Ventas Totales",
    template="plotly_white",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)  # Center the legend at the top
)

# Display plot in Streamlit
st.plotly_chart(fig)
