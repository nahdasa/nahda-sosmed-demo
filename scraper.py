"""
Demo Web Scraping dengan Python
Mata kuliah: Social Media Analysis - Teknik Web Scraping

Situs target: https://quotes.toscrape.com
(situs latihan resmi untuk belajar scraping, aman dan legal)

Jalankan semua demo : python scraper.py
Jalankan satu demo  : python scraper.py --demo 3
Atur jumlah halaman : python scraper.py --demo 6 --pages 5
"""
import argparse
import time
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

import pandas as pd
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://quotes.toscrape.com"
HEADERS = {"User-Agent": "Mozilla/5.0 (Educational scraping demo)"}


def judul(teks):
    print("\n" + "=" * 60)
    print(teks)
    print("=" * 60)


def fetch_html(url, retries=3, delay=2):
    """Ambil HTML dengan retry. Return None jika semua percobaan gagal."""
    for percobaan in range(1, retries + 1):
        try:
            res = requests.get(url, headers=HEADERS, timeout=10)
            res.raise_for_status()
            return res.text
        except requests.exceptions.RequestException as e:
            print(f"  Percobaan {percobaan}/{retries} gagal: {e}")
            time.sleep(delay)
    return None


# Demo 1 - Mengambil HTML mentah (urllib)
def demo_1_urlopen():
    judul("DEMO 1: Ambil HTML mentah dengan urllib.urlopen")
    html = urlopen(BASE_URL)
    konten = html.read()
    print("Tipe data :", type(konten))
    print("300 karakter pertama:\n", konten[:300])


# Demo 2 - Parsing dengan BeautifulSoup
def demo_2_beautifulsoup():
    judul("DEMO 2: Parsing dengan BeautifulSoup")
    soup = BeautifulSoup(fetch_html(BASE_URL), "html.parser")
    print("soup.title        :", soup.title)
    print("soup.title.text   :", soup.title.get_text(strip=True))
    print("find('span') text :", soup.find("span", class_="text").get_text(strip=True))
    print("find('small') pen.:", soup.find("small", class_="author").get_text(strip=True))


# Demo 3 - find_all
def demo_3_find_all():
    judul("DEMO 3: find_all() - ambil semua kutipan di halaman 1")
    soup = BeautifulSoup(fetch_html(BASE_URL), "html.parser")
    for i, item in enumerate(soup.find_all("div", class_="quote"), start=1):
        teks = item.find("span", class_="text").get_text(strip=True)
        print(f"{i}. {teks}")


# Demo 4 - Connecting & Exceptions
def get_title(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        print("  HTTP Error:", e)
        return None
    except URLError:
        print("  Server tidak ditemukan!")
        return None
    try:
        bs = BeautifulSoup(html.read(), "html.parser")
        title = bs.body.h1
    except AttributeError:
        return None
    return title


def demo_4_error_handling():
    judul("DEMO 4: Exception handling")
    daftar_url = [
        BASE_URL,                                   # berhasil
        BASE_URL + "/halaman-tidak-ada",            # HTTP 404
        "https://domain-ini-tidak-ada-123.com",     # server tidak ditemukan
    ]
    for url in daftar_url:
        print(f"\nURL: {url}")
        title = get_title(url)
        if title is None:
            print("  Title could not be found")
        else:
            print("  Title:", title.get_text(strip=True))


# Demo 5 - Perbandingan parser
def demo_5_parsers():
    judul("DEMO 5: html.parser vs lxml")
    html = fetch_html(BASE_URL)
    soup1 = BeautifulSoup(html, "html.parser")
    print("html.parser :", soup1.h1.get_text(strip=True))
    try:
        soup2 = BeautifulSoup(html, "lxml")
        print("lxml        :", soup2.h1.get_text(strip=True))
    except Exception:
        print("lxml belum terpasang -> pip install lxml")


# Demo 6 - Scraping beberapa halaman lalu simpan ke CSV
def demo_6_to_csv(pages=3):
    judul(f"DEMO 6: Scraping {pages} halaman -> CSV")
    data = []
    for page in range(1, pages + 1):
        url = f"{BASE_URL}/page/{page}/"
        print(f"Mengambil {url}")
        html = fetch_html(url)
        if html is None:
            print("  Dilewati.")
            continue
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all("div", class_="quote"):
            data.append({
                "kutipan": item.find("span", class_="text").get_text(strip=True),
                "penulis": item.find("small", class_="author").get_text(strip=True),
                "tag": ", ".join(t.get_text() for t in item.find_all("a", class_="tag")),
                "halaman": page,
            })
        time.sleep(1)  # jeda sopan agar tidak membebani server

    df = pd.DataFrame(data)
    df.to_csv("quotes.csv", index=False, encoding="utf-8-sig")
    print(f"\nTersimpan {len(df)} baris ke quotes.csv")
    print(df.head())


def main():
    parser = argparse.ArgumentParser(description="Demo Web Scraping")
    parser.add_argument("--demo", default="all", choices=["1", "2", "3", "4", "5", "6", "all"])
    parser.add_argument("--pages", type=int, default=3, help="jumlah halaman untuk demo 6")
    args = parser.parse_args()

    demos = {
        "1": demo_1_urlopen,
        "2": demo_2_beautifulsoup,
        "3": demo_3_find_all,
        "4": demo_4_error_handling,
        "5": demo_5_parsers,
        "6": lambda: demo_6_to_csv(args.pages),
    }
    if args.demo == "all":
        for fn in demos.values():
            fn()
    else:
        demos[args.demo]()


if __name__ == "__main__":
    main()