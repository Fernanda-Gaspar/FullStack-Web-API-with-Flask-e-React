from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_marshmallow import Marshmallow
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app, resource={
    r"/*":{
        "origins":"*"
    }
})
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://fernandagaspar:ZmVybmFuZGFn@localhost/fernandagaspar'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Pessoas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    rg = db.Column(db.Text())
    cpf = db.Column(db.Text)
    data_nascimento = db.Column(db.Date())
    data_admissao = db.Column(db.Date())
    date = db.Column(db.DateTime, default = datetime.datetime.now)


    def __init__(self, nome, rg, cpf, data_nascimento, data_admissao):
        self.nome = nome
        self.rg = rg
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.data_admissao = data_admissao

class PessoaSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nome', 'rg', 'cpf', 'data_nascimento', 'data_admissao', 'date')


pessoa_schema = PessoaSchema()
pessoas_schema = PessoaSchema(many=True)


@app.route('/get', methods = ['GET'])
def get_pessoas():
    all_pessoas = Pessoas.query.all()
    results = pessoas_schema.dump(all_pessoas)
    return jsonify(results)


@app.route('/get/<id>/', methods = ['GET'])
def post_details(id):
    pessoa = Pessoas.query.get(id)
    return pessoa_schema.jsonify(pessoa)


@app.route('/add', methods = ['POST'])
def add_pessoa():
    nome = request.json['nome']
    rg = request.json['rg']
    cpf = request.json['cpf']
    data_nascimento = request.json['data_nascimento']
    data_admissao = request.json['data_admissao']

    pessoas = Pessoas(nome, rg, cpf, data_nascimento, data_admissao)
    db.session.add(pessoas)
    db.session.commit()
    return pessoa_schema.jsonify(pessoas)



@app.route('/update/<id>/', methods = ['PUT'])
def update_pessoa(id):
    pessoa = Pessoas.query.get(id)

    nome = request.json['nome']
    rg = request.json['rg']
    cpf = request.json['cpf']
    data_nascimento = request.json['data_nascimento']
    data_admissao = request.json['data_admissao']
    
    pessoa.nome = nome
    pessoa.rg = rg
    pessoa.cpf = cpf
    pessoa.data_nascimento = data_nascimento
    pessoa.data_admissao = data_admissao

    db.session.commit()
    return pessoa_schema.jsonify(pessoa)



@app.route('/delete/<id>/', methods = ['DELETE'])
def pessoa_delete(id):
    pessoa = Pessoas.query.get(id)
    db.session.delete(pessoa)
    db.session.commit()

    return pessoa_schema.jsonify(pessoa)



if __name__ == "__main__":
    app.run()