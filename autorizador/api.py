from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import create_access_token
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

with open("./private.key","r") as private_key:
    app.config["JWT_PRIVATE_KEY"] = private_key.read()

app.config["JWT_ALGORITHM"] = "RS256"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = False
jwt = JWTManager(app)
api = Api(app)
class AuthResource(Resource):
    def post(self):
        access_token = create_access_token(identity={
            "tipo_usuario" : request.json["tipo_usuario"],
            "id_usuario" : request.json["id_usuario"]
        })
        return jsonify(access_token=access_token)


api.add_resource(AuthResource, '/jwt')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', ssl_context='adhoc')