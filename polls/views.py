from curses.ascii import HT
from django.shortcuts import render

from django.http import HttpResponse

def show(request):
    return HttpResponse("Hello world. You're at the polls index")

# Create your views here.
