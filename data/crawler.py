import urllib.request
from urllib.error import HTTPError
import random
import json
import csv

# Get latest movie_ids from:
# http://files.tmdb.org/p/exports/movie_ids_MM_DD_YYYY.json.gz

API_KEY = "26b756fc787e114571f0efbb2e62817a"
ids = []


def create_ids():
    with open("movie_ids_01_06_2022.json", encoding="utf-8") as f:
        for line in f.readlines():
            movie = json.loads(line)
            ids.append(movie["id"])
    random.shuffle(ids)


def crawl_movies(begin, end):
    count = begin
    while count < end:
        url_details = "https://api.themoviedb.org/3/movie/" + str(ids[count]) + "?api_key=" + API_KEY
        url_keywords = "https://api.themoviedb.org/3/movie/" + str(ids[count]) + "/keywords?api_key=" + API_KEY
        try:
            detail = urllib.request.urlopen(url_details).read()
            keywords = urllib.request.urlopen(url_keywords).read()
        except Exception:
            count += 1
            print("\r{0}...".format(count), end="")
        else:
            try:
                detail = json.loads(detail.decode('utf-8'))
            except Exception:
                count += 1
                print("\r{0}...".format(count), end="")
            else:
                keywords = json.loads(keywords.decode('utf-8'))
                del keywords["id"]
                detail = dict(detail, **keywords)
                with open('movie_details.json', 'a+') as f:
                    json.dump(detail, f, indent=4)
                    f.write(',\n')
                count += 1
                print("\r{0}...".format(count), end="")

    print("Done.")


if __name__ == '__main__':
    create_ids()
    for i in range(30):
        crawl_movies(i*10000, (i+1)*10000)
