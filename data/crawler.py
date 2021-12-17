import urllib.request
from urllib.error import HTTPError
import random
import json
import csv

# Get latest movie_ids from:
# http://files.tmdb.org/p/exports/movie_ids_MM_DD_YYYY.json.gz

API_KEY = "26b756fc787e114571f0efbb2e62817a"


def get_movies(number):
    movie_ids = []
    with open("movie_ids_12_15_2021.json", encoding="utf-8") as f:
        for line in f.readlines():
            movie = json.loads(line)
            movie_ids.append(movie["id"])
    random.shuffle(movie_ids)

    count = 0
    movies = []
    while count < number:
        url = "https://api.themoviedb.org/3/movie/" + str(movie_ids[count]) + "?api_key=" + API_KEY

        try:
            movie = urllib.request.urlopen(url).read()
        except HTTPError:
            count += 1
            print("\r{0}...".format(count), end="")
        else:
            movie = json.loads(movie.decode('utf-8'))
            movies.append(movie)
            count += 1
            print("\r{0}...".format(count), end="")

    # list of dicts to json
    with open('movies.json', 'w') as f:
        json.dump(movies, f, indent=4)

    # # list of dicts to csv
    #
    # headers = movies[0].keys()
    # with open('movies.csv', 'w', newline='', encoding='utf-8') as f:
    #     f_csv = csv.DictWriter(f, headers)
    #     f_csv.writeheader()
    #     f_csv.writerows(movies)

    print("Done.")


if __name__ == '__main__':
    get_movies(10000)
