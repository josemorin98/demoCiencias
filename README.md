# Demo Ciencias de Datos

Demo enfocado para ser utilizado en forma de usuario y conocer la comunicación entre los diferentes contenedores.

El demo consiste en 4 contenedores con las siguientes características:

- Container 1: (Postgres) Una base de datos.
- Container 2: (Processing) Contenedor enfocado a realizar operaciones básicas.
- Container 3: (Plot) Contenedor enfocado a crear boxplots sobre los datos generados.
- Container 4: (Middelware) Contenedor encargado de interactuar entre el usuario y los servicios.

El diseño del demo queda de la siguiente manera:

![Arquitectura](./arq.png "Arquitectura")

# Docker RUN

Para poder ejcutar los contenedores se necesita el siguiente comando:

- Container 1 (Postgres):

`docker run postgres:latest `
