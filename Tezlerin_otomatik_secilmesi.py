from requests_html import HTML
import requests 
from bs4 import BeautifulSoup
import csv
import pandas as pd 

#URL bağlantısı çekmek istediğim linke özel olmadığı için html kodlarını indirdim.
#str formatında olan bu dizinler html kodu analiz eder gibi davranabilirim. 
with open('C:/Users/lenovo/Desktop/source_code.html') as html_file:

#sayfayı indirmek değil, önemli olan kaynak kodunu yazılı formatta almak
#kaynak kodunu kopyala yapıştır yazınız
#bahsi geçen html dosyası sonuçları aldıktan sonra url kaynağından alınmış kodları içermektedir.

    source = html_file.read()
    html1 = HTML(html=source)
    
#burda verdiğim değişken adları o ana verilmiş değişkenlerdir.
#özel bir anlam ifade etmemektedir
    match = html1.find("div.shell",first= True)
    
    kaynakKodu= match.find("script",first=True).html
"""
HTML kodu üzerinde istediğim alan javascript 
formatında kayıtlı olduğu için böyle bir yol izledim
"""
#her tez detayının önenünde 'tezDetay' yazdığını kodlar arasından gördüm.
#uzunluklarının aynı olması işimi inanılmaz kolaylaştırdı.
#Yök Tez sitesinde her kodun detay kısmında ki 'ID' ve 'NO' aynı uzunluktadır.
#print(bir.split("tezDetay")[1][2:24])
#print(bir.split("tezDetay")[1][27:49])

i=1
for i in range(1,173):
    link_id=kaynakKodu.split("tezDetay")[i][2:24] 
    link_no=kaynakKodu.split("tezDetay")[i][27:49] 
#döngüde benim sonucumda 172 tane sonuc olduğu için max range 173 kullanıldı.

#örnek link
#https://tez.yok.gov.tr/UlusalTezMerkezi/tezDetay.jsp?id="TBzuU3MqYhqJ9XHc-esfgA"&no="TBzuU3MqYhqJ9XHc-esfgA"
  
    url='https://tez.yok.gov.tr/UlusalTezMerkezi/tezDetay.jsp?id="'+link_id+'"&no="'+link_no
#Verileriçekm işlemini otomatize ettikten sonra bu aşamada oluşturduğumuz url'ler alma işlemi kalıyor.
    
    R=requests.get(url)
    doc= BeautifulSoup(R.text,"html.parser")
#HTML kodlarını düzenli bir biçimde görmek için 'prettify' komutunu kullanıyoruz.
#print(doc.prettify())
#yök tez atlas sonuc sayfasından aldığınız tüm tez sonuçlarını için bu adımları uygulabilirsiniz

    tag=doc.find_all("td")
    #print(tag[])
    tezNo = tag[4].text
    tezKunye= str(tag[6])
    tezDurumu= str(tag[7])
    tezOzetTR=(tag[9].text)
    tezOzetING=(tag[11].text)
    
    tezAdıTR=(tezKunye.split("<br/>")[0].split("/")[1])

    tezAdıING=(tezKunye.split("<br/>")[0].split("/")[0].split('<td valign="top">')[1])
#!!ÖNEMLİ NOT:
#tezAdıING, Türkçe tez adları içermektedir.Bu sisteme yüklenme şekliyle ilgilidir.
#tezAdıING ve tezAdıTR değişkenleri çoğunluğa göre seçilmişitir. Düzeltmeyi yapma yolunu bulmadım.
#seçilen dillerin haricinde diller içerebilir. 
    tezYazarAdı=(tezKunye.split("<br/>")[1].split(":")[1])
    tezDanısmanAdı=(tezKunye.split("<br/>")[2].split(":")[1].strip())
    tezYerBilgisi=(tezKunye.split("<br/>")[3].split(":")[1].strip())
    tezLisansDerecesi=(tezDurumu.split("<br/>")[1].strip())
    tezYayimTarihi=(tezDurumu.split("<br/>")[2].strip())
    tezKonusuTR =(tezKunye.split("<br/>")[4].split("=")[0].split(":")[1])
    tezKonusuING=(tezKunye.split("<br/>")[4].split("=")[1].strip())
    #print(tezOzetING)
    """print(tezNo,tezAdıTR,tezAdıING,tezYazarAdı,tezDanısmanAdı,
          tezYerBilgisi,tezLisansDerecesi,
          tezKonusuTR,tezKonusuING,tezOzetTR,tezOzetING)"""
#hepsine tekrardan bakmakta fayda vardır.üsteki print komutunu test için aktif hale getiriniz.

#sırada bir sözlük yapmak var. headerları olan bir list için aşşağıdaki adımlar izlenmelidir.

    sonListe=[tezNo,tezAdıTR,tezAdıING,
              tezYazarAdı,tezDanısmanAdı,
              tezYerBilgisi,tezLisansDerecesi,
              tezYayimTarihi,
              tezKonusuTR,tezKonusuING,
              tezOzetTR,tezOzetING]
    
    
    headers= ["No","Adı_TR","Adı_ING","Yazar_Adı","Danisman_Adı",
              "Yer_Bilgisi","Lisans_Derecesi","Yayim_Tarihi",
              "Konusu_TR","Konusu_ING","Ozeti_TR","Ozeti_ING"]
    with open("tutorial.csv","a",newline="") as csvFile:
        fieldNames= ['Satır_sayısı',"No","Adı_TR","Adı_ING","Yazar_Adı","Danisman_Adı",
              "Yer_Bilgisi","Lisans_Derecesi","Yayim_Tarihi",
              "Konusu_TR","Konusu_ING","Ozeti_TR","Ozeti_ING"]
        thewriter= csv.DictWriter(csvFile,fieldnames=fieldNames)
        thewriter.writeheader()    
        counter=0
        for liste in sonListe:
            counter+=1
            dosya={"Satır_sayısı":[counter],"No":[tezNo],"Adı_TR":tezAdıTR,
                    "Adı_ING":[tezAdıING],"Yazar_Adı":[tezYazarAdı],
                    "Danisman_Adı":[tezDanısmanAdı],
                    "Yer_Bilgisi":[tezYerBilgisi],"Lisans_Derecesi":[tezLisansDerecesi],
                    "Yayim_Tarihi":[tezYayimTarihi],
                    "Konusu_TR":[tezKonusuTR],"Konusu_ING":[tezKonusuING],
                    "Ozeti_TR":[tezOzetTR],"Ozeti_ING":[tezOzetING]}
        
    print(sonListe)
    i+=1
