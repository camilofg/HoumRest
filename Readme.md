<p align="center">
  <img alt="HOUM logo" src="https://houm.com/static/brandImage/houmLogo.svg" width="320">
</p>

## Aplicación Houm

Codigo fuente para servicio REST para monitorear metricas definidas para entender la operación de los houmers, mejorar
la calidad de servicio y garantizar la seguridad de los houmers.

## Requerimientos previos:
Python 3.7 o versiones superiores (https://www.python.org/downloads/).
Git Bash (https://git-scm.com/downloads).
Redis-Server (https://redis.io/download).

## Configuración del Proyecto

1. Creación de una nueva carpeta donde se creara el ambiente virtual y se descargara el repositorio.
2. Ingresar a la carpeta recien creada y abrir git bash en esta ruta.
3. Crear el ambiente virtual, ejecutando el siguiente comando:
```
python -m venv venv
```
4. Instalar las dependencias necesarias para la ejecución de la aplicación, con el siguiente comando:
```
pip install -r requierement.txt
```

5. Iniciar la aplicación:

```
python manage.py runserver
```


La aplicación pose 3 endpoints descritos a continuación:

1. El endpoint es un POST para la creación de los registros de coordenadas d elos Houmers:

http://127.0.0.1:8000/positions/ 

El payload para el request de este endpoint es:

{
    "user": null,
    "latitude": null,
    "longitude": null
}

2. El siguiente endpoint es un GET, quien es el encargado de enlistar las visitas realizadas por cada Houmer con su 
   ubicación y duración, este endpoint tiene un queryString con el user_id y date, la fecha sera enviada con el formato
   yyyy-mm-dd:

http://127.0.0.1:8000/visits?user_id=1&date=2021-10-03   

El response de este endpoint sera el siguiente:

{
    "user": null,
    "latitude": null,
    "longitude": null,
    "visit_duration": null
}

3. El ultimo endpoint es un GET, con el cual podremos obtener los momentos y ubicaciones en los cuales el houmer 
sobrepaso cierto limite de velocidad. De igual manera tendra un queryString con el user_id, date y speed, este ultimo 
   definira la velocidad que ha sobrepasado el houmer y estara dada en Km/h:
   
http://127.0.0.1:8000/speed?user_id=1&speed=100&date=2021-10-03

El response para este endpoint tendrá la siguiente forma:

 {
        "user": 1,
        "latitude": "4.7118797",
        "longitude": "-74.1746589",
        "dateModified": "2021-10-03T02:51:09.414845Z",
        "speed": "262.0631"
}

## Nota
En el archivo config.ini del root se pueden modificar los parametros para definir el tiempo necesario para definir una 
visita y poderla diferenciar de ubicaciones en transito (el parametro se llama time), y el delta necesario para se 
considerado un desplazamiento y no movimientos internos dentro de la misma vivienda (el parametro se llama distance). 
Tambien en este archivo se define la url para redis la cual puede ser modificada en caso de ser necesario.
