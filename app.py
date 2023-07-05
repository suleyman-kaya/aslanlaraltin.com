from flask import Flask, render_template, jsonify, request, redirect, json
from VeriYoneticisi import VerCoskuyu
app = Flask(__name__)


def load_kar_listesi():
    with open('kar_listesi.json', 'r') as file:
        kar_listesi = json.load(file)
    return kar_listesi



def save_kar_listesi(kar_listesi):
    with open('kar_listesi.json', 'w') as file:
        json.dump(kar_listesi, file, indent=4)



@app.route('/')
def index():
    dovizler, altinlar = VerCoskuyu()
    return render_template('index.html', dovizler=dovizler, altinlar=altinlar)



@app.route('/update')
def update():
    dovizler, altinlar = VerCoskuyu()
    return jsonify(dovizler=dovizler, altinlar=altinlar)



@app.route('/yonetici', methods=['POST'])
def update_kar_listesi():
    if request.method == 'POST':
        kar_listesi = request.json
        save_kar_listesi(kar_listesi)
        return jsonify(success=True)
    else:
        return jsonify(error='Invalid request method.'), 405



@app.route('/admin')
def admin_page():
    kar_listesi = load_kar_listesi()
    return render_template('admin.html', kar_listesi=kar_listesi)



if __name__ == '__main__':
    app.run()
    
