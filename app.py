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


@app.route('/yonetici', methods=['GET', 'POST'])
def yonetici():
    if request.method == 'POST':
        with open('kar_listesi.json', 'r') as file:
            kar_listesi = json.load(file)
        
        if request.content_type == 'application/json':
            kar_listesi_verileri = request.get_json()

            update_kar_listesi(kar_listesi_verileri, kar_listesi)
            file.close()

            return render_template('yonetici.html', kar_listesi=kar_listesi)
        else:
            error_response = {'error': 'Invalid Content-Type. Expected application/json.'}
            return jsonify(error_response), 400

    with open('kar_listesi.json', 'r') as file:
        kar_listesi = json.load(file)
    file.close()

    return render_template('yonetici.html', kar_listesi=kar_listesi)


def update_kar_listesi(veriler, kar_listesi):
    for doviz_altin, kar_oranlari in veriler.items():
        if doviz_altin in kar_listesi:
            kar_listesi[doviz_altin]["alisa_eklenecek_kar_orani"] = kar_oranlari["alisa_eklenecek_kar_orani"]
            kar_listesi[doviz_altin]["satisa_eklenecek_kar_orani"] = kar_oranlari["satisa_eklenecek_kar_orani"]
        else:
            kar_listesi[doviz_altin] = {
                "alisa_eklenecek_kar_orani": kar_oranlari["alisa_eklenecek_kar_orani"],
                "satisa_eklenecek_kar_orani": kar_oranlari["satisa_eklenecek_kar_orani"]
            }

    with open('kar_listesi.json', 'w') as file:
        json.dump(kar_listesi, file)


if __name__ == '__main__':
    app.run()
