import talib  as ta


class indicators:
    '''
    args: 
    data :  DATA WITH A VALUES  BY TO CALCULE 

    '''
    def __init__(self, data):
        
        
        '''
        
        
        data(data_series) : los datos ha ser calculados de cierre 
        '''
        self.close = data
        self.open = data
        self.high = data



    def ema(self):
        return ta.EMA(self.close, timeperiod=15).iloc[-1]


    def rsi(self):
        '''
        calcula el rsi
        required : maximo de 14 datos de cierre 
        '''
        
        return ta.RSI(self.close, timeperiod=14)

    def SMA(self):
        return ta.SMA(self.close, timeperiod= 20)

    def macd(self):
        return ta.MACD(self.close, fastperiod=12, slowperiod=26, signalperiod=9)