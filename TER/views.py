from django.shortcuts import render


def index(request):
    context = {"hello": "Hello World!"}
    return render(request, "index.html", {"search_text": ""})