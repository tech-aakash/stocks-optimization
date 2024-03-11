import streamlit as st  
import pandas as pd  
import numpy as np  
from scipy.optimize import minimize
import plotly.graph_objs as go    

st.set_page_config(layout="wide", page_title="Stock Data Visualization", page_icon="📈",initial_sidebar_state="collapsed")  


def load_data():  
    data = pd.read_csv('stock_data.csv')  
    data['Date'] = pd.to_datetime(data['Date'])  
    data.set_index('Date', inplace=True)  
    tickers = list(set([col.split(' ')[1] for col in data.columns]))  
    return data, tickers  
  
def calculate_portfolio(data, tickers, amount_to_invest):  
    # Calculate daily returns for 'Close' prices only  
    close_prices = data[[f'Close {ticker}' for ticker in tickers]]  
    returns = close_prices.pct_change()  
  
    # Define the objective function (negative Sharpe Ratio)  
    def objective(weights):  
        weights = np.array(weights)  
        ret = np.sum(returns.mean() * weights) * 252  
        vol = np.sqrt(np.dot(weights.T, np.dot(returns.cov() * 252, weights)))  
        sharpe = ret / vol  
        return -1 * sharpe  # We want to maximize Sharpe ratio, hence the negative sign  
  
    # Define the constraints  
    cons = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})  # The weights must sum up to 1  
    bounds = tuple((0, 1) for x in range(len(tickers)))  # The weights can range from 0 to 1  
    initial_guess = [1 / len(tickers) for x in range(len(tickers))]  # We start from an evenly distributed portfolio  
  
    # Perform the optimization  
    optimized_result = minimize(objective, initial_guess, method='SLSQP', bounds=bounds, constraints=cons)  
  
    return optimized_result.x  
 
  
st.title('Portfolio Optimization')  
  
    # Load data  
data, tickers = load_data()  
  
    # Get amount to invest  
amount_to_invest = pd.read_csv('amount_to_invest.csv')['Amount to Invest'].values[0]  
  
# Optimize portfolio  
optimal_weights = calculate_portfolio(data, tickers, amount_to_invest)  
  
# Get daily returns for 'Close' prices only  
close_prices = data[[f'Close {ticker}' for ticker in tickers]]  
returns = close_prices.pct_change()  
  
# Display results  
max_sr_ret = np.sum((returns.mean() * optimal_weights * 252))  
max_sr_vol = np.sqrt(np.dot(optimal_weights.T, np.dot(returns.cov() * 252, optimal_weights)))  
max_sharpe_ratio = max_sr_ret/max_sr_vol  
# Calculate amounts to invest  
invest_amounts = np.round(optimal_weights * amount_to_invest)  
  
# Create pie chart  
fig = go.Figure(data=[go.Pie(labels=tickers, values=invest_amounts)])  
  
# Define layout  
fig.update_layout(title_text='Investment Amount per Stock')  
  
# Display the pie chart  
st.plotly_chart(fig)  

max_sr_ret_percent = round(max_sr_ret * 100, 2)  
max_sr_vol_percent = round(max_sr_vol * 100, 2) 

  
st.write(f"The maximum Sharpe Ratio obtained from the optimization is: {max_sharpe_ratio}")  
st.write(f"This occurs at a portfolio return of: {max_sr_ret_percent}%")  
st.write(f"And a portfolio volatility of: {max_sr_vol_percent}%")  
  
for ticker, weight, amount in zip(tickers, optimal_weights, invest_amounts):  
    st.write(f"Stock: {ticker}, Weight: {weight * 100:.2f}%, Amount: {amount:.2f}")  
  