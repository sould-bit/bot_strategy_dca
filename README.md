
## Proyecto de Trading Bot
Este es un proyecto de Trading Bot escrito en Python que utiliza la API de Binance para monitorear y ejecutar operaciones basadas en el indicador RSI (Índice de Fuerza Relativa).

## Descripción
Este proyecto está diseñado para monitorear el precio de un par de trading en Binance y realizar operaciones de compra y venta basadas en las lecturas del RSI. El RSI es un indicador técnico utilizado comúnmente en análisis técnico para identificar condiciones de sobrecompra y sobreventa en un activo.

## Características
Conexión asincrónica a la API de Binance.
Recepción de datos de velas (candles) en tiempo real.
Cálculo del RSI para tomar decisiones comerciales.
Lógica de compra y venta automatizada basada en el RSI.
Registro de eventos y errores en un archivo de registro.
Requisitos
Asegúrate de tener los siguientes requisitos instalados en tu entorno de desarrollo:

Python 3.7 o superior.
Bibliotecas Python: pandas, binance, time, entre otras (verifica los requisitos específicos en el código).
Instalación
Clona este repositorio:
bash
Copy code
git clone https://github.com/tu_usuario/tu_proyecto.git
cd tu_proyecto
Instala las dependencias:
bash
Copy code
pip install -r requirements.txt
Configura las credenciales de tu cuenta de Binance en el archivo config.py.
Uso
Para ejecutar el Trading Bot, utiliza el siguiente comando:


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