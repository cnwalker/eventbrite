import evbrite
import requests, os
from forms import CategoryForm
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

def index(request):
    args = {}
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            if len(form.cleaned_data['category_ids']) > 3:
                return HttpResponseRedirect('/?too_many_categories=true')

            event_search_url = "?category_ids=" + ",".join(form.cleaned_data['category_ids'])
            event_search_url += "&location=" + form.cleaned_data['location']
            return HttpResponseRedirect('/events/' + event_search_url)
    else:
        #Form will initialize with valid categories from eventbrite API
        if request.GET.get('too_many_categories'):
            args['error'] = "You may select no more than 3 categories" 
        else:
            args['category_form'] = CategoryForm()
        return render(request, 'index.html', args)

def events(request):
    args = {}
    page = ""
    location = ""

    if request.method == "POST":
        print("lol")
    else:
        #Takes in location and category ids as URL parameters
        if request.GET.get('location'):
            args['location'] = request.GET.get('location')

        event_info = evbrite.get_events_by_category_id(request.GET.get('category_ids').split(','),
                                                       args.get('location'), request.GET.get('page'))

        #If the API raises an error, pass the error through so the template can display the error page
        if event_info.get('error'):
            print('error detected!')
            return render(request, 'events.html', event_info)

        if event_info:
            args['events'] = event_info.get('events')

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
