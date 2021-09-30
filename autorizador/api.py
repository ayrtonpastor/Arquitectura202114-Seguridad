from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import create_access_token
from flask_jwt_extended import JWTManager

app = Flask(__name__)

with open("./private.key","r") as private_key:
    app.config["JWT_PRIVATE_KEY"] = private_key.read()

app.config["JWT_ALGORITHM"] = "RS256"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = False
jwt = JWTManager(app)
api = Api(app)

class AuthResource(Resource):
    def post(self):
        #obtener Id_usuario, tipo_usuario
        access_token = create_access_token(identity={
            "tipo_usuario" : "medico",
            "id_usuario" : 321
        })
        return jsonify(access_token=access_token)


api.add_resource(AuthResource, '/jwt')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', ssl_context='adhoc')