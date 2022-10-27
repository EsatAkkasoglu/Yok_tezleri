from requests_html import HTML
import requests
from bs4 import BeautifulSoup
import csv
# URL bağlantısı çekmek istediğim linke özel olmadığı için html kodlarını indirdim.
# str formatında olan bu dizinler html kodu analiz eder gibi davranabilirim.
with open('C:/Users/lenovo/Desktop/source_code.html') as html_file:

    # sayfayı indirmek değil, önemli olan kaynak kodunu yazılı formatta almak
    # kaynak kodunu kopyala yapıştır yazınız
    # bahsi geçen html dosyası sonuçları aldıktan sonra url kaynağından alınmış kodları içermektedir.

    source = html_file.read()
    html1 = HTML(html=source)

# burda verdiğim değişken adları o ana verilmiş değişkenlerdir.
# özel bir anlam ifade etmemektedir
    match = html1.find("div.shell", first=True)

    kaynakKodu = match.find("script", first=True).html
"""
HTML kodu üzerinde istediğim alan javascript 
formatında kayıtlı olduğu için böyle bir yol izledim
"""
# her tez detayının önenünde 'tezDetay' yazdığını kodlar arasından gördüm.
# uzunluklarının aynı olması işimi inanılmaz kolaylaştırdı.
# Yök Tez sitesinde her kodun detay kısmında ki 'ID' ve 'NO' aynı uzunluktadır.
# print(bir.split("tezDetay")[1][2:24])
# print(bir.split("tezDetay")[1][27:49])

i = 1
for i in range(1, 173):
    link_id = kaynakKodu.split("tezDetay")[i][2:24]
    link_no = kaynakKodu.split("tezDetay")[i][27:49]
# Range i'yi kaynak koddaki maximum sayım kadar kullanınız.
# döngüde benim sonucumda 172 tane sonuc olduğu için max range 173 kullanıldı.

#Her tez özeti için özel url vardır.
# örnek link
# https://tez.yok.gov.tr/UlusalTezMerkezi/tezDetay.jsp?id="TBzuU3MqYhqJ9XHc-esfgA"&no="TBzuU3MqYhqJ9XHc-esfgA"

    url = 'https://tez.yok.gov.tr/UlusalTezMerkezi/tezDetay.jsp?id="' +link_id+'"&no="'+link_no
# URL işlemini otomatize ettikten sonra bu aşamada oluşturduğumuz url'lerden html kodlarını alma işlemi kalıyor.

    R = requests.get(url)
    doc = BeautifulSoup(R.text, "html.parser")
# HTML kodlarını düzenli bir biçimde görmek için 'prettify' komutunu kullanıyoruz.
# print(doc.prettify())
# yök tez atlas sonuc sayfasından aldığınız tüm tez sonuçlarını için bu adımları uygulabilirsiniz

    tag = doc.find_all("td")
    # print(tag[])
    tezNo = tag[4].text.strip()
    print(tezNo)
    tezKunye = str(tag[6])
    tezDurumu = str(tag[7])
    tezOzetTR = (tag[9].text.strip())
    tezOzetING = (tag[11].text.strip())

    tezAdıTR = (tezKunye.split("<br/>")[0].split("/")[1].strip())

    tezAdıING = (tezKunye.split("<br/>")
                 [0].split("/")[0].split('<td valign="top">')[1].strip())
#!!ÖNEMLİ NOT:
# tezAdıING, Türkçe tez adları içermektedir.Bu sisteme yüklenme şekliyle ilgilidir.
# tezAdıING ve tezAdıTR değişkenleri çoğunluğa göre seçilmişitir. Düzeltmeyi yapma yolunu bulmadım.
# seçilen dillerin haricinde diller içerebilir.
    tezYazarAdı = (tezKunye.split("<br/>")[1].split(":")[1])
    tezDanısmanAdı = (tezKunye.split("<br/>")[2].split(":")[1].strip())+";"
    tezDanismanAdi1 = (tezDanısmanAdı.split(";")[0])
    tezDanismanAdi2 = (tezDanısmanAdı.split(";")[1])
    tezYerBilgisi = (tezKunye.split("<br/>")[3].split(":")[1].strip())
    tezLisansDerecesi = (tezDurumu.split("<br/>")[1].strip())
    tezYayimTarihi = (tezDurumu.split("<br/>")[2].strip())
    tezTarihi = (tezDurumu.split("<br/>")[3].strip())
    a = 0
    tezKonusuTR=[]
    tezKonusuING=[]
    for a in range(0, len(tezKunye.split("<br/>")[4].split(";"))):
        tezKonusuTR.reverse()
        tezKonusuTR=[tezKonusuTR]
        
        tezKonusuTR.append(tezKunye.split("<br/>")
                        [4].split(";")[a].split("=")[0].strip())
        tezKonusuING=[tezKonusuING]
        tezKonusuING.append(tezKunye.split("<br/>")
                        [4].split(";")[a].split("=")[1].strip())
        
        a += 1
        
        print(tezKonusuTR)
        print(tezKonusuING)
        
        
        
    with open("tutorial.csv", "a", newline="") as csvFile:
        fieldNames = ["No", "Adı_TR", "Adı_ING", "Yazar_Adı", "1.Danisman_Adı", "2.Danisman_Adı",
                      "Yer_Bilgisi", "Lisans_Derecesi", "Yayim_Tarihi",
                      "Konusu_TR", "Konusu_ING", "Ozeti_TR", "Ozeti_ING", "Tez_tarihi"]
        thewriter = csv.DictWriter(csvFile, fieldnames=fieldNames)
        thewriter.writeheader()
        thewriter.writerow({"No": [tezNo], "Adı_TR": [tezAdıTR],
                            "Adı_ING": [tezAdıING], "Yazar_Adı": [tezYazarAdı],
                            "1.Danisman_Adı": [tezDanismanAdi1], "2.Danisman_Adı": [tezDanismanAdi2],
                            "Yer_Bilgisi": [tezYerBilgisi], "Lisans_Derecesi": [tezLisansDerecesi],
                            "Yayim_Tarihi": [tezYayimTarihi],
                            "Konusu_TR": [tezKonusuTR], "Konusu_ING": [tezKonusuING],
                            "Ozeti_TR": [tezOzetTR], "Ozeti_ING": [tezOzetING], "Tez_tarihi": [tezTarihi]}) 
    # print(tezOzetING)
    tezKonusuTR=[]
    tezKonusuING=[]
    """print(tezNo,tezAdıTR,tezAdıING,tezYazarAdı,tezDanısmanAdı,
          tezYerBilgisi,tezLisansDerecesi,
          tezKonusuTR,tezKonusuING,tezOzetTR,tezOzetING)"""
# hepsine tekrardan bakmakta fayda vardır.üsteki print komutunu test için aktif hale getiriniz.

# sırada bir sözlük yapmak var. headerları olan bir list için aşşağıdaki adımlar izlenmelidir.

    

# CSV dosyasına kayıt ederken header tanıtma işlemini gerçekleştiremedim.
# excel dosyasından düzenleme işlemi yapacağım.

    print(tezTarihi)
    i += 1
