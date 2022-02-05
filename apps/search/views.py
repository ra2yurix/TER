from django.shortcuts import HttpResponse
from django.shortcuts import render
from .models import SearchEngine
from PIL import Image


IMAGE_BASE_PATH = "https://image.tmdb.org/t/p/w500"
search_engine = SearchEngine()


def index(request):
    if request.GET.get("search_text"):
        return search(request)
    return render(request, "index.html")


def search(request):
    search_text = request.GET.get("search_text")
    results = search_engine.text_query(search_text)
    fileImage = request.FILES.get('uploadPicture')
    if results:
        return render(request, "search.html", {'hits': results})
