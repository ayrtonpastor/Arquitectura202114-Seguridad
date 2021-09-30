from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/usarios.db'
db = SQLAlchemy(app)
db.create_all()
ma = Marshmallow(app)
app.config["JWT_ALGORITHM"] = "RS256"
with open("./public.pem","r") as private_key:
    app.config["JWT_PUBLIC_KEY"] = private_key.read()
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = False

jwt = JWTManager(app)
api = Api(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)



class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        fields = ("id", "username")


user_schema = UserSchema()
users_schema = UserSchema(many=True)


class UserListResource(Resource):
    @jwt_required()
    def get(self):
        identity = get_jwt_identity()
        return 'Authorized'

    @jwt_required()
    def post(self):
        identity = get_jwt_identity()
        print(identity)

        return "Modificacion de paciente completada"


class UserResource(Resource):
    @jwt_required()
    def get(self, user_id):
        return 'Authorized'



api.add_resource(UserListResource, '/users')
api.add_resource(UserResource, '/users/<int:user_id>')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', ssl_context='adhoc')