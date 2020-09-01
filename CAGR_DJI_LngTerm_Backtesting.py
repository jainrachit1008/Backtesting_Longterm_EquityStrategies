# Import necesary libraries
import yfinance as yf
import numpy as np
import datetime as dt
import pandas as pd
from pandas.plotting import table
import matplotlib.pyplot as plt

def CAGR(DF):
    "function to calculate the Cumulative Annual Growth Rate of a trading strategy"
    df = DF.copy()
    df["daily_ret"] = DF["Adj Close"].pct_change()
    df["cum_return"] = (1 + df["daily_ret"]).cumprod()
    n = len(df)/252
    cagr_final = (df["cum_return"][-1])**(1/n) - 1
    return cagr_final, DF.index[0]

######################################## BackTesting #########################################
"""" backtesting the strategy to buy and hold Dow Jones Index for exactly 5 year in a window 
 of past 35 years i.e. on 10,958 possible combinations """

ticker_index = "^DJI"
end_date = dt.date.today()
start_date = end_date - dt.timedelta(12783)
DJ = yf.download(ticker_index,start_date,end_date)
DJ_CAGR = {}
for i in range(len(DJ)-1828):
    start_year, start_month, start_day = DJ.index[i].year, DJ.index[i].month, DJ.index[i].day
    if (start_month == 2 and start_day > 28):
        end_year, end_month, end_day = start_year + 5, start_month, 28
    else:
        end_year, end_month, end_day = start_year + 5, start_month, start_day
    startday = dt.datetime(start_year,start_month,start_day)
    endday = dt.datetime(end_year,end_month,end_day)
    dj = DJ.loc[startday:endday]
    cagr = CAGR(dj)[0]*100
    key = CAGR(dj)[1]
    DJ_CAGR[key] = cagr

DJ_Index_CAGR = pd.DataFrame.from_dict(DJ_CAGR,orient='index',columns=['5-yr CAGR'])

# Plotting
fig, ax = plt.subplots(1, 1)
table(ax, np.round(DJ_Index_CAGR.describe(), 2), loc='upper right', colWidths=[0.2])
DJ_Index_CAGR.plot(ax=ax, ylim=(-10,50), legend=None, kind='line', use_index=True, grid=True, title='Dow Jones CAGR with 5 years holding period')
ax.set(xlabel="Time Series", ylabel = "5-yr Return %")