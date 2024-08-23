from django.http import HttpResponse


def index(request):
    return HttpResponse("hello world")


def product_list(request):
    return HttpResponse("list of products")
