from django.shortcuts import HttpResponse
from django.shortcuts import render

import time
from .models import SearchEngine

IMAGE_BASE_PATH = "https://image.tmdb.org/t/p/w500"
search_engine = SearchEngine()


def index(request):
    print("111")
    if request.method == "POST":
        print("2222")
        start_time = time.time()
        search_text = request.POST.get("search_text")
        search_list = request.POST.getlist("search")
        fields = []
        for i in search_list:
            if i == "0":
                fields.append("title")
            if i == "1":
                fields.append("overview")

        result = search_engine.text_query(search_text)

        if result:
            print("3333")
            # p = result[0]["poster_path"]
            # img_path = IMAGE_BASE_PATH + p
            # html = requests.get(img_path, verify=False)
            # poster = Image.open(BytesIO(html.content))
            # poster_img = poster.crop()

            year = "1900,2021"
            rating = "0,10"
            elapsed_time = time.time() - start_time
            return render(request, 'search.html',
                          {'search': search_list, 'error': False, 'hits': result, 'search_text': search_text,
                           'elapsed': elapsed_time, 'number': 1, 'year': year, 'rating': rating, 'results': result})

    return render(request, "search.html", {"search_text": ""})
