import json
import pandas as pd
import os

# 1. Ayarları ve Verileri Yükle
with open('config.json', 'r') as f:
    config = json.load(f)

# CSV dosyasını oku
df = pd.read_csv('parcalar.csv')

def hesapla(row):
    # Formül 1: Net Satınalma (TRY)
    net_satinalma = row['Brut_EUR'] * config['kur']
    
    # Formül 2: Liste Fiyatı (Ham)
    # (Net Satınalma / (1 - GM2/100)) / 0.7
    liste_ham = (net_satinalma / (1 - (config['plan_gm2'] / 100))) / 0.7
    
    # Formül 3: Liste Fiyatı (MROUND 5) - En yakın 5'e yuvarla
    liste_mround = 5 * round(liste_ham / 5)
    
    # Formül 4: TNS (Net Satış)
    tns = liste_mround * config['premium_katsayi']
    
    # Formül 5: GMS (Brüt Kar Marjı)
    # ((TNS - Net Satınalma) / TNS) - (SG&AV / 100)
    if tns != 0:
        gms = ((tns - net_satinalma) / tns) - (config['sg_av'] / 100)
    else:
        gms = 0
    
    return pd.Series([
        round(net_satinalma, 2),
        liste_mround, 
        round(tns, 2), 
        f"%{round(gms*100, 2)}"
    ])

# Hesaplamayı uygula
df[['Net_Satinalma_TRY', 'Liste_Fiyati_MROUND', 'TNS_Net_Satis', 'GMS_Kar_Marji']] = df.apply(hesapla, axis=1)

# Sonucu yeni bir CSV olarak kaydet
df.to_csv('guncel_fiyat_listesi.csv', index=False)
print("Hesaplama başarıyla tamamlandı.")
