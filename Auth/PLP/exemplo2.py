from app import app
from flask import Flask

@app.route('/exemplo2')
def testando2():
    return 'Variavel global %s.' % 2
