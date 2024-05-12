# dictator with gpt
 


## Instalación sin docker (python 3.12)

### Creación del entorno virtual (python 3.12)

1. Clona este repositorio en tu máquina local:

2. Dirígete a la ubicación donde crearás un entorno virtual

3. Crea un entorno virtual:

    ```
    python -m venv env
    ```
4. Activa el entorno virtual: 

    ```
    cd env/Scripts
    activate.bat
    ```

5. Dirígete a la ubicación de proyecto

6. Instala las dependencias:

    ```
    pip install -r requirements.txt
    ```

### Despliegue del proyecto:

1. Dirígete a la ubicación de proyecto

2. Despliega el proyecto (el puerto 80 puede ser diferente. Si no se especifica, por defecto es 8000):

    ```
    otree devserver 80
    ```

3. Accede a la aplicación en tu navegador web visitando `http://localhost:8000`.


## Instalación con docker

Para instalar y ejecutar este proyecto, asegúrate de tener Docker instalado en tu sistema.

1. Clona este repositorio en tu máquina local:

2. Navega al directorio del repositorio:

    ```
    cd dictator-with-gpt
    ```

3. Construye la imagen de Docker utilizando el Dockerfile proporcionado:

    ```
    docker build -t dictator-with-gpt .
    ```

4. Una vez que la imagen se haya construido correctamente, puedes ejecutar un contenedor basado en esta imagen:

    ```
    docker run -d -p 80:8000 dictator-with-gpt
    ```

    Este comando ejecutará el contenedor en segundo plano y expondrá el puerto 80 de tu máquina local al puerto 8000 del contenedor.

5. Accede a la aplicación en tu navegador web visitando `http://localhost:80`.



### Detener y Eliminar un Contenedor

Si deseas detener o eliminar el contenedor Docker, sigue estos pasos:

1. Listar contenedores activos:

    ```
    docker ps
    ```

1. Detener el contenedor con el id:

    ```
    docker stop id-contenedor
    ```

    Esto detendrá el contenedor en ejecución sin eliminarlo.

2. Eliminar el contenedor:

    ```
    docker rm id-contenedor
    ```

    Esto eliminará el contenedor Docker.