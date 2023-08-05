def sma(self, N):
    """
    Simple Moving Average = (N - PeriodSum) / N
    N = number of days in a given period
    PeriodSum = sum of stock closing prices in that period
    """
    name = 'sma_' + str(N)
    
    try:
        return self.data[name][self.index]
            
    except Exception as error:
        self.data[name] = self.data.loc[:, 'Close'].rolling(window=N).mean() 
        # setattr(self, name, [sma])