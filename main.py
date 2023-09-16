#%%
import websocket,json
import pandas as pd
import asyncio
from binance import AsyncClient, BinanceSocketManager
import logging
# from binance.client import 




logging.basicConfig()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
'''
        Debug :   10
        info:     20
        warning:  30
        error:    40 
        critical: 50 
'''
_secret = "ODhMTfZi3K9AeBmxXdtKH3gQfNxIz8GjyarmZWWkwtprWecomQngIV9yqb5XUvfV"

_key = "Y8xmWfwsQhHOCDFtunbhNyePj8SmeylNeASI9A1KWWONtzmzNCtL6CVCuvyV7x8K"


async def main():
    
    client = await  AsyncClient.create(api_key=_key,api_secret=_secret,testnet=True)
    
    bm = BinanceSocketManager(client)
    show = bm.kline_socket('BTCUSDT')
    # show_trade= bm.trade_socket('BTCUSDT')
    
    # enter the context manager
    
    
    # recive a message
    async with show as  showcm:
        while True:
            
            candle = await showcm.recv()
            close = pd.DataFrame({'price':float(candle['k']['c'])}, index=[pd.to_datetime(candle['E'],unit='ms')])
            
            
            print(close)

           
    
    # exit the context manager
    
    
    
    
    
    
if __name__=='__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    

#%%
    
    

# interval = '1m'
# cc = 'btcusdt'

# socket = f'wss://stream.binance.com:9443/ws/{cc}@kline_{interval}'
# # socket


# closes, highs, lows = [],[],[]
    
# def on_message(ws,message):
#     jso_message = json.loads(message)
#     candle = jso_message['k']
#     is_candle_close = candle['x']
#     close = candle['c']
#     high = candle['h']
#     low = candle['l']
#     vol = candle['v']
    
    
    
#     if is_candle_close:
#         closes.append(float(close))
#         highs.append(float(high))
#         lows.append(float(low))
#         print(closes)
#         print(highs)
#         print(lows)
    
    
    
    
# def on_close(ws):
#     logging.info('closed')
   


# ws = websocket.WebSocketApp(socket,on_message= on_message, on_close= on_close)



# ws.run_forever()