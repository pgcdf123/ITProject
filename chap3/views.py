from django.shortcuts import render

from django.http import HttpResponse


def indexpage(request):
    return HttpResponse("Rango says this chap3 app indexpage!!")

