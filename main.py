import streamlit as st
import yfinance as yf
import pandas as pd
from streamlit_extras.switch_page_button import switch_page

#set streamlit page layout to wide mode  
st.set_page_config(layout="wide", page_title="Stock Data Downloader", page_icon="📈",initial_sidebar_state="collapsed")  
st.title('Stock Data Downloader')  
  
st.subheader('Input Options')  
tickers = st.text_input("Enter stock tickers separated by commas: ").split(',')  
amount_to_invest = st.number_input("Enter amount to invest: ", value=10000.0, step=100.0)  
  
if st.button('Download Data'):  
    #make progress bar  
    progress = st.progress(0)  
    data = yf.download(tickers, start="2000-01-01", end=pd.Timestamp.now() - pd.Timedelta(days=1))[['Open', 'High', 'Low', 'Close']]    
  
    # Reset the column index to a single-level index  
    data.columns = [' '.join(col).strip() for col in data.columns.values]  
  
    # Save amount to invest to a separate CSV  
    pd.DataFrame([amount_to_invest], columns=['Amount to Invest']).to_csv('amount_to_invest.csv', index=False)  
  
    progress.progress(100)  
    data.to_csv('stock_data.csv')  
    st.write('Data downloaded successfully')  
    switch_page('visualize')