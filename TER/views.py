from django.shortcuts import render
from django.shortcuts import HttpResponse
from apps.search.views import index as search

#
# def index(request):
#     if request.method == "POST":
#         search(request)
#     return render(request, "index.html")
