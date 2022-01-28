from django.shortcuts import HttpResponse
from django.shortcuts import render
from .models import SearchEngine

IMAGE_BASE_PATH = "https://image.tmdb.org/t/p/w500"
search_engine = SearchEngine()


def index(request):
    if request.GET.get("search_text"):
        return search(request)
    return render(request, "newIndex.html")


def search(request):
    search_text = request.GET.get("search_text")
    results = search_engine.text_query(search_text)
    # for i in results:
    #
    #     return render(request, "newSearch.html", {})
    # else:
    #     return render(request, "ChangjunSaysNO.html")
    if not results:
        return render(request, "ChangjunSaysNO.html")
    else:
        print("-----")
        print(results[0])
        print("-----000")
        print(results[0]["genres"])
        # return render(request, "newSearch.html")
        return render(request, "newSearch.html", {'movies': results[0]["title"], 'genre': results[0]["genres"]})
