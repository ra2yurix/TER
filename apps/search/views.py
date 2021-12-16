from django.shortcuts import HttpResponse
from django.shortcuts import render

import time
from .models import SearchEngine

IMAGE_BASE_PATH = "https://image.tmdb.org/t/p/w500"
search_engine = SearchEngine()


def index(request):
    print("req", request)
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

def filter(request):
    res = request.GET.getlist("result")
    print(res)
    rating = request.GET.get("rating")
    year = request.GET.get("year")
    query = request.GET.get("search_text")
    # genre_list = request.GET.getlist('multi_genre')
    # date_q = QRY.DateRange("release_date", datetime.strptime(year.split(",")[0], "%Y"),datetime.strptime(year.split(",")[1], "%Y"))
    # rating_q = QRY.NumericRange("vote_average",int(rating.split(",")[0]), int(rating.split(",")[1]))
    # filter_q = QRY.And([date_q, rating_q])
    # if len(genre_list) > 0:
    #     genres_q=QRY.Or([QRY.Term(u"genres",unicode(x.lower())) for x in genre_list])
    #     filter_q = QRY.And([filter_q, genres_q])
    # ix = i.open_dir(INDEX_FILE)
    # searcher = ix.searcher(weighting=scoring.TF_IDF())
    # hitsList=[]
    # for x in res:
    #     res_q = QRY.Term(u"id", unicode(x))
    #     filter = QRY.And([filter_q, res_q])
    #     temp_hit = searcher.search(filter, filter=None, limit=None)
    #     if temp_hit:
    #         for y in temp_hit:
    #             hitsList.append(y)




    #
    # print(filter_q)

    return render(request, 'search.html',
                  { 'search_text': query,
                    'results':res})