#import the required libs first.

import pandas as pd
import numpy as np
import datetime
from datetime import date
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import yfinance as yf
from pandas_datareader import data as pdr
%matplotlib inline

def return_figures():
    """Creates four plotly visualizations

    Args:
        None

    Returns:
        list (dict): list containing the four plotly visualizations

    """
    
    #setup the holding period as 1, 2, 3 years

    def get_stock_history (tiker, invest_period):
    
        """
        input: 
              tiker - stock name
              invest_period 
    
        output: 
               stock_history_adjclose
    
        """
    
        today = date.today()
        time_of_buying_tree_years = today.replace(today.year - invest_period)
        time_of_buying_two_years = today.replace(today.year - invest_period)
        time_of_buying_one_years = today.replace(today.year - invest_period)

        #down load the stock historical data for recent 3 years
        yf.pdr_override()
        stock_history = pdr.get_data_yahoo(tiker, time_of_buying_tree_years, today)
    
        # Create a dataframe with only the Adj Close column
        stock_history_adjclose = stock_history[['Adj Close']]
        
        return stock_history_adjclose

    sp500_adjclose_three_years = get_stock_history('^GSPC', 3) #sp500 adjusted closing price in recent 3 years
    sp500_adjclose_three_years = sp500_adjclose_three_years.rename(columns={'Adj Close':'SP500'})
    
    #choosing 5 stocks into the portfolio
    portfolio_stocks = ["AAPL", "JNJ", "MCD", "MTCH", "NFLX"]

    #down load the historical data for the tocks in the portfolio for recent 3 years
    portfolio_adjclose_three_years = get_stock_history(portfolio_stocks, 3)
    portfolio_adjclose_three_years = portfolio_adjclose_three_years['Adj Close']
    
    #merge the two data frames
    merged_portfolio_sp500_three_years = pd.merge(portfolio_adjclose_three_years, sp500_adjclose_three_years, 
                                                  left_index=True, right_index=True)
    
    #plot the portfolio & SP500 history in recent 3 years

    graph_one = []
    for stock in merged_portfolio_sp500_three_years.columns.tolist():
          x_val = merged_portfolio_sp500_three_years.index.tolist()
          y_val = merged_portfolio_sp500_three_years[stock].tolist()
          graph_one.append(
              go.Scatter(
              x = x_val,
              y = y_val,
              mode = 'lines',
              name = stock
              )
          )
    
    layout_one = dict(title = 'Portfolio and SP500 History in Recent 3 Years',
                      xaxis = dict(title = 'Time',
                  ),
                yaxis = dict(title = 'Price'),
                )

    #assume the selling date is today and start of the holding date was the three years ago 
    #swap the rows and columns
    merged_portfolio_sp500_three_years_start_end = merged_portfolio_sp500_three_years.iloc[[0,-1]]
    merged_portfolio_sp500_three_years_start_end = merged_portfolio_sp500_three_years_start_end.T
    merged_portfolio_sp500_three_years_start_end.rename(columns=lambda t: t.strftime('%Y'), inplace=True)
    merged_portfolio_sp500_three_years_start_end.rename(columns={'2017':'Start', '2020':'End'}, 
                                                        index = {'Date':'Portfolio'}, inplace=True)
    merged_portfolio_sp500_three_years_start_end
    
    #calculate the three years investment return on the current date
    merged_portfolio_sp500_three_years_start_end['Return'] = merged_portfolio_sp500_three_years_start_end['End'] / merged_portfolio_sp500_three_years_start_end['Start'] - 1
    merged_portfolio_sp500_three_years_start_end
    
    #average return of the selected portfolio
    portfolio_return_three_years = merged_portfolio_sp500_three_years_start_end.iloc[0:4]['Return'].mean()
    
    #average return of sp500
    sp500_returen_three_years = merged_portfolio_sp500_three_years_start_end.iloc[-1]['Return']
    
    #plot the expected ROI of portfolio vs SP500 in recent 3 years
    graph_two = []
    graph_two.append(
          go.Bar(
          x = ['SP500', 'Portfolio'],
          y = [sp500_returen_three_years, portfolio_return_three_years] 
          )
        )

    layout_two = dict(title = 'ROI - SP500 VS Portfolio for 3 Years',
                    xaxis = dict(title = 'SP500 VS Portfolio',),
                    yaxis = dict(title = 'Return'),
                    )
    
    #prepare data for the 2 years period of investment
    sp500_adjclose_two_years = get_stock_history('^GSPC', 2) #sp500 adjusted closing price in recent 2 years
    sp500_adjclose_tow_years = sp500_adjclose_two_years.rename(columns={'Adj Close':'SP500'})
    portfolio_adjclose_two_years = get_stock_history(portfolio_stocks, 2)
    portfolio_adjclose_two_years = portfolio_adjclose_two_years['Adj Close']
    merged_portfolio_sp500_two_years = pd.merge(portfolio_adjclose_two_years, sp500_adjclose_two_years, left_index=True,
                                                right_index=True)

    #assume the selling date is today and start of the holding date was the two years ago 
    #swap the rows and columns
    merged_portfolio_sp500_two_years_start_end = merged_portfolio_sp500_two_years.iloc[[0,-1]]
    merged_portfolio_sp500_two_years_start_end = merged_portfolio_sp500_two_years_start_end.T
    merged_portfolio_sp500_two_years_start_end.rename(columns=lambda t: t.strftime('%Y'), inplace=True)
    merged_portfolio_sp500_two_years_start_end.rename(columns={'2018':'Start', '2020':'End'}, index = {'Date':'Portfolio'},
                                                      inplace=True)

    #calculate the two years investment return on the current date
    merged_portfolio_sp500_two_years_start_end['Return'] = merged_portfolio_sp500_two_years_start_end['End'] /
    merged_portfolio_sp500_two_years_start_end['Start'] - 1

    #average return of the selected portfolio
    portfolio_return_two_years = merged_portfolio_sp500_two_years_start_end.iloc[0:4]['Return'].mean()
    sp500_returen_two_years = merged_portfolio_sp500_two_years_start_end.iloc[-1]['Return']
    
    #plot the expected ROI of portfolio vs SP500 in recent 2 years
    graph_three = []
    graph_three.append(
          go.Bar(
          x = ['SP500', 'Portfolio'],
          y = [sp500_returen_two_years, portfolio_return_two_years] 
          )
        )

    layout_three = dict(title = 'ROI - SP500 VS Portfolio for 2 Years',
                    xaxis = dict(title = 'SP500 VS Portfolio',),
                    yaxis = dict(title = 'Return'),
                    )
    
    #prepare data for the 1 years period of investment
    sp500_adjclose_one_years = get_stock_history('^GSPC', 1) #sp500 adjusted closing price in recent 1 years
    sp500_adjclose_one_years = sp500_adjclose_one_years.rename(columns={'Adj Close':'SP500'})
    portfolio_adjclose_one_years = get_stock_history(portfolio_stocks, 1)
    portfolio_adjclose_one_years = portfolio_adjclose_one_years['Adj Close']
    merged_portfolio_sp500_one_years = pd.merge(portfolio_adjclose_one_years, sp500_adjclose_one_years, left_index=True,
                                                right_index=True)

    #assume the selling date is today and start of the holding date was the two years ago 
    #swap the rows and columns
    merged_portfolio_sp500_one_years_start_end = merged_portfolio_sp500_one_years.iloc[[0,-1]]
    merged_portfolio_sp500_one_years_start_end = merged_portfolio_sp500_one_years_start_end.T
    merged_portfolio_sp500_one_years_start_end.rename(columns=lambda t: t.strftime('%Y'), inplace=True)
    merged_portfolio_sp500_one_years_start_end.rename(columns={'2019':'Start', '2020':'End'}, index = {'Date':'Portfolio'}, inplace=True)

    #calculate the two years investment return on the current date
    merged_portfolio_sp500_one_years_start_end['Return'] = merged_portfolio_sp500_one_years_start_end['End'] /
    merged_portfolio_sp500_one_years_start_end['Start'] - 1

    #average return of the selected portfolio
    portfolio_return_one_years = merged_portfolio_sp500_one_years_start_end.iloc[0:4]['Return'].mean()
    sp500_returen_one_years = merged_portfolio_sp500_one_years_start_end.iloc[-1]['Return']
    
    #plot the expected ROI of portfolio vs SP500 in recent 1 years
    graph_four = []
    graph_four.append(
          go.Bar(
          x = ['SP500', 'Portfolio'],
          y = [sp500_returen_one_years, portfolio_return_one_years] 
          )
        )
    
    layout_four = dict(title = 'ROI - SP500 VS Portfolio for 1 Years',
                    xaxis = dict(title = 'SP500 VS Portfolio',),
                    yaxis = dict(title = 'Return'),
                    )


    # append all charts to the figures list
    figures = []
    figures.append(dict(data=graph_one, layout=layout_one))
    figures.append(dict(data=graph_two, layout=layout_two))
    figures.append(dict(data=graph_three, layout=layout_three))
    figures.append(dict(data=graph_four, layout=layout_four))

    return figures