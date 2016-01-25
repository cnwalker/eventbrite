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
            # Passes error through if user selected more than three category ids
            category_num = len(form.cleaned_data['category_ids'])
            if category_num > 3:
                return HttpResponseRedirect('/?too_many_categories=true')
            if category_num == 0:
                return HttpResponseRedirect('/?too_few_categories=true')
            event_search_url = "?category_ids=" + ",".join(form.cleaned_data['category_ids'])
            event_search_url += "&location=" + form.cleaned_data['location']
            return HttpResponseRedirect('/events/' + event_search_url)
        else:
            return HttpResponseRedirect('/?no_location=true')
    else:
        # Raises an error if user has not selected any categories
        if request.GET.get('too_few_categories'):
            args['error'] = "You must select at least 1 category"

        # Raises an error if user selected more than three category ids
        if request.GET.get('too_many_categories'):
            args['error'] = "You may select no more than 3 categories"

        if request.GET.get('no_location'):
            args['error'] = "You must include a location"
        # Form will initialize with valid categories from eventbrite API
        args['category_form'] = CategoryForm()
        return render(request, 'index.html', args)

def events(request):
    args = {}
    page = ""
    location = ""

    # This page doesn't accept POST requests
    if request.method == "POST":
        return render(request, 'index.html', args)
    else:
        if request.GET.get('location'):
            # Takes in location as a GET parameter
            args['location'] = request.GET.get('location')

        if request.GET.get('category_ids'):
            # Takes in comma delimited category ids as GET parameters
            args['category_ids'] = request.GET.get('category_ids')

        # Gets event data from the API
        event_info = evbrite.get_events_by_category_id(args.get('category_ids').split(','),
                                                       args.get('location'), request.GET.get('page'))
        if event_info:
            # This checks to make sure that the evbrite repsonse wasn't None
            if event_info.get('error'):
                #If the API raises an error, pass the error through so the template can display the error page
                args['error'] = event_info
                return render(request, 'events.html', event_info)
            else:
                # If the API has not raised an error then prepare to pass it through to the template
                args['events'] = event_info.get('events')

        pagination = event_info.get('pagination')
        # Convert page_number and page_count to ints to do first and last checks
        current_page = int(pagination.get('page_number'))
        total_pages = int(pagination.get('page_count'))

        if current_page < total_pages:
            # Set a next page variable on args if not at the last page returned by the API
            args['next_page'] = str(int(pagination['page_number']) + 1)
        if current_page > 1:
            # Set a prev page variable on args if not at the first page
            args['prev_page'] = str(current_page - 1)
        args['current_page'] = pagination.get('page_number')
        args['total_pages'] = pagination.get('page_count')
        args['on_events_page'] = "on_events_page"
    return render(request, 'events.html', args)
