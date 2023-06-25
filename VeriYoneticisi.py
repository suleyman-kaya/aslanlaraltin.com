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
        result["alis"] = float(result["alis"])
        result["satis"] = float(result["satis"])
    
    return result




def Verileri_Gruplara_Ayir(veri_kumesi:dict) -> set:
    #tum_doviz_ve_altinlar_listesi = list(veri_kumesi.keys())
    #filtreli_doviz_listesi = [eleman for eleman in tum_doviz_ve_altinlar_listesi if eleman.endswith("TRY")]
    #filtreli_doviz_listesi = [eleman for eleman in filtreli_doviz_listesi if "RUB" not in eleman and "DKK" not in eleman and "BGN" not in eleman and "CNY" not in eleman and "JPY" not in eleman and "GUMUS" not in eleman]
    filtreli_doviz_listesi = ['USDTRY', 'EURTRY', 'GBPTRY', 'SEKTRY', 'NOKTRY', 'CHFTRY', 'AUDTRY', 'JODTRY', 'CADTRY', 'OMRTRY', 'SARTRY', 'AEDTRY', 'QARTRY', 'KWDTRY', 'ILSTRY', 'MADTRY']

    #filtreli_altin_listesi = [eleman for eleman in tum_doviz_ve_altinlar_listesi if eleman.find("USD") == -1 and eleman.find("ONS") == -1 and eleman.find("XAU") == -1 and eleman.find("EUR") == -1 and eleman.find("TRY") == -1]
    filtreli_altin_listesi = ['ALTIN', 'AYAR14', 'AYAR22', 'KULCEALTIN', 'CEYREK_YENI', 'CEYREK_ESKI', 'YARIM_YENI', 'YARIM_ESKI', 'TEK_YENI', 'TEK_ESKI', 'ATA_YENI', 'ATA_ESKI', 'ATA5_YENI', 'ATA5_ESKI', 'GREMESE_YENI', 'GREMESE_ESKI']
    
    doviz_listesi, altin_listesi = {}, {}

    for eleman in filtreli_doviz_listesi:
        doviz_listesi[eleman] = veri_kumesi[eleman]

    for eleman in filtreli_altin_listesi:
        altin_listesi[eleman] = veri_kumesi[eleman]

    return (doviz_listesi, altin_listesi)
