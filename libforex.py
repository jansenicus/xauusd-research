class ForexPair:
    
    def __init__(self, name):
        
        self.name = name
        self.dataframe = None
    
    def read_csv(self, filepath):
        """ interface to pandas read_csv
            return dataframe for the class
        """
        import pandas as pd
        dataframe = pd.read_csv(filepath, 
                                header=0, 
                                names=['Date', 'Time', 'Open','High','Low','Close','Volume'], 
                                parse_dates=[['Date', 'Time']])
                                             
        self.dataframe = dataframe.set_index('Date_Time', drop=False)
           
    def get_market_extreme(self, period="M", mode="all"):
        """
        base_price = "Open","High","Low","Close"
        base price to determine the lowest price
        
        period='M' 
        period monthly
        
        mode = "min", "max"
        """
        import pandas as pd
        if mode == 'min':
            market_extreme = self.dataframe.groupby([pd.Grouper(freq='M')])[['Date_Time', 'Low']].min()
            print("Market Dates with Lowest Price ("+mode+")")
            market_extreme = market_extreme.set_index(['Date_Time'], drop=False).sort_index()
            
        elif mode == 'max': 
            market_extreme = self.dataframe.groupby([pd.Grouper(freq='M')])[['Date_Time', 'High']].max()                
            print("Market Dates with Highest Price ("+mode+")")
            market_extreme = market_extreme.set_index(['Date_Time'], drop=False).sort_index()
            
        else:
            extreme_hi = self.dataframe.groupby([pd.Grouper(freq='M')])[['Date_Time', 'High']].max()
            extreme_lo = self.dataframe.groupby([pd.Grouper(freq='M')])[['Date_Time', 'Low']].min()
            market_extreme = pd.concat([extreme_hi, extreme_lo])
            market_extreme = market_extreme.loc[market_extreme.index.notnull()]
            
            # in order to classify the price type whether it is High or Low 
            # we are comparing the value on itself
            # if it returns True then the type is itself
            
            market_extreme.loc[market_extreme['High']==market_extreme['High'],'Type'] = 'High'
            market_extreme.loc[market_extreme['Low']==market_extreme['Low'],'Type'] = 'Low'
            
            # in order to have one column for the price
            # we have to fill NaN with zero and then add the two columns altogether
            
            market_extreme = market_extreme.fillna(value=0)
            market_extreme['Price'] = market_extreme['High'] + market_extreme['Low']
            market_extreme = market_extreme.drop(["High", "Low"], axis=1)
        
        return market_extreme.sort_index()
    
    def get_market_closing_extreme(self, period="M", mode="all"):
        """
        base_price = "Open","High","Low","Close"
        base price to determine the lowest price
        
        period='M' 
        period monthly
        
        mode = "min", "max"
        """
        import pandas as pd
        if mode == 'min':
            market_extreme = self.dataframe.groupby([pd.Grouper(freq='M')])[['Date_Time', 'Close']].min()
            print("Market Dates with Lowest Price ("+mode+")")
            market_extreme = market_extreme.set_index(['Date_Time'], drop=False).sort_index()
            
        elif mode == 'max': 
            market_extreme = self.dataframe.groupby([pd.Grouper(freq='M')])[['Date_Time', 'Close']].max()                
            print("Market Dates with Highest Price ("+mode+")")
            market_extreme = market_extreme.set_index(['Date_Time'], drop=False).sort_index()
            
        else:
            extreme_hi = self.dataframe.groupby([pd.Grouper(freq='M')])[['Date_Time', 'Close']].max()
            extreme_lo = self.dataframe.groupby([pd.Grouper(freq='M')])[['Date_Time', 'Close']].min()
            market_extreme = pd.concat([extreme_hi, extreme_lo])
            market_extreme = market_extreme.loc[market_extreme.index.notnull()]
        
        return market_extreme.sort_index()