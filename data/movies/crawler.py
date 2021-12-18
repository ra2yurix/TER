import urllib.request
from urllib.error import HTTPError
import random
import json
import csv

# Get latest movie_ids from:
# http://files.tmdb.org/p/exports/movie_ids_MM_DD_YYYY.json.gz

API_KEY = "26b756fc787e114571f0efbb2e62817a"


# count = 0
# keywords_line = ""
# keywords_lines = []
# while count < number:
#     url_details = "https://api.themoviedb.org/3/movie/" + str(movie_ids[count]) + "?api_key=" + API_KEY
#     url_keywords = "https://api.themoviedb.org/3/movie/" + str(movie_ids[count]) + "/keywords?api_key=" + API_KEY
#     try:
#         detail = urllib.request.urlopen(url_keywords).read()
#     except Exception:
#         count += 1
#         print("\r{0}...".format(count), end="")
#     else:
#         movie = json.loads(movie.decode('utf-8'))
#         movies.append(movie)
#         count += 1
#         print("\r{0}...".format(count), end="")
#
# url_details = "https://api.themoviedb.org/3/movie/497698?api_key=26b756fc787e114571f0efbb2e62817a"
# url_keywords = "http://api.themoviedb.org/3/movie/497698/keywords?api_key=26b756fc787e114571f0efbb2e62817a"
# movie = urllib.request.urlopen(url_keywords).read()
# movie = json.loads(movie.decode('utf-8'))
#
# for i in movie:
#     keywords_line = keywords_line + i["name"] + " "
#
# movie = urllib.request.urlopen(url_keywords).read()
# movie = json.loads(movie.decode('utf-8'))["keywords"]
#
# for i in movie:
#     keywords_line = keywords_line + i["name"] + " "
# print(keywords_line)


def crawl_movies(number):
    ids = []
    with open("movie_ids_12_17_2021.json", encoding="utf-8") as f:
        for line in f.readlines():
            movie = json.loads(line)
            ids.append(movie["id"])
    random.shuffle(ids)

    count = 0
    details = []
    keywords_lines = []
    while count < number:
        url_details = "https://api.themoviedb.org/3/movie/" + str(ids[count]) + "?api_key=" + API_KEY
        url_keywords = "https://api.themoviedb.org/3/movie/" + str(ids[count]) + "/keywords?api_key=" + API_KEY
        try:
            detail = urllib.request.urlopen(url_details).read()
            keywords = urllib.request.urlopen(url_keywords).read()
        except Exception:
            count += 1
            print("\r{0}...".format(count), end="")
        else:
            detail = json.loads(detail.decode('utf-8'))
            details.append(detail)
            keywords_line = detail["title"]
            for genre in detail["genres"]:
                keywords_line = keywords_line + " " + genre["name"]
            keywords = json.loads(keywords.decode('utf-8'))
            for keyword in keywords["keywords"]:
                keywords_line = keywords_line + " " + keyword["name"]
            keywords_line = keywords_line + "\n"
            keywords_lines.append(keywords_line)
            count += 1
            print("\r{0}...".format(count), end="")

    with open('movie_details.json', 'w') as f:
        json.dump(details, f, indent=4)

    with open('movie_keywords.txt', 'w', newline='', encoding='utf-8') as f:
        print(keywords_lines)
        f.writelines(keywords_lines)

    print("Done.")


if __name__ == '__main__':
    crawl_movies(100000)
