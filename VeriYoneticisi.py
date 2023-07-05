from urllib import request, parse
import gzip, json


def VerileriCek()->dict:
    url = 'https://www.haremaltin.com/dashboard/ajax/doviz'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/112.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://www.haremaltin.com',
        'Connection': 'keep-alive',
        'Referer': 'https://www.haremaltin.com/canli-piyasalar/',
        'Cookie': 'PHPSESSID=1q4084qbl7qd02biui6sgak6rl; SERVERID=003',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'DNT': '1',
        'Sec-GPC': '1'
    }
    data = {
        'dil_kodu': 'tr'
    }

    encoded_data = parse.urlencode(data).encode()

    req = request.Request(url, headers=headers, data=encoded_data)
    response = request.urlopen(req)

    if response.status == 200:
        if response.headers.get('Content-Encoding') == 'gzip':
            compressed_data = response.read()
            data = gzip.decompress(compressed_data)
        else:
            data = response.read()

        content_type = response.headers.get('Content-Type')
        encoding = response.headers.get_content_charset() or 'utf-8'

        result = json.loads(data.decode(encoding))

        result = result["data"]

        # Alış ve satış değerlerini float'a dönüştürme
        for deger in result:
            result[deger]["alis"] = float(result[deger]["alis"])
            result[deger]["satis"] = float(result[deger]["satis"])
    
    return result




def Verileri_Gruplara_Ayir(veri_kumesi:dict) -> set:
    """
    Onceki kullanılan kodlar:
    tum_doviz_ve_altinlar_listesi = list(veri_kumesi.keys())
    filtreli_doviz_listesi = [eleman for eleman in tum_doviz_ve_altinlar_listesi if eleman.endswith("TRY")]
    filtreli_doviz_listesi = [eleman for eleman in filtreli_doviz_listesi if "RUB" not in eleman and "DKK" not in eleman and "BGN" not in eleman and "CNY" not in eleman and "JPY" not in eleman and "GUMUS" not in eleman]
    """
    filtreli_doviz_listesi = ['USDTRY', 'EURTRY', 'GBPTRY', 'CHFTRY', 'SARTRY', 'AUDTRY', 'CADTRY', 'GUMUSTRY', 'ATA5_YENI', 'ATA_YENI']

    """
    Onceki kullanilan kodlar:
    filtreli_altin_listesi = [eleman for eleman in tum_doviz_ve_altinlar_listesi if eleman.find("USD") == -1 and eleman.find("ONS") == -1 and eleman.find("XAU") == -1 and eleman.find("EUR") == -1 and eleman.find("TRY") == -1]
    """
    filtreli_altin_listesi = ['ALTIN', 'AYAR14', 'AYAR22', 'KULCEALTIN', 'CEYREK_YENI', 'CEYREK_ESKI', 'YARIM_YENI', 'YARIM_ESKI', 'TEK_YENI', 'TEK_ESKI', 'GREMESE_YENI', 'GREMESE_ESKI']

    
    doviz_listesi, altin_listesi = {}, {}

    for eleman in filtreli_doviz_listesi:
        doviz_listesi[eleman] = veri_kumesi[eleman]

    for eleman in filtreli_altin_listesi:
        altin_listesi[eleman] = veri_kumesi[eleman]

    return (doviz_listesi, altin_listesi)




global kar_listesi
kar_listesi = {"USDTRY":{"alisa_eklenecek_kar_orani":-0.15,"satisa_eklenecek_kar_orani":0.4},"EURTRY":{"alisa_eklenecek_kar_orani":-0.3,"satisa_eklenecek_kar_orani":0.15},"GBPTRY":{"alisa_eklenecek_kar_orani":-0.15,"satisa_eklenecek_kar_orani":0.2},"CHFTRY":{"alisa_eklenecek_kar_orani":-0.1,"satisa_eklenecek_kar_orani":0.2},"AUDTRY":{"alisa_eklenecek_kar_orani":-0.1,"satisa_eklenecek_kar_orani":0.1},"CADTRY":{"alisa_eklenecek_kar_orani":-0.1,"satisa_eklenecek_kar_orani":0.1},"SARTRY":{"alisa_eklenecek_kar_orani":-0.1,"satisa_eklenecek_kar_orani":0.1},"GUMUSTRY":{"alisa_eklenecek_kar_orani":-0.1,"satisa_eklenecek_kar_orani":0.2},"ALTIN":{"alisa_eklenecek_kar_orani":0.5,"satisa_eklenecek_kar_orani":-0.5},"AYAR14":{"alisa_eklenecek_kar_orani":-10,"satisa_eklenecek_kar_orani":0},"AYAR22":{"alisa_eklenecek_kar_orani":2,"satisa_eklenecek_kar_orani":-5},"KULCEALTIN":{"alisa_eklenecek_kar_orani":1,"satisa_eklenecek_kar_orani":-3},"CEYREK_YENI":{"alisa_eklenecek_kar_orani":20,"satisa_eklenecek_kar_orani":-20},"CEYREK_ESKI":{"alisa_eklenecek_kar_orani":10,"satisa_eklenecek_kar_orani":-10},"YARIM_YENI":{"alisa_eklenecek_kar_orani":10,"satisa_eklenecek_kar_orani":-20},"YARIM_ESKI":{"alisa_eklenecek_kar_orani":10,"satisa_eklenecek_kar_orani":-20},"TEK_YENI":{"alisa_eklenecek_kar_orani":30,"satisa_eklenecek_kar_orani":-40},"TEK_ESKI":{"alisa_eklenecek_kar_orani":30,"satisa_eklenecek_kar_orani":-40},"ATA_YENI":{"alisa_eklenecek_kar_orani":20,"satisa_eklenecek_kar_orani":-30},"ATA5_YENI":{"alisa_eklenecek_kar_orani":90,"satisa_eklenecek_kar_orani":-100},"GREMESE_YENI":{"alisa_eklenecek_kar_orani":50,"satisa_eklenecek_kar_orani":-70},"GREMESE_ESKI":{"alisa_eklenecek_kar_orani":50,"satisa_eklenecek_kar_orani":-70}}
filtreli_doviz_listesi = ['USDTRY', 'EURTRY', 'GBPTRY', 'CHFTRY', 'SARTRY', 'AUDTRY', 'CADTRY', 'GUMUSTRY', 'ATA5_YENI', 'ATA_YENI']
filtreli_altin_listesi = ['ALTIN', 'AYAR14', 'AYAR22', 'KULCEALTIN', 'CEYREK_ESKI', 'CEYREK_YENI', 'YARIM_ESKI', 'YARIM_YENI', 'TEK_ESKI','TEK_YENI', 'GREMESE_ESKI', 'GREMESE_YENI']
kar_listesi = {k: v for k, v in kar_listesi.items() if k in filtreli_doviz_listesi + filtreli_altin_listesi}




def TabloyaKarEkle(orijinal_veri_tablosu:dict, kar_listesi:dict) -> dict:
    orijinal_veri_tablosu_kopya = orijinal_veri_tablosu.copy()
    for eleman in kar_listesi.keys():
        orijinal_veri_tablosu_kopya[eleman]["satis"] = round(orijinal_veri_tablosu_kopya[eleman]["satis"] + kar_listesi[eleman]["satisa_eklenecek_kar_orani"],3)
        orijinal_veri_tablosu_kopya[eleman]["alis"] = round(orijinal_veri_tablosu_kopya[eleman]["alis"] + kar_listesi[eleman]["alisa_eklenecek_kar_orani"],3)

    return orijinal_veri_tablosu_kopya




def IsimleriDegistir(veri_tablosu:dict)-> dict:
    veri_tablosu_kopya = veri_tablosu.copy()
    veri_tablosu_kopya["ALTIN"]["code"] = "HAS"
    veri_tablosu_kopya["AYAR14"]["code"] = "14 AYAR"
    veri_tablosu_kopya["AYAR22"]["code"] = "22 AYAR"
    veri_tablosu_kopya["KULCEALTIN"]["code"] = "GRAM ALTIN"
    veri_tablosu_kopya["TEK_YENI"]["code"] = "YENİ TAM"
    veri_tablosu_kopya["TEK_ESKI"]["code"] = "ESKİ TAM"
    veri_tablosu_kopya["ATA_YENI"]["code"] = "REŞAT"
    veri_tablosu_kopya["ATA5_YENI"]["code"] = "36 REŞAT"
    veri_tablosu_kopya["CEYREK_ESKI"]["code"] = "ESKİ ÇEYREK"
    veri_tablosu_kopya["CEYREK_YENI"]["code"] = "YENİ ÇEYREK"
    veri_tablosu_kopya["YARIM_ESKI"]["code"] = "ESKİ YARIM"
    veri_tablosu_kopya["YARIM_YENI"]["code"] = "YENİ YARIM"
    veri_tablosu_kopya["GREMESE_ESKI"]["code"] = "ESKİ GREMESE"
    veri_tablosu_kopya["GREMESE_YENI"]["code"] = "YENİ GREMESE"
    veri_tablosu_kopya["GUMUSTRY"]["code"] = "GÜMÜŞ"

    
    return veri_tablosu_kopya




def VerCoskuyu():
    veri_kumesi = VerileriCek()
    isim_guncellenmis_tablo = IsimleriDegistir(veri_kumesi)
    kar_eklenmis_veri = TabloyaKarEkle(isim_guncellenmis_tablo, kar_listesi)
    dovizler, altinlar = Verileri_Gruplara_Ayir(kar_eklenmis_veri)
    return (dovizler, altinlar)