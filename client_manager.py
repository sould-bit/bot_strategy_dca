from binance.spot import Spot
from config import secret
from config import key
from time import sleep
import time
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
'''
        Debug :   10
        info:     20
        warning:  30
        error:    40
        critical: 50
'''


class client_:
    

    def __init__(self):
            '''
            inicializa y conecta  el Cliente
            '''
            while True:
                try :
                # crea una instancia del Cliente 
                    self.brok =Spot(api_key=key,api_secret=secret)
                    logging.info(f"iniciando coneccion con la Api ")
                    break

                
                except Exception as e:
                    logging.warning(f"no se ha podido establecer la coneccion con binance Appi -> {e}")
                    sleep(5)
                
    def order_buy(self,size:int, max_retries = 3):
            '''
            args :
            size (int) : cantidad en usd comprar
            '''
            
            retries = 0 
            # nesesario para la test  es usar quantity
            # price = float(self.brok.ticker_price('BTCBUSD')['price'])
            
            while retries < max_retries:
                try:
                    params = {'symbol':'BTCUSDT',
                              'side':'BUY',
                              'type':'MARKET',
                              'quoteOrderQty': size
                              }                 
                    self.brok.new_order(**params)
                    print(f'\n ** \ncompra\n ** \n')
                    break # 'exito'  salir del bucle 
                
                except Exception as e:
                    logging.error(f'error al crear la orden de compra: {e}')
                    
                    retries += 1
                    sleep(1)
                    
            if retries == max_retries:
                logging.info(f'el numero maximo de intentos ha sido superdo, debido al error') 
                
                
    def secuity_order_buy(self,size:int, max_retries = 3):
            '''
            args: 
            size (int): tamaño de recompra en usd 
            '''
            
            retries = 0
            # nesesario para la test  es usar quantity
            # price = float(self.brok.get_symbol_ticker()[11][price])
            while retries < max_retries:
                try:
                    params = {'symbol': 'BTCUSDT',
                              'side': 'BUY',
                              'type': 'MARKET',
                              'quoteOrderQty': size 
                              }
                    
                    self.brok.new_order(**params)
                    print(f'\n ** \nRecompra\n ** \n')
                    break # 'exito' salir del bucle 
                    
                except Exception as e:
                    logging.error(f'error al crear la orden de compra: {e}')
                    sleep(1)
                    
                    retries += 1
                    
            if retries == max_retries:
                logging.info(f'el numero maximo de intentos ha sido superdo, debido al error: {e}')     
        
        
    def order_sell(self,max_retries = 3):
            
            retries = 0
            while retries < max_retries:
                try:
                    # AHI  QUE VERIFICAR , SI BALANCE_BTC MUESTRA EL BALANCE EN SI 
                    balance_btc = [x for x in self.brok.account()['balances'] if x['asset'] == 'BTC']
                    btc_to_sell = float(balance_btc[0]['free'])
                    
                    params = {'symbol': 'BTCUSDT',
                              'side': 'SELL',
                              'type': 'MARKET',
                              'quantity': btc_to_sell}
                    
                    self.brok.new_order(**params)
                    print(f'\n ** \nventa\n ** \n')
                    break # exito, salir del bucle 
                
                except Exception as e:
                    logging.error(f'error al crear la orden de venta : {e}')
                    
                    retries += 1
                
                         
            if retries == max_retries:
                logging.info(f'el numero maximo de intentos ha sido superdo, debido al error: {e}') 

    
    def calcular_ganancias(self,precio_de_entrada, precio_actual):
        '''
        args:
        precio_de_entrada (float):  el precio de entrada 
        
        precio actual (float): el precio actual 
        
        return :  ganancias o perdidas actuales 
        '''
        if precio_de_entrada != None:
            balance_btc = [x for x in self.brok.account()['balances'] if x['asset'] == 'BTC']
            btc_to_sell = float(balance_btc[0]['free'])
            
            earning = (precio_actual - precio_de_entrada) * btc_to_sell
            return earning
        else :
            return None 
        
        
        
    def calcule_percentage(self,earning,entry_price):
        '''
        args: 
        earning float():  requiere el calculo de las ganancias
        entry_price float(): requiere el precio de entrada  (compra)
        
        return : float(percentage_profit)
        '''
        if earning != None:
        
            balance_btc = [x for x in self.brok.account()['balances'] if x['asset'] == 'BTC']
            btc_to_sell = float(balance_btc[0]['free'])
            porcentage_ganancia = (earning / (entry_price * btc_to_sell)) * 100 
            
            return porcentage_ganancia
        else: 
            return None



