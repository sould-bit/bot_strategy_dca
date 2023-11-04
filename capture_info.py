import pandas as pd 
import os
def capture_info(time,type,symbol,price, cantidad,earnings ):
    
    '''ARGS:
    time (datetime): time 
    type (str): sell o buy
    symbol (str): simbolo del par
    price (float): precio de la accion
    cantidad: cantidad 
    earnings (float): las ganancias  o perdidad de la accion en caso de averla 
    
    '''
    file_name = 'files_saved/transaciones.xlsx'
    
    try:
    # crear el archivo si no existe 
        if not os.path.exists(file_name):
            transactions = pd.DataFrame(columns=['TIME', 'TYPE', 'SYMBOL', 'PRICE','CANTIDAD', 'PROFIT/LOWS'])
            transactions.to_excel(file_name,engine='openpyxl', index=False,header=True)
            return capture_info()
    
        if os.path.exists(file_name):
            
            df = pd.read_excel(file_name)
            df.loc[len(df)] = {'TIME': time,
                              'TYPE': type,
                              'SYMBOL': symbol,
                              'PRICE': price,
                              'CANTIDAD': cantidad,
                              'PROFIT/LOWS': earnings
                              }
            # Guardar el archivo
            df.to_excel(file_name,engine='openpyxl',index=False)
        
    
    except Exception as e:
        print(e)
        
        

# info =  {'time': '11-3-4','type': 'sell','symbol': 'BTCUSDT','price': 1000,'cantidad':3123213,'earnings': 10}
# capture_info(**info)