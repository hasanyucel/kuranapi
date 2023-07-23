from fastapi import FastAPI,HTTPException
from custom_logger import CustomLoggerMiddleware
import sqlite3

db_file = "kuran_database.db"
app = FastAPI()
app.add_middleware(CustomLoggerMiddleware)

diller_db = {
    "Almanca (Abu Rida)": "de_aburida",
    "İngilizce (Yusuf Ali)": "en_yusufali",
    "Fransızca (Hamidullah)": "fr_hamidullah",
    "İtalyanca (Piccardo)": "it_piccardo",
    "Japonca": "ja_japanese",
    "KU (Asan)": "ku_asan",
    "Orjinal Arapça": "quran_text",
    "Rusça (Muntahab)": "ru_muntahab",
    "Türkçe (Diyanet)": "tr_diyanet",
    "Özbekçe (Sodik)": "uz_sodik"
}

def get_metin(dil, sure, ayet):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute(f'SELECT text FROM {dil} where sura = {sure} and aya = {ayet}')
    text = cur.fetchone()
    conn.close()
    return text

def get_sureler():
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute('SELECT * FROM sureler')
    rows = cur.fetchall()
    conn.close()
    sureler = [{"sure_no": row[0], "ayet_sayisi": row[1], "sure_ismi": row[2]} for row in rows]
    return sureler

def get_sure_adi(sure_no):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute(f'SELECT sure_adi FROM sureler where sure_no = {sure_no}')
    row = cur.fetchone()
    conn.close()
    return row[0]

@app.get("/")
def bismillahirrahmanirrahim():
    result = {
                "KuranAPI" : "Bismillahirrahmanirrahim!",
                "Api Dokümanı" : "/docs",
                "Diller": "/diller",
                "Sureler": "/sureler",
                "Kaynaklar":["https://tanzil.net","https://www.ubilisim.com"],
                "Developed By":"Hasan Hüseyin YÜCEL",
                "Contact":"https://www.linkedin.com/in/hhy34/"
             }
    return result

@app.get("/diller")
def diller():
    return diller_db 

@app.get("/sureler")
def sureler():
    sureler = get_sureler()
    return sureler

@app.get("/get_ayet/{dil}/{sure}/{ayet}")
def get_ayet(dil: str, sure: int, ayet: int):
    for lang_key, lang_value in diller_db.items():
        if lang_value == dil:
            text = get_metin(dil,sure,ayet)
            if text:
                sure_adi = get_sure_adi(sure)
                metin = text[0]
                result = {
                    "Dil": lang_key,
                    "Sure No": sure,
                    "Sure Adı" : sure_adi,
                    "Ayet No": ayet,
                    "Ayet": text[0]
                }
                return result
            else:
                raise HTTPException(status_code=404, detail="Sure veya ayet bulunamadı!")
            
    raise HTTPException(status_code=404, detail="Dil bulunamadı!")