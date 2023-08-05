from pandas import Series
def roc(self, N=5):
    """
    roc = [(Current Close price - Close price N periods ago) / Close price N periods ago))]
    """
    name = 'roc_' + str(N)
    try:
        return self.data[name][self.index]
    except:
        diff = self.data['Close'].diff(N)
        previous = self.data['Close'].shift(N)
        roc = Series(diff/previous, name='Rate of Change')
        self.data[name] = roc
        roc
        return self.data[name][self.index]
        