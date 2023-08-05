import pandas as pd
def cci(self, N=20):
    """
    Commodity Channel Index/CCI = (Typical Price  - MA) / (0.015 * MD)
    Typical price = (High + Low + Close) / 3
    MA = Moving Average
    Moving Average = (N - PeriodSum) / N
    MD = Mean Devation
    Mean Devation = ∑i=1|Typical - MA| / N
​	
    """
    name = 'cci_' + str(N)

    try:
        return self.data[name][self.index]
    except:
        TP = (self.data['High'] + self.data['Low'] + self.data['Close']) / 3 
        CCI = pd.Series((TP - TP.rolling(N).mean()) / (0.015 * TP.rolling(N).std()), name=name) 
        self.data[name] = CCI 
        
        return self.data[name][self.index]