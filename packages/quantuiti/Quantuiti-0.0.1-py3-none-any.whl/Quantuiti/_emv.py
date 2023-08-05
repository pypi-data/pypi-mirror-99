from pandas import Series
def emv(self, N=14):
    """
    Distance Moved =  ( ((High + Low) / 2) - ((PH + PH) / 2) )
    Box Ratio = (Volume / scale) / (High - Low)
    1-Period EMV = ((High + Low) / 2) - ((PH + PL) / 2 )) / ( (Volume / scale) / (High - Low) )
    14-period Ease of movement = 14-period simple moving average of 1-period EMV
    where:
    PH = Prior High
    PL = Prior Low
    """
    try:
        return self.data[name][self.index]
    except:
        name = 'EVM_MA_' + str(N)
        dm = ((self.data['High'] + self.data['Low'])/2) - ((self.data['High'].shift(1) + self.data['Low'].shift(1))/2)
        br = (self.data['Volume'] / 100000000) / ((self.data['High'] - self.data['Low']))
        EVM = dm / br 
        EVM_MA = Series(EVM.rolling(N).mean(), name = 'EVM') 
        self.data[name] = EVM_MA
        return self.data[name][self.index]