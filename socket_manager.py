import pandas as pd
from binance import BinanceSocketManager, AsyncClient
from client_manager import client_
from config import secreta
from config import keya
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
    def __init__(self,symbol :str,size:int,size_segurity:int, umbral_activacion :int, ordenes_seguridad, riesgo_segurity: float,target:float) -> None:
        '''
        Inicializa una instancia de la clase SocketManagerDate.

        Args:
            symbol(str): par de divisa cripto 
            size (int): Tamaño de la inversión principal.
            size_segurity (int): Tamaño de reinversión cuando el riesgo de seguridad es activado.
            umbral_activacion (int): Umbral del indicador RSI para activar la estrategia (ejemplo: 30 o 25).
            ordenes_segurity (int): Número máximo de órdenes de seguridad que se pueden realizar en un ciclo de trading.
            riesgo_seguridad (float): Punto de recompra para promediar cuando se activa el riesgo  el numero debe ser negativo .
            target (float): Objetivo de take profit en porcentaje
        '''
        
        self.max_candle = 100
        self.symbol = symbol
        self.data = pd.DataFrame(columns=['PRICE','RSI'])
        
        
        
        # params  de ciclo de trading  
        self.size = size
        self.size_segurity = size_segurity
        self.umbral_activacion = umbral_activacion
        self.ordenes_de_seguridad = ordenes_seguridad
        self.riesgo_segurity = riesgo_segurity
        self.target = target
        
        
        #managers logicos 
        self.on_trade = False
        self.entry_price = None
        self.trades = []
        self.earning = None
        self.percentage_profit = None
        
        
        #manager operacionales
        self.cantidad_activos = 0
        self.total_cantidad_activos = 0 
        
        
    async def conncect_socket(self):
        '''
        inicializa la creacion  del client y coneccion del socket
        '''
        while True:
            try:
            # Crea una instancia del cliente asincrónico de Binance
                self.client = await AsyncClient.create(api_key=keya,api_secret=secreta)
                self.bsm = BinanceSocketManager(self.client)
                
            # Configura una conexión WebSocket para recibir datos de velas (candles)
                self.kline_data = self.bsm.kline_socket(self.symbol)
                
                return self.kline_data
                
            except Exception as e:
                await asyncio.sleep(5)
                print(f'conect failed socket -> {e}')
                
    
    async def calcular_antidad_activos_por_precio(self, size: float):
        '''
        Calcula la cantidad de activos basada en el tamaño de inversión principal.

        Args:
            size (float): El tamaño de inversión principal.
        '''
        self.cantidad_activos = size / self.klines
        self.total_cantidad_activos += self.cantidad_activos
        
        
    async def costo_promedio(self,lista_compras:list[dict])-> float:
        '''calcula el costo promedio de una lista de compras

            Args:
                lista_compras (list[dict]): Una lista de diccionarios, donde cada diccionario tiene las claves "cantidad" y "precio".

            returns:
                float :el costo promedio de las compras.
        '''
        
        total_invertido = sum(compra["cantidad"] * compra["precio"] for compra in lista_compras)
        total_cantidad = sum(compra["cantidad"] for compra in lista_compras)
        
        costo_promedio = total_invertido / total_cantidad if total_cantidad > 0  else 0
        
        return costo_promedio
        
                
    async def process_data(self):
        try:
        # esperamos la coneccion del socket
            await self.conncect_socket()
            
            async with self.kline_data as k_d:
                while True:
                    # await asyncio.sleep(0.9)  # Esperar 1 segundo entre ciclos.
                    object = client_()

                    self.earning = await object.calcular_ganancias(self.entry_price,self.klines)
                    self.percentage_profit = await object.calcule_percentage(self.earning,self.entry_price)
                    
                    msg = await k_d.recv()
                    self.klines = pd.DataFrame({'PRICE': float(msg['k']['c'])}
                                          ,index=[pd.to_datetime(msg['E'],unit='ms')])
                    
                    if msg['k']['x']:
                        self.data = pd.concat([self.data, self.klines], axis=0)
                        print('Nueva vela')

                    if len(self.data) > self.max_candle:
                        # eliminamos ,  mantenemos la cantidad de datos en 100 velas  en data frame 
                        self.data = self.data.iloc[-self.max_candle:]

                    if len(self.data['PRICE']) >= 14:
                        self.data['RSI'] = indicators(self.data['PRICE']).rsi()
                        print(self.data.iloc[-1])
                        print(len(self.data))

                    #  LOGUICA COMERCIAL 


                        if self.data['RSI'].iloc[-1] <= self.umbral_activacion and not self.on_trade:
                            # object =  client_()
                            await object.order_buy(self.size)
                            self.calcular_antidad_activos_por_precio(size=self.size)
                            self.entry_price = self.klines
                            self.trades.append({'cantidad': self.cantidad_activos,'precio': self.klines})
                            self.on_trade = True
                        
                        
                        if self.percentage_profit <= self.riesgo_segurity and len(self.trades) < self.ordenes_de_seguridad and self.on_trade: 
                            # compramos para promediar  con el precio de  seguridad 
                            await object.order_buy(self.size_segurity)
                            self.calcular_antidad_activos_por_precio(size=self.size_segurity)
                            self.trades.append({'cantidad': self.cantidad_activos,'precio': self.klines})
                            
                            
                            
                            
                        
                        
                            
                            
                        if self.data['RSI'].iloc[-1] >= 70 and self.on_trade:
                            self.on_trade = False
                            sell = client_()
                            sell.order_buy()
                            
                    
                    else:
                        print(self.klines)
                        print(f"La data tiene: {len(self.data)}")
                
                
                
        except Exception as e:
            logging.error(f"Error en la ejecución: {str(e)}")
            await asyncio.sleep(5)
            
        