from flask import Flask, render_template, jsonify, request, redirect, json
from VeriYoneticisi import VerCoskuyu
app = Flask(__name__)


@app.route('/')
def index():
    dovizler, altinlar = VerCoskuyu()
    return render_template('index.html', dovizler=dovizler, altinlar=altinlar)



@app.route('/update')
def update():
    dovizler, altinlar = VerCoskuyu()
    return jsonify(dovizler=dovizler, altinlar=altinlar)


if __name__ == '__main__':
    app.run()