import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf

#Class to Manage STOCK price Data
class StockPriceManagement(object):
    def __init__(self):
        pass
    
    # Method to get the data for given company and given interval using yfinance library
    def get_data( self, company="MS",start_date = '2020-03-01', end_date='2020-07-31', interval='1wk' ):
        """
        :param company:
        :param start_date:
        :param end_date:
        :param interval:
        :return:
        """
        msft = yf.Ticker( company )
        res = msft.history( start=start_date,
                            end=end_date,
                            interval=interval)
        return res
    
    # Method to process the data and give the requested data
    def prepare_process_data( self, response_data, data_key='Close'):
        """
        :param response_data:
        :param data_key:
        :return:
        """
        dates = [str( x.date() ) for x in response_data[data_key].keys()]
        closed_data = response_data[data_key].tolist()
        process_data = zip( dates, closed_data )
        response_data = [item for item in process_data]
        return response_data

    # Method to get the data higher than the given percentage value
    def get_data_higer_than_given_percentage( self, process_data, percentage_value=5 ):
        """
        :param process_data:
        :param percentage_value:
        :return:
        """
        graph_dates = [process_data[0][0]]
        precentage_values = [0]
        process_values = [process_data[0][1]]
        for i in range( 1, len( process_data ) ):
            precentage_val = (process_data[i][1] - process_data[i - 1][1]) * 100 / process_data[i - 1][1]
            if abs( precentage_val ) >= percentage_value:
                precentage_values.append( precentage_val )
                graph_dates.append( process_data[i][0])
                process_values.append(process_data[i][1])
        
        return graph_dates, precentage_values, process_values

    # Method to Plot the Graph using Matlab and Pandas
    def plot_graph( self, graph_dates, percentage_values, process_values):
        """
        :param graph_dates:
        :param percentage_values:
        :param process_values:
        :return:
        """
        df = pd.DataFrame( {
            'dates': graph_dates,
            'spike': percentage_values
        } )
        
        df.plot( kind='bar', x='dates', y='spike' )
        plt.xlabel( 'Dates' )
        for i, v in enumerate( percentage_values ):
            gap = .25 if v >= 0 else -1.5
            plt.text( i - .5, v + gap, "C: " + str(round(process_values[i],1 )), fontsize=8 )
        plt.ylabel( 'Percentage Spike greater than >=+5 % or <= -5%' )
        plt.show()



sp = StockPriceManagement() #Get the Class Object
res_data = sp.get_data() #Get the Stock Price Data using yfinance default for Conpany: MS start_date = '2020-03-01', end_date='2020-07-31', interval='1wk' you can pass your value
process_data = sp.prepare_process_data(res_data) #Prepare the data for the Closing Values
dates, percentage_values, process_values = sp.get_data_higer_than_given_percentage(process_data) #Get Values Higher that the given percentage value
sp.plot_graph(dates, percentage_values, process_values) #Plot the Graph using Matlab
