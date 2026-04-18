""" Amiral Battı Oyunu  - Python Terminal Oyunu
    Akıllı AI rakibi : Olasılık haritatsı + Hunt/Target modu"""

import random
from copy import deepcopy

#sabitler
BOYUT = 10
HARFLER = "ABCDEFGHIJ"
GEMILER = [
    ("Uçak Gemisi", 5),
    ("Zırhlı Gemi", 4),
    ("Destroyer", 3),
    ("Denizaltı", 3),
    ("Devriye", 2)
]

BOŞ = "."
GEMİ = "G"
ISABET = "X"
KAÇIRMA = "O"

#renk kodları
R = "\033[0m"
KIRMIZI   = "\033[91m"
YEŞİL     = "\033[92m"
SARI      = "\033[93m"
MAVİ      = "\033[94m"
CYAN      = "\033[96m"
GRİ       = "\033[90m"
BOLD      = "\033[1m"

#tahta
def yeni_tahta():
    return [[BOŞ] * BOYUT for _ in range(BOYUT)]

def tahta_göster(tahta, gizle=False, başlık=""):
    """Tahtayı renkli şekilde yazdır. gizle=True → gemileri gösterme."""
    print(f"\n{BOLD}{başlık}{R}")
    print(f"  {GRİ}" + "  ".join(str(i+1).rjust(2) for i in range(BOYUT)) + R)
    for r in range(BOYUT):
        satır = f"{BOLD}{HARFLER[r]}{R} "
        for c in range(BOYUT):
            hücre = tahta[r][c]
            if hücre == ISABET:
                satır += f"{KIRMIZI} X {R}"
            elif hücre == KAÇIRMA:
                satır += f"{GRİ} O {R}"
            elif hücre == GEMİ and not gizle:    
                satır += f"{YEŞİL} G {R}"
            else:
                satır += f"{GRİ} . {R}"
        print(satır)

def iki_tahta_göster(tahta1, tahta2, başlık1="Sen", başlık2="Rakip"):
    """İki tahtayı yan yana göster."""
    print(f"\n {BOLD}{başlık1:<35}{başlık2}{R}")
    header = " " + " ".join(str(i+1).rjust(2) for i in range(BOYUT))
    print(f" {GRİ} {header}  {header}{R}")
    for r in range(BOYUT):
        def satır_yap(tahta, gizle):
            s = f"{BOLD}{HARFLER[r]}{R} "
            for c in range(BOYUT):
                h = tahta[r][c]
                if h == ISABET: s += f"{KIRMIZI} X {R}"
                elif h == KAÇIRMA: s += f"{GRİ} O {R}"
                elif h == GEMİ and not gizle: s += f"{YEŞİL} G {R}"
                else: s += f"{GRİ} . {R}"
            return s
        print(satır_yap(tahta1, False) + " " + satır_yap(tahta2, True))

#gemi yerleştirme
def geçerli_mi(tahta, r, c, boyut, yön):
    "gemi bu konuma sığar mı"
    for i in range(boyut):
        nr = r + (i if yön == "D" else 0)
        nc = c + (i if yön == "Y" else 0)
        if not ( 0 <= nr < BOYUT and 0 <= nc < BOYUT):
            return False
        if tahta[nr][nc] != BOŞ:
            return False
    return True

def gemi_yerleştir(tahta, boyut):
    """rastgele geçerli konuma gemi yerleştir"""
    while True:
        yön= random.choic(["Y", "D"])
        r = random.randint(0, BOYUT - 1)
        c = random.randint(0, BOYUT - 1)
        if geçerli_mi(tahta, r, c, boyut, yön):
            for i in range(boyut):    
                nr = r + (i if yön == "D" else 0)
                nc = c + (i if yön == "Y" else 0)
                tahta[nr][nc] = GEMİ
            return ( r, c, yön)

def tahtayı_doldur(tahta):
    """tüm gemileri yerleştir"""
    konumlar = []
    for ad, boyut in GEMILER:
         konum = gemi_yerleştir(tahta, boyut)
         konumlar.append((ad, boyut, konum))
    return konumlar
     
def manuel_yerleştir(tahta):
    """oyuncunun gemileri ei ile yerleştirmesi"""
    print(f"\n{BOLD}Gemilerini yerleştir!{R}")
    print(f"Yön için: {CYAN}Y{R}=Yatay, {CYAN}D{R}=Dikey")
    print(f"Konum için örnek: {CYAN}A1{R}, {CYAN}B5{R}, {CYAN}J10{R}\n")
    for ad, boyut in GEMILER:
        tahta_göster(tahta, başlık=f"Mevcut tahtan:")
        while True:
            try:
                girdi = input(f"{BOLD}{ad}{R} ({boyut} hücre) -> Konum: ").strip().upper()
                yön = input(f" Yön(Y/D): ").strip().upper()
                if yön not in ("Y", "D"):
                    print(f"{KIRMIZI}Geçersiz yön.{R}"); continue
                r = HARFLER.index(girdi[0])
                c = int(girdi[1:]) - 1
                if geçerli_mi(tahta, r, c, boyut, yön):
                    for i in range(boyut):
                        nr = r + (i if yön == "D" else 0)
                        nc = c + (i if yön == "Y" else 0)
                        tahta[nr][nc] = GEMİ
                    break
                else:     
                    print(f"{KIRMIZI}Oraya sığmaz, tekrar dene.{R}")
            except ( ValueError, IndexError):
                print(f"{KIRMIZI}Geçersiz giriş. Örnek: A1{R}")

#oyuncu atışı 
def oyuncu_atışı(rakip_tahta):
    while True:
        try:
            girdi = input(f"\n{BOLD} Hedef koordinat (örn B7): {R}").strip().upper()
            r = HARFLER.index(girdi[0])
            c = int(girdi[1:]) - 1
            if not (0 <= r < BOYUT and 0 <= c < BOYUT):
                print(f"{KIRMIZI}Geçersiz koordinat.{R}"); continue
            if rakip_tahta[r][c] in (ISABET, KAÇIRMA):
                print(f"{SARI} Buraya zaten attın. {R}"); continue
            break
        except(ValueError, IndexError):
            print(f"{KIRMIZI} Geçersiz giriş. Örnek: A1{R}")
    return r, c

#AI
class AkıllıAI:
    """ Hunt/Target modu + olasılık haritası ile oyna AI"""

    def __init__(self):
        self.atılmış = set() #(r,c) - atılan tüm hücreler
        self.isabet_kümesi = [] #(r,c) - isabetler ( henüz batmayan)
        self.hedef_kuyruğu = [] #(r,c) - target modunda denenecekler
        self.eksen = None #"Y" veya "D" - tespit edilen eksen
        self.kalan_gemiler = [b for _, b in GEMILER]

#olasılık haritası
    def olasılık_haritası(self):
        harita = [[0] * BOYUT for _ in range(BOYUT)]

        for boyut in self.kalan_gemiler:
            #yatay
            for r in range(BOYUT):
                for c in range(BOYUT - boyut + 1):
                    hücreler = [(r, c+i) for i in range(boyut)]
                    if all((hr,hc) not in self.atılmış for hr, hc in hücreler):
                        for hr, hc in hücreler:
                            harita[hr][hc] += 1
            #dikey
            for r in range(BOYUT - boyut + 1):
                hücreler = [(r+1, c) for i in range(boyut)]
                if all((hr,hc) not in self.atılmış for hr, hc in hücreler):
                    for hr, hc in hücreler:
                        harita[hr][hc] += 1
        #zaten atılanları sıfırla
        for r, c in self.atılmış:
            harita[r][c] = 0
        return harita

#atış seç
def hedef_seç(self):
    #target modu: kuyrukta bekleyen hedef varsa onu kullan
    while self.hedef_kuyruğu:
        hedef = self.hedef_kuyruğu.pop(0)
        if hedef not in self.atılmış:
            return hedef
    #hunt modu: olasılık haritasından en yüksek hücreyi seç
    harita = self.olasılık_haritası()

    #checkerboard filtresi ( isabette değil, saf hunt'ta)
    if not self.isabet_kümesi:
        en_yüksek = -1
        adaylar = []
        for r in range(BOYUT):
            for c in range(BOYUT):
                if(r+c) % 2 == 0 and (r,c) not in self.atılmış:
                    if harita[r][c] > en_yüksek:
                        en_yüksek = harita[r][c]
                        adaylar = [(r,c)]
                    elif harita[r][c] == en_yüksek:
                        adaylar.append((r,c))
        if adaylar:
            return random.choice(adaylar)
    #checkerboard filtresiz en yüksek olasılıklı
    en_yüksek = -1
    adaylar = []
    for r in range(BOYUT):
        for c in range(BOYUT):
            if (r,c) not in self.atılmış:
                if harita[r][c] > en_yüksek:
                    en_yüksek = harita[r][c]
                    adaylar = [(r,c)]
                elif harita[r][c] == en_yüksek:
                    adaylar.append((r,c))
    return random.choice(adaylar) if adaylar else None                                                                                       