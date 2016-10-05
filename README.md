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



## Primer hito: Estructuración y tema del proyecto.

### Prerrequisitos

- [x]   Tener aprobado el hito 0
- [x]   Tener alcanzado el 80% de los objetivos del tema

### Descripción del proyecto

El proyecto es un bot de Telegram que tiene como finalidad la búsqueda de precios de
vuelos aprovechando la API de Skyscanner. El usuario introducirá aeropuerto de origen, destino, fecha de ida y fecha de vuelta y el bot le devolverá el precio más bajo para los datos indicados. Parte de esta información podrá ser guardada en una base de datos para determinar destinos más deseados y fechas donde los viajeros compran más vuelos.

Adicionalmente puede que el bot pueda llegar a ofrecer en un futuro precios sin fechas exactas ofreciendo el día que es más barato ir a un destino o buscar los destinos más baratos de un determinado país.

- Para la realización del proyecto necesitaremos tener instalado Python que es el lenguaje que se usará.

- Una base de datos para almacenar información que pueda ser de interés.

- Una API de bots de Telegram basada en Python para hacer el desarrollo de una forma sencilla.

- API en Python de Skyscanner para realizar peticiones y obtener los precios de los vuelos.

- Servicio en la nube para montar nuestro bot.

- Servicios de monitorización y logs de errores para estudiar la carga y los errores que puedan aparecer en el sistema.
