from django.shortcuts import HttpResponse
from django.shortcuts import render
from .models import SearchEngine
from PIL import Image

IMAGE_BASE_PATH = "https://image.tmdb.org/t/p/w500"
search_engine = SearchEngine()


def index(request):
    if request.method == 'POST':
        return search(request)
    return render(request, "index.html")


def search(request):
    search_text = request.POST.get("search_text")
    image = request.FILES.get("upload_image")
    print(search_text)
    print(image)
    if search_text == "":
        print("image")
        results = search_engine.image_query(image)
    elif image is None:
        results = search_engine.text_query(search_text)
    if results:
        return render(request, "search.html", {'hits': results})


def search_img(request):
    fileImage = request.FILES.get('upload_image')
    results = search_engine.image_query(fileImage)
    if results:
        return render(request, "search.html", {'hits': results})
