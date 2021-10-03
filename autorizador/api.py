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

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo_usuario = db.Column(db.String(50))

class AuthResource(Resource):
    def post(self):
        setMockUp()
        user = User.query.get_or_404(request.json["id_usuario"])
        access_token = create_access_token(identity={
            "tipo_usuario" : user.tipo_usuario,
            "id_usuario" : user.id
        })
        return jsonify(access_token=access_token)

def setMockUp():
    for usuario in User.query.all():
        db.session.delete(usuario)
        
    db.session.commit()
    db.session.close()

    user1 = User(id=1, tipo_usuario='directivo')
    user2 = User(id=2, tipo_usuario='administrativo')
    db.session.add_all([user1, user2])
    db.session.commit()
    db.session.close()


api.add_resource(AuthResource, '/jwt')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', ssl_context='adhoc')