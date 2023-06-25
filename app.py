from flask import Flask, render_template, jsonify
from VeriYoneticisi import VerileriCek, Verileri_Gruplara_Ayir, IstenenVeriyeKarEkle

app = Flask(__name__)

@app.route('/')
def index():
    veri_kumesi = VerileriCek()
    kar_eklenmis_veri = IstenenVeriyeKarEkle(veri_kumesi, "USDTRY", "satis", 25.0)
    dovizler, altinlar = Verileri_Gruplara_Ayir(kar_eklenmis_veri)
    return render_template('index.html', dovizler=dovizler, altinlar=altinlar)

@app.route('/update')
def update():
    veri_kumesi = VerileriCek()
    kar_eklenmis_veri = IstenenVeriyeKarEkle(veri_kumesi, "USDTRY", "satis", 25.0)
    dovizler, altinlar = Verileri_Gruplara_Ayir(kar_eklenmis_veri)
    return jsonify(dovizler=dovizler, altinlar=altinlar)

if __name__ == '__main__':
    app.run()
