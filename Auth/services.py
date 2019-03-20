from Auth import app
from flask import jsonify
from flask import request
from flask import abort
from Database.mydbconn import db_execute_scalar
import base64
import string
import random
from Crypto.Cipher import DES3
import hashlib

@app.route('/user/<email>', methods=['GET'])
def user_get(email):
    results = db_execute_scalar("EXEC SPT_WEBV3_GET_USUARIO %s;", email)
    if results:
        return jsonify(results)
    else:
        return '', 204

@app.route('/user/validate', methods=['POST'])
def user_validate():
    results = db_execute_scalar("EXEC SPT_WEBV3_VALIDA_USUARIO %s, %s;", 
        (request.json['email'], encrypt_pass(request.json['password'])))
    if results:
        return jsonify(results)
    else:
        return '', 401


@app.route('/user/companies/<id_user>', methods=['GET'])
def user_companies(id_user):
    results = db_execute_scalar("EXEC SPT_WEBV3_LIST_EMPRESAS %s;", id_user)
    if results:
        return jsonify(results)
    else:
        return '', 204

@app.route('/user/password/<id_user>', methods=['POST'])
def user_password(id_user):
    if not request.json:
        abort(406)
    results = db_execute_scalar("EXEC SPT_WEBV3_SET_SENHA %s, %s;", (encrypt_pass(request.json['password']), id_user))
    if results:
        return jsonify(results)
    else:
        return '', 204

@app.route('/client/<cod_cliente>', methods=['GET'])
def user_list(cod_cliente):
    results = db_execute_scalar("EXEC SPT_WEBV3_LIST_USUARIOS %s;", cod_cliente)
    if results:
        return jsonify(results)
    else:
        return '', 204

@app.route('/user/<cod_cliente>', methods=['POST'])
def user_create(cod_cliente):
    if not request.json:
        abort(406)
    new_key = id_generator()
    crpt_key = encrypt_pass(new_key)
    results = db_execute_scalar("EXEC SPT_WEBV3_CREATE_USUARIO %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s;",
    (
        cod_cliente,
        request.json['user']['EMAIL'],
        request.json['user']['NOME'],
        crpt_key,
        request.json['user']['SETOR'],
        request.json['user']['_inclPedido'],
        request.json['user']['_visuCobranca'],
        request.json['user']['_inclNovoEndereco'],
        request.json['user']['_recEmailPedido'],
        request.json['user']['_recebEmailDanf'],
        request.json['user']['_recEmailembarque'],
        request.json['user']['_recebEmailBoleto'],
        request.json['user']['_recEmailatraso'],
        request.json['user']['_recEmailtresdias'],
        request.json['user']['_recEmailnegativar'],
        '',
        '')
    )
    if results:
        return jsonify(results)
    else:
        return '', 204

@app.route('/user/<cod_cliente>', methods=['PUT'])
def user_set(cod_cliente):
    if not request.json:
        abort(406)
    results = db_execute_scalar("EXEC SPT_WEBV3_SET_USUARIO %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s;",
    (
        cod_cliente,
        request.json['user']['EMAIL'],
        request.json['user']['NOME'],
        request.json['user']['SETOR'],
        request.json['user']['_inclPedido'],
        request.json['user']['_visuCobranca'],
        request.json['user']['_inclNovoEndereco'],
        request.json['user']['_recEmailPedido'],
        request.json['user']['_recebEmailDanf'],
        request.json['user']['_recEmailembarque'],
        request.json['user']['_recebEmailBoleto'],
        request.json['user']['_recEmailatraso'],
        request.json['user']['_recEmailtresdias'],
        request.json['user']['_recEmailnegativar'],
        '',
        '')
    )
    if results:
        return jsonify(results)
    else:
        return '', 204

@app.route('/user/<email>', methods=['DELETE'])
def user_del(email):
    results = db_execute_scalar("EXEC SPT_WEBV3_DEL_USUARIO %s;", email)
    data = {
        "status"    : True,
        "errorCod"  : "",
        "data"    : results
    }
    if results:
        return jsonify(results)
    else:
        return '', 204



def encrypt_pass(password):
    key = 'x2'
    key_byte = key.encode('utf-8')
    m = hashlib.md5()
    m.update(key_byte)
    pad_len = 8 - len(password) % 8
    padding = chr(pad_len) * pad_len
    password += padding

    cryptor = DES3.new(m.digest(), DES3.MODE_ECB)
    data = cryptor.encrypt(password)

    return base64.b64encode(data).decode('utf-8')

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
