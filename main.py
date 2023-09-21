
import asyncio
from socket_manager import socket_manager_date



    
if __name__=='__main__':
    process = socket_manager_date('BTCUSDT')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(process.process_data())
    