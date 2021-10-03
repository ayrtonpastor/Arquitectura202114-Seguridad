from os import error
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/pacientes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)
app.config["JWT_ALGORITHM"] = "RS256"
with open("./public.pem","r") as private_key:
    app.config["JWT_PUBLIC_KEY"] = private_key.read()
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = False

jwt = JWTManager(app)
api = Api(app)


class Paciente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(50))
    apellidos = db.Column(db.String(50))
    celular = db.Column(db.String(50))
    tipo_sangre = db.Column(db.String(50))
    email = db.Column(db.String(50))


class PacienteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        fields = ("id", "nombres", "apellidos", "celular", "tipo_sangre", "email")


paciente_schema = PacienteSchema()
pacientes_schema = PacienteSchema(many=True)

class PacienteListResource(Resource):
    @jwt_required()
    def get(self):
        identity = get_jwt_identity()
        permiso = identity.get("tipo_usuario")
        if permiso == 'administrativo':
            pacientes =  Paciente.query.all()
            return pacientes_schema.dump(pacientes)
        else:
            return 'Permisos Denegados',404

    @jwt_required()
    def post(self):
        identity = get_jwt_identity()
        permiso = identity.get("tipo_usuario")
        if permiso == 'administrativo':
            nuevo_paciente = Paciente(nombres=request.json["nombres"], apellidos=request.json["apellidos"], 
                                    celular=request.json["celular"], tipo_sangre=request.json["tipo_sangre"], email=request.json["email"])
            db.session.add(nuevo_paciente)
            db.session.commit()
            return jsonify(paciente_schema.dump(nuevo_paciente))
        else:
            return 'Permisos Denegados',404

class PacienteResource(Resource):
    @jwt_required()
    def get(self, paciente_id):
        identity = get_jwt_identity()
        permiso = identity.get("tipo_usuario")
        if permiso == 'administrativo':
            paciente = Paciente.query.get_or_404(paciente_id)
            return paciente_schema.dump(paciente)
        else:
            return 'Permisos Denegados',404


api.add_resource(PacienteListResource, '/pacientes')
api.add_resource(PacienteResource, '/pacientes/<int:paciente_id>')


if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    app.run(debug=True, host='0.0.0.0', ssl_context='adhoc')