
## Proyecto de Trading Bot
Este es un proyecto de Trading Bot escrito en Python que utiliza la API de Binance para monitorear y ejecutar operaciones basadas en el indicador RSI (Índice de Fuerza Relativa).

## Descripción
Este proyecto está diseñado para monitorear el precio de un par de trading en Binance y realizar operaciones de compra y venta basadas en las lecturas del RSI. El RSI es un indicador técnico utilizado comúnmente en análisis técnico para identificar condiciones de sobrecompra y sobreventa en un activo.

##  librerias y Características 

we used websocket for python

'pip install binance-connector' 

'pip install pandas' 

'pip install TA-Lib'


si tienes problemas al instalar talib intenta lo siguiente  for linux

 'wget https://sourceforge.net/projects/ta-lib/files/ta-lib/0.4.10/ta-lib-0.4.10-src.tar.gz'


$ tar -xzf ta-lib-0.4.0-src.tar.gz
$ cd ta-lib/
$ ./configure --prefix=/usr
$ make
$ sudo make install


## Copy code
python tu_script.py
Asegúrate de modificar el valor de symbol y umbral_activacion según tus preferencias antes de ejecutar el script.

## Contribución
Si deseas contribuir a este proyecto, sigue estas pautas:

Abre un issue para discutir la contribución.
Crea un fork del proyecto en GitHub.
Trabaja en tu propia rama (branch).
Envía una solicitud de extracción (pull request) a la rama principal.
Créditos
Este proyecto utiliza la API de Binance y se basa en el análisis técnico del RSI. Agradecemos a la comunidad de desarrolladores de código abierto y a la plataforma Binance por proporcionar las herramientas necesarias para este proyecto.

## Licencia
Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE.md para obtener más detalles.