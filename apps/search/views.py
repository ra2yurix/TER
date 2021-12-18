from django.shortcuts import HttpResponse
from django.shortcuts import render

import time
from .models import SearchEngine

IMAGE_BASE_PATH = "https://image.tmdb.org/t/p/w500"
search_engine = SearchEngine("tmdb")


def index(request):
    if request.method == "POST":
        start_time = time.time()
        search_text = request.POST.get("search_text")
        results = search_engine.text_query(search_text)

        if results:
            elapsed_time = time.time() - start_time
            return render(request, 'results.html', {'results': results, 'elapsed': elapsed_time})

    return render(request, "index.html", {"search_text": ""})