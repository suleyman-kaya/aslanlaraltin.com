from flask import Flask, render_template, jsonify, request, redirect, json
from VeriYoneticisi import kar_listesi, VerCoskuyu
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
        # Check if the request contains JSON data
        if request.content_type == 'application/json':
            # Get the JSON data
            kar_listesi_verileri = request.get_json()
            print(kar_listesi_verileri)

            # Güncellenmiş kar listesini al
            update_kar_listesi(kar_listesi_verileri)

            # Yönetici sayfasını güncellenmiş kar listesiyle yeniden yükle
            return render_template('yonetici.html', kar_listesi=kar_listesi)
        else:
            # Return an error response if the Content-Type is not JSON
            error_response = {'error': 'Invalid Content-Type. Expected application/json.'}
            return jsonify(error_response), 400

    # GET isteği durumunda yönetici sayfasını göster
    return render_template('yonetici.html', kar_listesi=kar_listesi)

def update_kar_listesi(veriler):
    for doviz_altin, kar_oranlari in veriler.items():
        if doviz_altin in kar_listesi:
            kar_listesi[doviz_altin]["alisa_eklenecek_kar_orani"] = kar_oranlari["alisa_eklenecek_kar_orani"]
            kar_listesi[doviz_altin]["satisa_eklenecek_kar_orani"] = kar_oranlari["satisa_eklenecek_kar_orani"]
        else:
            kar_listesi[doviz_altin] = {
                "alisa_eklenecek_kar_orani": kar_oranlari["alisa_eklenecek_kar_orani"],
                "satisa_eklenecek_kar_orani": kar_oranlari["satisa_eklenecek_kar_orani"]
            }


if __name__ == '__main__':
    app.run()
    
