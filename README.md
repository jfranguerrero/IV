# VuelaBot

[![Build Status](https://travis-ci.org/jfranguerrero/IV.svg?branch=master)](https://travis-ci.org/jfranguerrero/IV)

[![Heroku Deploy](https://www.herokucdn.com/deploy/button.svg)](https://intense-tor-85639.herokuapp.com/  )


[![Docker](https://camo.githubusercontent.com/8a4737bc02fcfeb36a2d7cfb9d3e886e9baf37ad/687474703a2f2f693632382e70686f746f6275636b65742e636f6d2f616c62756d732f7575362f726f6d696c67696c646f2f646f636b657269636f6e5f7a7073776a3369667772772e706e67)](https://hub.docker.com/r/jfranguerrero/iv/)

## Descripción del proyecto

El proyecto es un bot de Telegram que tiene como finalidad la búsqueda de precios de vuelos aprovechando la API de Skyscanner. El usuario introducirá aeropuerto de origen, destino, fecha de ida y fecha de vuelta y el bot le devolverá el precio más bajo para los datos indicados. Parte de esta información podrá ser guardada en una base de datos para determinar destinos más deseados y fechas donde los viajeros compran más vuelos.

Adicionalmente puede que el bot pueda llegar a ofrecer en un futuro precios sin fechas exactas ofreciendo el día que es más barato ir a un destino o buscar los destinos más baratos de un determinado país.

Para tener una mayor explotación comercial en la fase final del proyecto se introducirán funcionalidades para consultar precios de hoteles indicando la ciudad deseada.

## Servicios

- Una base de datos para almacenar información que pueda ser de interés como los códigos de aeropuerto o de aerolíneas.

- Una API de bots de Telegram basada en Python para hacer el desarrollo de una forma sencilla. Con esto aprovecharemos el potencial que nos ofrece un servicio como Telegram.

- API en Python de Skyscanner para realizar peticiones y obtener los precios de los vuelos.

## Funcionamiento

Para agregar el bot en funcionamiento se puede usar el siguiente enlace:

https://telegram.me/vuelaBot

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

## Despliegue en un PaaS

El Paas elegido para el despliegue es Heroku debido a su sencillez. La idea del despliegue
es que cuando se actualice nuestro repositorio (mediante un git push) automáticamente
se ejecuten los tests realizados por Travis-CI y si éstos son correctos, se despliegue
en Heroku.

Crearemos una app mediante ```heroku create``` y una base de datos que donde almacenar datos con ```heroku addons:create heroku-postgresql:hobby-dev ```

El problema que se nos presenta es que anteriormente trabajábamos con sqlite y ahora estamos usando Postgresql.

Para ello lo que se ha realizado es modificar la anterior base de datos sqlite3 a Postgresql y
para que funcione correctamente con la base de datos con Heroku, se ha introducido lo siguiente en la forma de conexión:

```
urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])

con_bd =psycopg2.connect(database=url.path[1:], user=url.username, password=url.password, host=url.hostname, port=url.port)
    c = con_bd.cursor()

```

Posteriormente se ha realizado un fichero Procfile que indica a Heroku que fichero debe ejecutar para lanzar la aplicación. El Procfile tiene la siguiente estructura:

```
worker: python vuelaBot/vuelabot.py
```

Finalmente debemos sincronizar el despligue de Heroku con Travis-CI y GitHub. Lo podemos llevar a cabo desde la configuración de nuestra aplicación en Heroku, en la sección de "Deploy". Conectamos con nuestro repositorio de GitHub y marcamos "Wait for CI to pass before deploy " para esperar a la realización de tets de Travis-CI para el despligue. En la siguiente imagen se puede apreciar la configuración:


![alt text](http://i67.tinypic.com/2uygdw0.png)

Se puede ver funcionando desde: https://telegram.me/vuelaBot

## Entorno de pruebas (Docker)

Para el entorno de pruebas se puede usar un contenedor docker todo tendremos todo lo necesario para hacer funcionar el proyecto. Para hacerlo funcionar necesitaremos:
```
docker pull jfranguerrero/iv

sudo docker run -e "token_vuelabot=XXX" -e "DATABASE_URL=XXX" -e "api_skyscanner=XXX" -i -t jfranguerrero/iv
```

Editando las variables de los tokens de las API con los valores que el usuario haya obtenido.

## Despliegue en un IAAS

Para el despliegue de nuestra aplicación en Microsoft Azure necesitamos Vagrant y Ansible.
Vagrant lo instalamos mediante ```sudo apt-get install vagrant```.

Para instalar Ansible el comando a introducir es: ```sudo apt-get install ansible```.

Como vamos a usar Azure vamos a instalar sus respectivos plugins. Lo llevamos a cabo con:

```
vagrant plugin install vagrant-azure
```

Crearemos los certificados para el servidor y los subiremos a Azure. Su realización se realiza mediante:

```
openssl req -x509 -nodes -days 3650 -newkey rsa:2048 -keyout azure.pem -out azure.pem
openssl x509 -inform pem -in azure.pem -outform der -out azure.cer
chmod 600 azure.pem

```
Para subirlo vamos a configuración de Azure y dentro de ella la sección de certificados de administración.

Generamos un Vagrantfile mediante la orden ```vagrant init```.

Deberemos añadirle la respectiva configuación de Azure. Aquí podemos acceder al [Vagrantfile](https://github.com/jfranguerrero/IV/blob/master/Vagrantfile).

El siguiente paso es crear un fichero de configuración de [ansible](https://github.com/jfranguerrero/IV/blob/master/ansible.yml).

Creados estos ficheros podremos lanzar el despliegue mediante:

```
vagrant up --provider=azure
```

Podremos conectar por SSH a la máquina con ```vagrant ssh```.

Para ejecutar órdenes en la máquina creamos un fabfile el cual usaremos con Fabric.

Las ordenes de fabric que se han desarrollado son las siguientes:

- start: Ejecuta la aplicación.
- stop: Detiene la aplicación.
- download: Descarga la aplicación.
- delete: Elimina la aplicación.
- tests: Ejecuta los tests.
- nohup: Ejecuta la aplicación en background.

La orden a introducir en Fabric es:
```
fab -p "pass_maquina" -H usuario@vuelabot.cloudapp.net orden_de_fabric
```

También podremos realizar todo el despliegue de forma automática mediante el script deploy.sh.

## Adicional

Proyecto inscrito en el concurso de software libre de la OSL.

![alt text](http://i65.tinypic.com/sy76rm.png)
