# VuelaBot


## Descripción del proyecto

El proyecto es un bot de Telegram que tiene como finalidad la búsqueda de precios de vuelos aprovechando la API de Skyscanner. El usuario introducirá aeropuerto de origen, destino, fecha de ida y fecha de vuelta y el bot le devolverá el precio más bajo para los datos indicados. Parte de esta información podrá ser guardada en una base de datos para determinar destinos más deseados y fechas donde los viajeros compran más vuelos.

Adicionalmente puede que el bot pueda llegar a ofrecer en un futuro precios sin fechas exactas ofreciendo el día que es más barato ir a un destino o buscar los destinos más baratos de un determinado país.

Para tener una mayor explotación comercial en la fase final del proyecto se introducirán funcionalidades para consultar precios de hoteles indicando la ciudad deseada.

## Servicios

- Una base de datos para almacenar información que pueda ser de interés como los códigos de aeropuerto o de aerolíneas.

- Una API de bots de Telegram basada en Python para hacer el desarrollo de una forma sencilla. Con esto aprovecharemos el potencial que nos ofrece un servicio como Telegram.

- API en Python de Skyscanner para realizar peticiones y obtener los precios de los vuelos.
