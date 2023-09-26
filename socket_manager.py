import pandas as pd
from binance import AsyncClient, BinanceSocketManager
from binance.client import Client
from client_manager import client_
from config import __secret as _secret
from config import __key as _key
from time import sleep
from ind import indicators
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

class socket_manager_date:
    def __init__(self,symbol :str, umbral_activacion :int) -> None:
        '''
        Inicializa una instancia de la clase SocketManagerDate.

        Args:
            symbol (str): El símbolo del par de trading que se va a monitorear.
            umbral_activacion (int): Umbral del indicador RSI para activar la estrategia (ejemplo: 30 o 25).
        '''
        
        self.max_candle = 100
        self.symbol = symbol
        self.data = pd.DataFrame(columns=['PRICE','RSI'])
        
        self.umbral_activacion = umbral_activacion
        
        
        # manager logicos 
        self.on_trade = False
        
        
    async def conncect_socket(self):
        '''
        inicializa la creacion  del client y coneccion del socket
        '''
        while True:
            try:
            # Crea una instancia del cliente asincrónico de Binance
                self.client = await AsyncClient.create(api_key=_key,api_secret=_secret)
                self.bsm = BinanceSocketManager(self.client)
                
            # Configura una conexión WebSocket para recibir datos de velas (candles)
                self.kline_data = self.bsm.kline_socket(self.symbol)
                
                return self.kline_data
                
            except Exception as e:
                await asyncio.sleep(5)
                print(f'conect failed socket -> {e}')
                
    
        
                
    async def process_data(self):
        try:
        # esperamos la coneccion del socket
            await self.conncect_socket()
            
            async with self.kline_data as k_d:
                while True:
                    # await asyncio.sleep(0.1)  # Esperar 1 segundo entre ciclos.
                    
                    msg = await k_d.recv()
                    klines = pd.DataFrame({'PRICE': float(msg['k']['c'])}
                                          ,index=[pd.to_datetime(msg['E'],unit='ms')])
                    
                    if msg['k']['x']:
                        self.data = pd.concat([self.data, klines], axis=0)
                        print('Nueva vela')

                    if len(self.data) > self.max_candle:
                        self.data = self.data.iloc[-self.max_candle:]

                    if len(self.data['PRICE']) >= 14:
                        self.data['RSI'] = indicators(self.data['PRICE']).rsi()
                        print(self.data.iloc[-1])
                        print(len(self.data))

                    #  LOGUICA COMERCIAL 


                        if self.data['RSI'].iloc[-1] <= self.umbral_activacion and not self.on_trade:
                            self.on_trade = True
                            buy =  client_()
                            await buy.order_buy()
                            
                            
                        if self.data['RSI'].iloc[-1] >= 70 and self.on_trade:
                            self.on_trade = False
                            sell = client_()
                            sell.order_buy()
                            
                    
                    else:
                        print(klines)
                        print(f"La data tiene: {len(self.data)}")
                
                
                
        except Exception as e:
            logging.error(f"Error en la ejecución: {str(e)}")
            await asyncio.sleep(5)
            
        