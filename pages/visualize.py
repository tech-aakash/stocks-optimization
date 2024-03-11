import streamlit as st  
import plotly.express as px  
import plotly.graph_objects as go  
import pandas as pd  
from streamlit_extras.switch_page_button import switch_page
  
st.set_page_config(layout="wide", page_title="Stock Data Visualization", page_icon="📈",initial_sidebar_state="collapsed")  
st.title('Stock Data Visualization')  
  
# Try loading the CSV data  
try:  
    data = pd.read_csv('stock_data.csv')  
except Exception as e:  
    st.error(f'Error loading data: {e}')  
    raise e  
  
# Convert 'Date' column to datetime format  
try:  
    data['Date'] = pd.to_datetime(data['Date'])  
except Exception as e:  
    st.error(f'Error converting date: {e}')  
    raise e  
  
# Set 'Date' column as the index  
data.set_index('Date', inplace=True)  
  
# Extract ticker symbols from column names  
tickers = list(set([col.split(' ')[1] for col in data.columns]))  
  
# Create a dropdown list for the user to select a ticker  
ticker = st.selectbox('Select a ticker to visualize', tickers)  
  
st.subheader('Stock Data Visualization')  
  
# Create a multi-line chart for the stock data  
try:  
    fig = px.line(data[f'Close {ticker}'], title="Adjusted Close Price Over Time")  
    st.plotly_chart(fig)  
except Exception as e:  
    st.error(f'Error creating plot: {e}')  
    raise e  
  
# Create a candlestick chart  
try:  
    fig = go.Figure(data=[go.Candlestick(x=data.index,  
                    open=data[f'Open {ticker}'],  
                    high=data[f'High {ticker}'],  
                    low=data[f'Low {ticker}'],  
                    close=data[f'Close {ticker}'])])  
    st.plotly_chart(fig)  
except Exception as e:  
    st.error(f'Error creating plot: {e}')  
    raise e  
  
# Create a histogram for closing prices  
try:  
    fig = px.histogram(data, x=f'Close {ticker}')  
    st.plotly_chart(fig)  
except Exception as e:  
    st.error(f'Error creating plot: {e}')  
    raise e  
if st.button("Optimise Portfolio"):
    switch_page('optimise')