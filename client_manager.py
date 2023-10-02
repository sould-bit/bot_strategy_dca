from binance.client import Client
from config import secreta
from config import keya 
from time import sleep
import asyncio
import logging
key = keya
secret = secreta
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
    

    async def connect_Client(self):
            '''
            inicializa y conecta  el Cliente
            '''
            while True:
                try :
                # crea una instancia del Cliente 
                    self.brok =Client(api_key=key,api_secret=secret)
                    logging.info(f"iniciando coneccion con la Api ")
                    return self.brok
                
                except Exception as e:
                    logging.warning(f"no se ha podido establecer la coneccion con binance Appi -> {e}")
                    sleep(5)
                    
    async def order_buy(self,size:int, max_retries = 3):
            '''
            args :
            size (int) : cantidad en usd comprar
            '''
            await self.connect_Client()
            retries = 0 
            while retries < max_retries:
                try:
                    params = {'symbol': 'BTCBUSD',
                              'side':'BUY',
                              'type': 'MARKET',
                              # usamos quoterOrderQty , para  tomar valores en usd
                              'quoterOrderQty': size # compramos 10 dolares 
                              }                 
                    self.brok.create_test_order(
                    
                    )
                    print(f'\n ** \ncompra\n ** \n')
                    break # 'exito'  salir del bucle 
                
                except Exception as e:
                    logging.error(f'error al crear la orden de compra: {e}')
                    await asyncio.sleep(2)
                    retries += 1
                    
            if retries == max_retries:
                logging.info(f'el numero maximo de intentos ha sido superdo, debido al error: {e}') 
                
                
    async def secuity_order_buy(self,size:int, max_retries = 3):
            '''
            args: 
            size (int): tamaño de recompra en usd 
            '''
            await self.connect_Client()
            retries = 0
            while retries < max_retries:
                try:
                    params = {'symbol': 'BTCBUSD',
                              'side': 'BUY',
                              'type': 'MARKET',
                              'quoterOrderQty': size # compramos el valor de 15 dolares 
                              }
                    
                    self.brok.create_test_order(**params)
                    print(f'\n ** \nRecompra\n ** \n')
                    break # 'exito' salir del bucle 
                    
                except Exception as e:
                    logging.error(f'error al crear la orden de compra: {e}')
                    await asyncio.sleep(2)
                    retries += 1
                    
            if retries == max_retries:
                logging.info(f'el numero maximo de intentos ha sido superdo, debido al error: {e}')     
        
        
    async def order_sell(self,max_retries = 3):
            await  self.connect_Client()
            retries = 0
            while retries < max_retries:
                try:
                    # nesesito mostra el balance , de los assets   para cuando ocurra la venta se venda todo !
                    valor_usdt = None
                    params = {'symbol': 'BTCBUSD',
                              'side': 'SELL',
                              'type': 'MARKET',
                              'quantity': valor_usdt}
                    
                    self.brok.create_test_order(**params)
                    print(f'\n ** \nventa\n ** \n')
                    break # exito, salir del bucle 
                
                except Exception as e:
                    logging.error(f'error al crear la orden de venta : {e}')
                    await asyncio.sleep(2)
                    retries += 1
                
                         
            if retries == max_retries:
                logging.info(f'el numero maximo de intentos ha sido superdo, debido al error: {e}') 

    
    async def calcular_ganancias(self,precio_de_entrada, precio_actual):
        '''
        args:
        precio_de_entrada float():  el precio de entrada 
        
        return :  ganancias o perdidas actuales 
        '''
        if precio_de_entrada != None:
            await self.connect_Client()
            balance = self.brok.get_asset_balance('BTC')['free']
            earning = (precio_actual - precio_de_entrada) * balance
            return earning
        else :
            return None 
        
        
        
    async def calcule_percentage(self,earning,entry_price):
        '''
        args: 
        earning float():  requiere el calculo de las ganancias
        entry_price float(): requiere el precio de entrada  (compra)
        
        return : float(percentage_profit)
        '''
        if earning != None:
        
            await self.connect_Client()
            balance = self.brok.get_asset_balance('BTC')['free']
            porcentage_ganancia = (earning / (entry_price * balance)) * 100 
            
            return porcentage_ganancia
        else: 
            return None
