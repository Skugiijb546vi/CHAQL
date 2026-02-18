import requests
import firebase_admin
from firebase_admin import credentials, db
import time

# 1. Firebase Setup
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {'databaseURL': 'لینکەکەت'})

TMDB_API_KEY = "کلیلی_تۆ"

def sync_new_movies():
    # وەرگرتنی لیستی فیلمە نوێیەکانی ئەمڕۆ لە TMDB
    url = f"https://api.themoviedb.org/3/movie/now_playing?api_key={TMDB_API_KEY}&language=en-US&page=1"
    movies = requests.get(url).json().get('results', [])

    for m in movies:
        movie_id = str(m['id'])
        # پشکنین: ئایا پێشتر ئەم فیلمەمان زیاد کردووە؟
        ref = db.reference(f'/subtitled_movies/{movie_id}')
        if ref.get() is None:
            # ئەگەر نوێ بوو، زانیارییەکان ڕێکبخە و بێنێرە
            data = {
                "id": m['id'],
                "title": m['title'],
                "poster": f"https://image.tmdb.org/t/p/w500{m['poster_path']}",
                "url": f"https://vidsrc.me/embed/movie?tmdb={movie_id}",
                "type": "movie",
                "subtitleEnglish": f"https://sub.wyzie.ru/search?id={movie_id}&format=srt&encoding=utf-8",
                # لێرە هەموو فێڵدەکانی تری مۆدێلەکەت زیاد بکە...
            }
            ref.set(data)
            print(f"🆕 فیلمی نوێ زیاد کرا: {m['title']}")

# ئەمە وا دەکات کۆدەکە ٢٤ سەعات ئیش بکات
while True:
    sync_new_movies()
    print("سەعاتێکی تر دووبارە دەپشکنمەوە...")
    time.sleep(3600) # هەموو یەک سەعات جارێک بپشکنە
