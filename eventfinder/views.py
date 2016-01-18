import requests, os
import evbrite
from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting
from models import CategoryList

def index(request):
    args = {}
    display_categories = evbrite.get_categories()
    if display_categories.get('categories') and not display_categories.get('error'):
        args['categories'] = display_categories['categories']
    else:
        args['error'] = display_categories
    return render(request, 'index.html', args)

def db(request):
    greeting = Greeting()
    greeting.save()
    greetings = Greeting.objects.all()
    return render(request, 'db.html', {'greetings': greetings})
