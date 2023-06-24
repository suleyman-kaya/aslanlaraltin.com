from flask import Flask, render_template, jsonify
from VeriYoneticisi import VerileriCek, Verileri_Gruplara_Ayir

app = Flask(__name__)

@app.route('/')
def index():
    veri_kumesi = VerileriCek()
    dovizler, altinlar = Verileri_Gruplara_Ayir(veri_kumesi)
    return render_template('index.html', dovizler=dovizler, altinlar=altinlar)

@app.route('/update')
def update():
    veri_kumesi = VerileriCek()
    dovizler, altinlar = Verileri_Gruplara_Ayir(veri_kumesi)
    return jsonify(dovizler=dovizler, altinlar=altinlar)

if __name__ == '__main__':
    app.run()
