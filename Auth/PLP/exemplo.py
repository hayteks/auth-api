from app import app
from flask import Flask

@app.route('/exemplo')
def testando():
    return 'Incrementando: %s.' % 1
