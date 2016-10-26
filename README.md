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


