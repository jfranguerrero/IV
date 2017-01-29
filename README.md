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

## Hito 5: Despliegue en un IAAS

Para el despliegue de nuestra aplicación en Microsoft Azure necesitamos Vagrant y Ansible.
Vagrant lo instalamos mediante ```sudo apt-get install vagrant```.

Para instalar Ansible el comando a introducir es: ```sudo apt-get install ansible```.

Como vamos a usar Azure vamos a instalar sus respectivos plugins. Lo llevamos a cabo con:

```
vagrant plugin install vagrant-azure
```

Es posible que se nos produzca un error en la instalación en Ubuntu 16.04. Para solventarlo se pueden seguir los pasos del siguiente [enlace](http://stackoverflow.com/questions/36811863/cant-install-vagrant-plugins-in-ubuntu-16-04/36991648#36991648).

El siguiente paso es crear una cuenta de Azure si no disponemos de ella. Podemos usar un código promocional si disponemos de él o usar el servicio de pago.

### Certificados

Crearemos los certificados para el servidor y los subiremos a Azure. Su realización se realiza mediante:

```
openssl req -x509 -nodes -days 3650 -newkey rsa:2048 -keyout azure.pem -out azure.pem
openssl x509 -inform pem -in azure.pem -outform der -out azure.cer
chmod 600 azure.pem

```
Para subirlo vamos a configuración de Azure y dentro de ella la sección de certificados de administración.

![alt text](http://i68.tinypic.com/d4snr.png)

### Vagrant

Generamos un Vagrantfile mediante la orden ```vagrant init```.

Deberemos añadirle la respectiva configuación de Azure. Aquí podemos acceder al [Vagrantfile](https://github.com/jfranguerrero/IV/blob/master/Vagrantfile).

El siguiente paso es crear un fichero de configuración de [ansible](https://github.com/jfranguerrero/IV/blob/master/ansible.yml). En él indicaremos los paquetes a instalar y el repositorio de la aplicación para descargarla.

Creados estos ficheros podremos lanzar el despliegue mediante:
```
vagrant up --provider=azure
```
Tardará unos minutos en la instalación pero si no se produce ningún error tendremos nuestra máquina totalmente funcional. Podemos comprobarlo desde la página de Azure.

![alt text](http://i63.tinypic.com/x3h3qh.png)

Si queremos acceder por ssh a la máquina simplemente introduciremos ```vagrant ssh```.

### Fabric

Fabric nos permite administrar una máquina externa desde nuestra propia máquina. La instalaremos con:
```
sudo apt-get install fabric
```

Necesitaremos un fichero de instrucciones para fabric donde indicarle que debe realizar en la máquina. Este lo llamaremos [fabfile](https://github.com/jfranguerrero/IV/blob/master/fabfile.py) y le indicaremos las ordenes de instalación, eliminación, tests, ejecución y detención de la aplicación.

Las ordenes de fabric que se han desarrollado son las siguientes:

- start: Ejecuta la aplicación.
- stop: Detiene la aplicación.
- download: Descarga la aplicación.
- delete: Elimina la aplicación.
- tests: Ejecuta los tests.

Un problema que se presenta es que cuando salimos de fabric nuestra aplicación deja de funcionar. Este problema se ha resuelto gracias a nohup el cual nos permite ejecutarla en segundo plano.

Para ejecutar una orden en nuestra máquina mediante fabric deberemos introducir lo siguiente:
```
fab -p "pass_maquina" -H usuario@vuelabot.cloudapp.net orden_de_fabric

```

### Automatización

Se ha realizado un [script](https://github.com/jfranguerrero/IV/blob/master/deploy.sh) cuya finalidad es realizar todos los pasos anteriores del despliegue de forma totalmente automática.

```
#!/bin/bash

sudo apt-get update

wget https://releases.hashicorp.com/vagrant/1.8.7/
sudo dpkg -i vagrant_1.8.7_x86_64.deb

sudo vagrant plugin install vagrant-azure

# Instalación Ansible
sudo apt-get install ansible


# Despliegue en Azure
sudo vagrant up --provider=azure

# Despliegue de la aplicación con Fabric
sudo pip install fabric
# Actualiza el supervisor
fab -p password -H usuario@vuelabot.cloudapp.net nohup
```

Aquí tenemos un ejemplo del funcionando:

![alt text](http://i68.tinypic.com/9602zq.png)
