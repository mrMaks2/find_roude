from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    name = 'Maks'

    return render(request, 'home.html', {'name' : name})