## Práctica 0: Git y GitHub

### Creación de claves SSH
Para la creación de las claves necesariarias simplemente hacemos en nuestra terminal:

```
ssh-keygen -t rsa -b 4096 -C "jfranguerrero@gmail.com"
```

La clave pública la necesitaremos para introducirla en GitHub. Esta en mi caso está ubicada en la ruta:+
```
/home/francisco/.ssh/id_rsa.pub
```

Finalmente introduciremos esta clave en nuestra cuenta de GitHub desde las opciones de usuario para que funcione correctamente.

### Creación de repositorio y fork del repositorio de la asignatura

Este paso es muy simple. Creamos un repositorio desde la interfaz de GitHub y hacemos un fork del repositorio de la asignatura.

### Creación de branch

Para la creación de un branch donde introducir nuestra práctica en el repositorio debemos ir a la interfaz y pinchar en branch donde podremos crear uno nuevo. En este caso lo llamaremos Hito0 por ejemplo. Ahí podremos introducir la práctica inicial.

### Creación del milestone e issues

Para la creación de un milestone desde nuestro repositorio vamos a issues y desde ahí a milestone. Le damos a New Milestone y le introducimos un título y una descripción. Adicionalmente si no requerimos podemos introducir una fecha.

En este milestone deberemos añadir los distintos issues a realizar para que así se muestre el porcentaje de realización en el milestone.

### Pull Request

Finalmente solo necesitamos realizar un pull request en el repositorio de la asignatura.


## Hito2: Integración continua

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


## Hito 3: Despliegue en un PaaS

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

## Hito 4: Entorno de pruebas

El entorno de pruebas se va a llevar a cabo en contenedores docker.

Lo primero que debemos realizar es crear un fichero Dockerfile. En este fichero le indicaremos la versión de Ubuntu a usar y los comandos para instalar git, descargar el repositorio del proyecto, instalar python y pip y ejecutar el makefile de instalación del proyecto.

![alt text](http://i64.tinypic.com/2uqlpqo.png)

El siguiente paso es registrarnos en DockerHub. Tras registrarnos enlazamos nuestra cuenta con GitHub. Esto lo llevamos a cabo desde opciones en Linked Accounts.

![alt text](http://i64.tinypic.com/flwyux.png)

Ahora debemos asociar nuestro repositorio para que se cree la imagen de forma automática. Para ello vamos a create y create automated build. Aquí nos permitirá elegir el repositorio para crear su imagen.

![alt text](http://i63.tinypic.com/95ot5c.png)

En el momento en el cual se realice un commit en el repositorio automáticamente se creará una nueva imagen del contenedor para descargar.

![alt text](http://i63.tinypic.com/dxg65u.png)

Se creará una imagen la cual descargaremos mediante ```docker pull jfranguerrero/iv```.

Cuando esté descargada la ejecutamos con ```sudo docker run -e "token_vuelabot=XXX" -e "DATABASE_URL=XXX" -e "api_skyscanner=XXX" -i -t jfranguerrero/iv```

Debemos tener en cuenta el introducir los tokens para poder conectar a las APIs y a la base de datos.

[![Docker](https://camo.githubusercontent.com/8a4737bc02fcfeb36a2d7cfb9d3e886e9baf37ad/687474703a2f2f693632382e70686f746f6275636b65742e636f6d2f616c62756d732f7575362f726f6d696c67696c646f2f646f636b657269636f6e5f7a7073776a3369667772772e706e67)](https://hub.docker.com/r/jfranguerrero/iv/)
