from django.shortcuts import HttpResponse
from django.shortcuts import render

import time
from .models import SearchEngine


def index(request):
    if request.method == "POST":
        # start_time = time.time()
        engine = SearchEngine()
        text = request.POST.get("search_text")
        search_list = request.POST.getlist("search")
        trii = []
        for i in search_list:
            if i == "0":
                trii.append("title")
            if i == "1":
                trii.append("overview")

    return HttpResponse("Hmmmm")
