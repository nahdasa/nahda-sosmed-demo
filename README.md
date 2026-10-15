# Demo Web Scraping dengan Python

Demo mata kuliah Social Media Analysis - Teknik Web Scraping.
Target: https://quotes.toscrape.com (situs latihan scraping).

## Isi demo
1. Ambil HTML mentah dengan urllib
2. Parsing dengan BeautifulSoup
3. find_all untuk banyak elemen
4. Exception handling
5. Perbandingan parser html.parser vs lxml
6. Scraping banyak halaman dan simpan ke CSV

## Cara menjalankan
```
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scraper.py
python scraper.py --demo 6 --pages 5
```

Hasil demo 6 tersimpan di `quotes.csv`.

## Catatan etika
Scraping hanya dilakukan pada situs latihan, dengan jeda antar request.