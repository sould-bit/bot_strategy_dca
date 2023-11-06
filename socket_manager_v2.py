import websocket, json
import pandas as pd
from ind import indicators
from client_manager import client_
from capture_info import capture_info

from time  import sleep
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




symbol = "btcusdt"
interval = "1m"
socket = f"wss://stream.binance.com:9443/ws/{symbol}@kline_{interval}"

data = pd.DataFrame(columns=['PRICE','RSI']) # DATA FRAME WHITH TWO COLUMNS

class socket_manager_date:
    logging.info("accediendo al socket_manager_date")
    def __init__(self,size:int,size_segurity:int, umbral_activacion :int, ordenes_seguridad, riesgo_segurity: int,target:float) -> None:
        '''
        Inicializa una instancia de la clase SocketManagerDate.

        Args:
            data : la data 
            object: objeto que se concecta con el cliente de binance atravez de la llave 
        
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
        self.object =  client_()
        
        
        
        
        
        
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
        
        
        #Manager operacionales
        self.cantidad_activos = 0
        self.total_cantidad_activos = 0 
        
    # Calculamos  cantidad de activos     
    def calcular_antidad_activos_por_precio(self, size: float):
        '''
        Calcula la cantidad de activos basada en el tamaño de inversión principal.

        Args:
            size (float): El tamaño de inversión principal.
        '''
        self.cantidad_activos = size / kline
        self.total_cantidad_activos += self.cantidad_activos
        
    # Calculamos el costo promedio 
    def costo_promedio(self,lista_compras:list[dict])-> float:
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
    
    # LOGUICA COMERCIAL
    def process_data(self): 
        
        self.earning = self.object.calcular_ganancias(self.entry_price,kline['PRICE'])
        if self.earning != None:
            print(f'earning: {self.earning}')
            self.percentage_profit = self.object.calcule_percentage(self.earning,self.entry_price)
        
        if data['RSI'].iloc[-1] != None  and  data['RSI'].iloc[-1] <= self.umbral_activacion and not self.on_trade:
            self.object.order_buy(self.size) # realizamos la compra con el tamaño determinado por size 
            self.calcular_antidad_activos_por_precio(size=self.size)
            self.entry_price = kline['PRICE']
            self.trades.append({'cantidad': self.cantidad_activos,'precio': kline['PRICE']})
            self.on_trade = True
            capture_info(time=kline.index[-1], type="BUY",symbol="btc",price=kline['PRICE'],cantidad=self.cantidad_activos,earnings="Nan")
            self.cantidad_activos = 0
            logging.info("compra")
            print(f' trades: {self.trades}')
            
        if self.percentage_profit  != None  and self.percentage_profit <= self.riesgo_segurity and len(self.trades) < self.ordenes_de_seguridad and self.on_trade: 
            # compramos para promediar  con el precio de  seguridad 
            self.object.order_buy(self.size_segurity)
            # calculamos la cantidad de activos 
            self.calcular_antidad_activos_por_precio(size=self.size_segurity)
            # agregamos lod datos a la lista , que nos ayuda a promediar 
            self.trades.append({'cantidad': self.cantidad_activos,'precio': kline['PRICE']})
            # promediamos  el precio segun los datos 
            self.entry_price = self.costo_promedio(self.trades)
            # actualizamos el profit actual 
            self.earning = self.object.calcular_ganancias(self.entry_price,kline['PRICE'])
            capture_info(time=kline.index[-1], type="BUY",symbol="btc",price=kline['PRICE'],cantidad=self.cantidad_activos,earnings="Nan")
            self.cantidad_activos = 0
            logging.info("recompra")
            print(f'trades 2: {self.trades}')
            
            
            
        if self.on_trade and self.percentage_profit >= self.target:  
            self.object.order_sell()
            capture_info(time=kline.index[-1], type="SELL",symbol="btc",price=kline['PRICE'],cantidad=self.cantidad_activos,earnings=self.earning)
            #managers logicos 
            
            self.on_trade = False
            self.trades = []
            self.entry_price = None
            self.earning = None
            self.percentage_profit = None
            #Manager operacionales
            
            self.cantidad_activos = 0
            self.total_cantidad_activos = 0 
            logging.info("venta")
            
            
def on_message(ws, message):
    
    
    
    max_candle = 100
    
    
    
    try:
        
        global data # mantenemos las varoiables globales, para que  la funcion on_message no la omita 
        global kline# mantenemos las varoiables globales, para que  la funcion on_message no la omita 
        '''
        data : variable
        kline : variable global
        '''
        
        json_message = json.loads(message)
        # event_time = json_message["E"] #  event time of each kline
        # candle = json_message["k"] # dict with values 
        # candle_is_closed = candle["x"] # close interval kline 
        # stream_close =  float(candle["c"]) # close price actual 
        kline =  pd.DataFrame({'PRICE': float(json_message['k']['c'])}
                                              ,index=[pd.to_datetime(json_message['E'],unit='ms')])
        
        # verificamos la klnie de cierre temporal
        if json_message['k']['x']:
            data = pd.concat([data,kline])
            print(data.tail(3))
            
            
        # controlar el limite
        if len(data) > max_candle:
            '''
             queremos mantener la cantidad de datos controlada , 
             hemos echo un estudio y el rsi nesesita al rededor de 60 datos para ser calculado con precicion 
             definimos el maximo un poco por encima , dejandolo en 100 candles 
            '''
            data = data.iloc[-max_candle:]
            
            
        '''   
            el numero 15 es sujeto  a prueba , al concluir el projecto debera ser cambiado manualmente a  minimo 60 
            realizamos los calculos del rsi nesesarios 
        '''
        # Calculamos el [RSI] 
        if len(data) >  90:
            data['RSI'] = indicators(data['PRICE']).rsi()
            
            # sujeto a  prueba imprimir la data completa 
            #print(data)
            # realizamos el informe 
            logging.info(f"\n{data.iloc[-1]}")
            logging.info(f"La data tiene: {len(data)}\n")
            
        # LOGICA COMERCIAL
            process = socket_manager_date( size=10,size_segurity=15,umbral_activacion=30,ordenes_seguridad=16,riesgo_segurity=-3,target=2.1)
            process.process_data()
            
            
            
            
        else:
            logging.info(f"{kline['PRICE'].iloc[-1]}")
            logging.info(f"La data tiene: {len(data)}\n")
        
    except Exception as e :
        logging.error(f"error en la ejecucion {e}")
        sleep(5)
        

def on_close(ws):
    print("### closed ###")



ws = websocket.WebSocketApp(socket,on_message=on_message, on_close=on_close)

ws.run_forever()










