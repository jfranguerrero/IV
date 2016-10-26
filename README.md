# VuelaBot

[![Build Status](https://travis-ci.org/jfranguerrero/IV.svg?branch=master)](https://travis-ci.org/jfranguerrero/IV)

## Descripción del proyecto

El proyecto es un bot de Telegram que tiene como finalidad la búsqueda de precios de vuelos aprovechando la API de Skyscanner. El usuario introducirá aeropuerto de origen, destino, fecha de ida y fecha de vuelta y el bot le devolverá el precio más bajo para los datos indicados. Parte de esta información podrá ser guardada en una base de datos para determinar destinos más deseados y fechas donde los viajeros compran más vuelos.

Adicionalmente puede que el bot pueda llegar a ofrecer en un futuro precios sin fechas exactas ofreciendo el día que es más barato ir a un destino o buscar los destinos más baratos de un determinado país.

Para tener una mayor explotación comercial en la fase final del proyecto se introducirán funcionalidades para consultar precios de hoteles indicando la ciudad deseada.

## Servicios

- Una base de datos para almacenar información que pueda ser de interés como los códigos de aeropuerto o de aerolíneas.

- Una API de bots de Telegram basada en Python para hacer el desarrollo de una forma sencilla. Con esto aprovecharemos el potencial que nos ofrece un servicio como Telegram.

- API en Python de Skyscanner para realizar peticiones y obtener los precios de los vuelos.

## Funcionamiento

Actualmente el bot dispone de dos funciones.

- ```/aeropuertos```: Muestra el código de aeropuerto y ciudad de los aeropuertos españoles. proximamente se mostrarán aeropuertos de toda Europa indicándole el país deseado.

- ```/buscarvuelo Código_aeropuerto_ida código_aeropuerto_vuelta fecha_ida fecha_vuelta```: De esta forma se realizará la búsqueda en las fechas y aeropuertos determinados para ofrecer el mejor precio posible. Por ejemplo sería así :```/buscarvuelo AGP BCN 12/11/2016 23/12/2016```


## Integración continua

Para la integración continua se ha usado Travis-CI para realizar los tests. Para llevarlo a cabo se ha necesitado crear un fichero .travis.yml el cual sepa ejecutar un makefile que instale las dependencias y ejecute los tests. El fichero sería el siguiente:


```
branches:
  except:
    - Documentacion

language: python
python:
  - "2.7"

# command to install dependencies
install: make install

# command to run tests
script: make test
```

El Makefile para la instalación de la dependencias y la ejecución de los diversos tests ha sido el siguiente:

```

install:
	pip install -r requirements.txt

test:
	cd vuelaBot && python test_vuelabot.py

execute:
  cd vuelaBot && python vuelabot.py

```

Autmomáticamente Travis comenzará a instalar las dependencias e iniciar los tests. Como en nuestro caso se una una API de Skyscanner se necesita un token el cual debemos indicárselo a Travis como variable de entorno en sus opciones.

Si todo está correcto nos aparecerá una imagen similar a la siguiente con la imagen verde.

![alt text](http://i64.tinypic.com/deppux.png)
