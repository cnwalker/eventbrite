import requests, os
import evbrite
from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    args = {}
    display_categories = evbrite.get_categories()
    if display_categories.get('categories') and not display_categories.get('error'):
        args['categories'] = display_categories['categories']
    else:
        args['error'] = display_categories
    return render(request, 'index.html', args)

def events(request):
    args = {}
    page = ""
    location = ""

    #Takes in location and category ids as URL parameters
    if request.GET.get('location'):
        args['location'] = request.GET.get('location')

    event_info = evbrite.get_events_by_category_id(request.GET.get('category_ids').split(','),
                                                   args.get('location'), request.GET.get('page'))

    if event_info.get('error'):
        print('error detected!')
        return render(request, 'events.html', event_info)

    if event_info:
        args['events'] = event_info.get('events')

    print(args['events'])

    # Set a next page variable on args if not at the last page returned by the API
    pagination = event_info.get('pagination')
    current_page = int(pagination.get('page_number'))
    total_pages = int(pagination.get('page_count'))

    if current_page < total_pages:
        args['next_page'] = str(int(pagination['page_number']) + 1)
    if current_page > 1:
        args['prev_page'] = str(current_page - 1)

    args['current_page'] = pagination.get('page_number')
    return render(request, 'events.html', args)

def db(request):
    greeting = Greeting()
    greeting.save()
    greetings = Greeting.objects.all()
    return render(request, 'db.html', {'greetings': greetings})
