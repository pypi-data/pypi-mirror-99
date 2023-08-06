# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from requests import Session
from parsel   import Selector

from shutil      import copyfileobj
from pytesseract import image_to_string 
from PIL         import Image

from os import remove

class BTKSorgu(object):
    """Hedef websitesinin BTK Tarafından Erişim Engeli Sorgusu
    
    Dönüş :
        (str)
            {domain}, {karar}
            Karar Bulunamadı.
    """
    def __init__(self, sorgu_url:str, arka_plan:bool=False):
        self.arka_plan     = arka_plan
        self.ana_sayfa     = "https://internet2.btk.gov.tr"
        self.sorgu_sayfasi = "https://internet2.btk.gov.tr/sitesorgu/"
        self.sorgu_url     = sorgu_url

        self.oturum = Session()

    @property
    def captcha_ver(self):
        ilk_bakis    = self.oturum.get(self.sorgu_sayfasi, allow_redirects=True)
        captcha_yolu = Selector(ilk_bakis.text).xpath("//div[@class='arama_captcha']/img/@src").get()

        captcha_data = self.oturum.get(f"{self.ana_sayfa}{captcha_yolu}", stream=True)
        with open('captcha.png', 'wb') as captcha_gorsel:
            copyfileobj(captcha_data.raw, captcha_gorsel)

        return image_to_string(Image.open('captcha.png')).strip().replace(' ', '')

    @property
    def karar(self):
        captcha = self.captcha_ver

        payload = {
            "deger"             : self.sorgu_url,
            "ipw"               : '',
            "kat"               : '',
            "tr"                : '',
            "eg"                : '',
            "ayrintili"         : 0,
            "submit"            : "Sorgula",
            "security_code"     : captcha
        }

        kimlik = {
            "Content-Type"             : "application/x-www-form-urlencoded",
            "Host"                     : "internet2.btk.gov.tr",
            "Origin"                   : self.ana_sayfa,
            "Referer"                  : self.sorgu_sayfasi,
        }

        karar_sayfasi = self.oturum.post(self.sorgu_sayfasi, headers=kimlik, data=payload)

        # print(karar_sayfasi.text)
        secici     = Selector(karar_sayfasi.text)
        hatali_kod = secici.xpath("//div[@class='icerik']/ul/li/text()").get()
        erisim_var = secici.xpath("//div[@class='yazi2']/text()").get()
        erisim_yok = secici.xpath("//span[@class='yazi2_2']/text()").get()
        karar  = hatali_kod or erisim_var or erisim_yok or ''

        if self.arka_plan:
            print(f"""

            # Sorgu   : {self.sorgu_url}
            # Captcha : {captcha}
            # Karar   : {karar}

""")
        return karar

    def __repr__(self) -> str:
        hatalar = ['Lütfen güvenlik kodunu giriniz.', 'Güvenlik kodunu yanlış girdiniz. Lütfen Güvenlik Kodunu resimde gördüğünüz şekilde giriniz.']
        while True:
            karar = self.karar
            if karar not in hatalar:
                remove('captcha.png')
                return karar