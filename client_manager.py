from binance.client import Client
from config import __secret as _secret
from config import __key as _key
from time import sleep
import asyncio
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
    

    async def connect_Client(self):
            '''
            inicializa y conecta  el Cliente
            '''
            while True:
                try :
                # crea una instancia del Cliente 
                    self.brok =Client(api_key=_key,api_secret=_secret,testnet=True)
                    logging.info(f"iniciando coneccion con la Api ")
                    return self.brok
                except Exception as e:
                    logging.warning(f"no se ha podido establecer la coneccion con binance Appi -> {e}")
                    sleep(5)
                    
    async def order_buy(self, max_retries = 3):
            await self.connect_Client()
            retries = 0 
            while retries < max_retries:
                try:                    
                    self.brok.create_test_order(
                        symbol = 'BTCUSDT',
                        side = self.brok.SIDE_BUY,
                        type = self.brok.ORDER_TYPE_MARKET,
                        quantity = 100
                    )
                    print(f'\n ** \ncompra\n ** \n')
                    break # exito , salir del bucle 
                
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
                    self.brok.create_test_order(
                        symbol = 'BTCUSDT',
                        side = self.brok.SIDE_SELL,
                        type = self.brok.ORDER_TYPE_MARKET,
                        quantity = 100,
                        recvWindow=60000
                     )
                    print(f'\n ** \nventa\n ** \n')
                    break # exito, salir del bucle 
                
                except Exception as e:
                    logging.error(f'error al crear la orden de venta : {e}')
                    await asyncio.sleep(2)
                    retries += 1
                
                         
            if retries == max_retries:
                logging.info(f'el numero maximo de intentos ha sido superdo, debido al error: {e}') 
