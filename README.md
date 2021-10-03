# Arquitectura202114-Seguridad

# ¿Cuál es el punto de sensibilidad?
Autenticador en el API Gateway, para comprobar que un componente de autorización en el API Gateway permite autenticarse con los microservicios
# ¿Qué utiliza el experimento?
El experimento utiliza un API Gateway que contiene un certificado SSL autofirmado para realizar comunicación HTTPS con el fin de asegurar que la información en tránsito es segura.

Utiliza un Autorizador que contiene una llave pública y privada, con la cual emite JWT tokens utilizando encriptación asimétrica, tokens que luego pueden ser verificados usando la llave pública por los microservicios.

Utiliza el microservicio de pacientes que a partir de la llave pública del autorizador verifica los token y así permite acceder a las funciones de listar, crear y consultar pacientes.

# ¿Cómo ejecuto el experimento?
Para ejecutar el experimento se necesita tener configurado en el computador ``docker`` y ``docker-compose``. Si utiliza windows basta con tener ``Docker Desktop``.

Ubiquese en la raiz del proyecto donde está el archivo ``docker-compose.yaml`` y ejecute:

```
docker-compose build
docker-compose up
```

Esto va a construir las imagenes requeridas y luego a montar y comunicar los contenedores de dichas imagenes.

Al tener corriendo la infraestructura se montarán 3 contenedores:

1. API Gateway
2. Autorizador
3. Microservicio Pacientes

El API Gateway se expondrá en el puerto 5000 por lo cual, el nginx estará disponible a través de ``https://localhost:5000`` usando https, ya que utiliza dicho protocolo.

Para el autorizador, la comunicación pasará a través del API Gateway por lo cual será usando la url ``https://localhost:5000/jwt``

El endpoint disponible para el autorizador es el que otorga un token haciendo un ``POST https://localhost:5000/jwt`` con el payload
```
{
    "tipo_usuario" : <string>:"auxiliar|administrativo",
    "id_usuario" : <numerico>
}
```

Para el microservicio de pacientes, la comunicación pasará a través del API Gateway por lo cual será usando la url ``https://localhost:5000/pacientes``

El microservicio de pacientes cuenta con los siguiente endpoints:

Creacion de paciente:
```
POST https://localhost:5000/pacientes
Payload:
{
    "nombres" : <string>,
    "apellidos" : <string>,
    "celular" : <string>,
    "tipo_sangre" : <string>,
    "email" : <string>
}
```
Consulta de paciente:
```
GET https://localhost:5000/pacientes
```
Este debe incluir el token de autorización, que indique que es un administrativo para asegurar que únicamente las personas con los permisos adecuados pueden ejecutar estas operaciones.