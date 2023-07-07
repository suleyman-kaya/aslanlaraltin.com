from urllib import request, parse
import gzip, json



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
        with open('kar_listesi.json', 'r') as file:
            kar_listesi = json.load(file)


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
        
        # Şimdi döviz listesine kârı ekliyoruz.
        for eleman in kar_listesi.keys():
            result[eleman]["satis"] = round(result[eleman]["satis"] + kar_listesi[eleman]["satisa_eklenecek_kar_orani"],3)
            result[eleman]["alis"] = round(result[eleman]["alis"] + kar_listesi[eleman]["alisa_eklenecek_kar_orani"],3)

        # Şimdi ise has altını referans alarak diğer altınların değerini çarpıp belirliyoruz
        has_alis = result["ALTIN"]["alis"]
        has_satis = result["ALTIN"]["satis"]
        # Alışlar
        result["AYAR14"]["alis"] = int(has_alis * 0.55)
        result["AYAR22"]["alis"] = int(has_alis * 0.912)
        result["KULCEALTIN"]["alis"] = int(has_alis * 0.995)
        result["TEK_YENI"]["alis"] = int(has_alis * 6.40)
        result["TEK_ESKI"]["alis"] = int(has_alis * 6.40)
        result["ATA_YENI"]["alis"] = int(has_alis * 6.42)
        result["ATA5_YENI"]["alis"] = int(has_alis * 32.8)
        result["CEYREK_ESKI"]["alis"] = int(has_alis * 1.60)
        result["CEYREK_YENI"]["alis"] = int(has_alis * 1.60)
        result["YARIM_ESKI"]["alis"] = int(has_alis * 3.20)
        result["YARIM_YENI"]["alis"] = int(has_alis * 3.20)
        result["GREMESE_ESKI"]["alis"] = int(has_alis * 16)
        result["GREMESE_YENI"]["alis"] = int(has_alis * 16)
        # Satışlar
        result["AYAR14"]["satis"] = int(has_satis * 0.80)
        result["AYAR22"]["satis"] = int(has_satis * 0.960)
        result["KULCEALTIN"]["satis"] = int(has_satis * 1.005)
        result["TEK_YENI"]["satis"] = int(has_satis * 6.68)
        result["TEK_ESKI"]["satis"] = int(has_satis * 6.56)
        result["ATA_YENI"]["satis"] = int(has_satis * 7)
        result["ATA5_YENI"]["satis"] = int(has_satis * 34.7)
        result["CEYREK_ESKI"]["satis"] = int(has_satis * 1.64)
        result["CEYREK_YENI"]["satis"] = int(has_satis * 1.67)
        result["YARIM_ESKI"]["satis"] = int(has_satis * 3.28)
        result["YARIM_YENI"]["satis"] = int(has_satis * 3.34)
        result["GREMESE_ESKI"]["satis"] = int(has_satis * 16.40)
        result["GREMESE_YENI"]["satis"] = int(has_satis * 16.70)
        

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
        
        file.close()

        return (doviz_listesi, altin_listesi)
    
    else:
        return (doviz_listesi, altin_listesi)