from urllib import request, parse
import gzip, json

global kar_listesi
kar_listesi = {"USDTRY":{"alisa_eklenecek_kar_orani":-0.15,"satisa_eklenecek_kar_orani":0.4},"EURTRY":{"alisa_eklenecek_kar_orani":-0.3,"satisa_eklenecek_kar_orani":0.15},"GBPTRY":{"alisa_eklenecek_kar_orani":-0.15,"satisa_eklenecek_kar_orani":0.2},"CHFTRY":{"alisa_eklenecek_kar_orani":-0.1,"satisa_eklenecek_kar_orani":0.2},"AUDTRY":{"alisa_eklenecek_kar_orani":-0.1,"satisa_eklenecek_kar_orani":0.1},"CADTRY":{"alisa_eklenecek_kar_orani":-0.1,"satisa_eklenecek_kar_orani":0.1},"SARTRY":{"alisa_eklenecek_kar_orani":-0.1,"satisa_eklenecek_kar_orani":0.1},"GUMUSTRY":{"alisa_eklenecek_kar_orani":-0.1,"satisa_eklenecek_kar_orani":0.2},"ALTIN":{"alisa_eklenecek_kar_orani":0.5,"satisa_eklenecek_kar_orani":-0.5},"AYAR14":{"alisa_eklenecek_kar_orani":-10,"satisa_eklenecek_kar_orani":0},"AYAR22":{"alisa_eklenecek_kar_orani":2,"satisa_eklenecek_kar_orani":-5},"KULCEALTIN":{"alisa_eklenecek_kar_orani":1,"satisa_eklenecek_kar_orani":-3},"CEYREK_YENI":{"alisa_eklenecek_kar_orani":20,"satisa_eklenecek_kar_orani":-20},"CEYREK_ESKI":{"alisa_eklenecek_kar_orani":10,"satisa_eklenecek_kar_orani":-10},"YARIM_YENI":{"alisa_eklenecek_kar_orani":10,"satisa_eklenecek_kar_orani":-20},"YARIM_ESKI":{"alisa_eklenecek_kar_orani":10,"satisa_eklenecek_kar_orani":-20},"TEK_YENI":{"alisa_eklenecek_kar_orani":30,"satisa_eklenecek_kar_orani":-40},"TEK_ESKI":{"alisa_eklenecek_kar_orani":30,"satisa_eklenecek_kar_orani":-40},"ATA_YENI":{"alisa_eklenecek_kar_orani":20,"satisa_eklenecek_kar_orani":-30},"ATA5_YENI":{"alisa_eklenecek_kar_orani":90,"satisa_eklenecek_kar_orani":-100},"GREMESE_YENI":{"alisa_eklenecek_kar_orani":50,"satisa_eklenecek_kar_orani":-70},"GREMESE_ESKI":{"alisa_eklenecek_kar_orani":50,"satisa_eklenecek_kar_orani":-70}}


def VerCoskuyu()->dict:
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

        # Her yerden ulaşmak istirem
        global result

        result = json.loads(data.decode(encoding))

        result = result["data"]

        keys_to_keep = ['USDTRY', 'EURTRY', 'GBPTRY', 'CHFTRY', 'SARTRY', 'AUDTRY', 'CADTRY', 'GUMUSTRY', 'ATA5_YENI', 'ATA_YENI', 'ALTIN', 'AYAR14', 'AYAR22', 'KULCEALTIN', 'CEYREK_YENI', 'CEYREK_ESKI', 'YARIM_YENI', 'YARIM_ESKI', 'TEK_YENI', 'TEK_ESKI', 'GREMESE_YENI', 'GREMESE_ESKI']
        filtered_result = {key: value for key, value in result.items() if key in keys_to_keep}
        result = filtered_result

        # Alış ve satış değerlerini float'a dönüştürme
        for deger in result:
            result[deger]["alis"] = float(result[deger]["alis"])
            result[deger]["satis"] = float(result[deger]["satis"])
        
        # Şimdi kârı ekliyoruz.
        for eleman in kar_listesi.keys():
            result[eleman]["satis"] = round(result[eleman]["satis"] + kar_listesi[eleman]["satisa_eklenecek_kar_orani"],3)
            result[eleman]["alis"] = round(result[eleman]["alis"] + kar_listesi[eleman]["alisa_eklenecek_kar_orani"],3)

        # Şimdi ise çeşitli birimlerin kodlarını değiştiriyoruz.
        result["ALTIN"]["code"] = "HAS"
        result["AYAR14"]["code"] = "14 AYAR"
        result["AYAR22"]["code"] = "22 AYAR"
        result["KULCEALTIN"]["code"] = "GRAM ALTIN"
        result["TEK_YENI"]["code"] = "YENİ TAM"
        result["TEK_ESKI"]["code"] = "ESKİ TAM"
        result["ATA_YENI"]["code"] = "REŞAT"
        result["ATA5_YENI"]["code"] = "36 REŞAT"
        result["CEYREK_ESKI"]["code"] = "ESKİ ÇEYREK"
        result["CEYREK_YENI"]["code"] = "YENİ ÇEYREK"
        result["YARIM_ESKI"]["code"] = "ESKİ YARIM"
        result["YARIM_YENI"]["code"] = "YENİ YARIM"
        result["GREMESE_ESKI"]["code"] = "ESKİ GREMESE"
        result["GREMESE_YENI"]["code"] = "YENİ GREMESE"
        result["GUMUSTRY"]["code"] = "GÜMÜŞ"

        # Şimdi ise döviz ve altınları ayırıp fonksiyonun çıktısı olarak veriyoruz
        filtreli_doviz_listesi = ['USDTRY', 'EURTRY', 'GBPTRY', 'CHFTRY', 'SARTRY', 'AUDTRY', 'CADTRY', 'GUMUSTRY', 'ATA5_YENI', 'ATA_YENI']
        filtreli_altin_listesi = ['ALTIN', 'AYAR14', 'AYAR22', 'KULCEALTIN', 'CEYREK_YENI', 'CEYREK_ESKI', 'YARIM_YENI', 'YARIM_ESKI', 'TEK_YENI', 'TEK_ESKI', 'GREMESE_YENI', 'GREMESE_ESKI']
        
        # Her yerden ulaşmak istirem
        global doviz_listesi
        global altin_listesi

        doviz_listesi, altin_listesi = {}, {}

        for eleman in filtreli_doviz_listesi:
            doviz_listesi[eleman] = result[eleman]

        for eleman in filtreli_altin_listesi:
            altin_listesi[eleman] = result[eleman]

        return (doviz_listesi, altin_listesi)
    
    else:
        return (doviz_listesi, altin_listesi)