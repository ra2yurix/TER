from django.shortcuts import HttpResponse
from django.shortcuts import render

import time
from .models import SearchEngine

IMAGE_BASE_PATH = "https://image.tmdb.org/t/p/w500"
search_engine = SearchEngine()


def index(request):
    if request.method == "POST":
        start_time = time.time()
        search_text = request.POST.get("search")

        result = search_engine.text_query(search_text)

        if result:

            elapsed_time = time.time() - start_time
            return render(request, 'results.html',
                          {'error': False,  'search_text': search_text,
                           'elapsed': elapsed_time, 'number': 1, 'year': year, 'rating': rating, 'results': result})

    return render(request, "results.html", {"search_text": ""})