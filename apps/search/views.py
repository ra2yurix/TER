from django.shortcuts import HttpResponse
from django.shortcuts import render

import time
from .models import SearchEngine

IMAGE_BASE_PATH = "https://image.tmdb.org/t/p/w500"
search_engine = SearchEngine("mongo")


def index(request):
    if request.GET.get("search_text"):

        return search(request)
    return render(request, "index.html")


def search(request):

        # start_time = time.time()
    search_text = request.GET.get("search_text")
    results = search_engine.text_query(search_text)
    for i in results:
        print(i)
    if results:
        return render(request, "search.html")
        # elapsed_time = time.time() - start_time
        # return render(request, 'search.html', {'results': results, 'elapsed': elapsed_time})

    return render(request, "index.html")
