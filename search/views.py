from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models.functions import Lower
from .models import Event, Venue
from .forms import VenueForm, EventForm
import csv

# below are imports necessary for pdf
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

# Import Pagination Stuff
from django.core.paginator import Paginator



#generate pdf file venue list
def venue_pdf(request):
    # Create Bytestream buffer
    buf = io.BytesIO()
    # Create a canvas
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    # Create a text object
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)
    # Creating a Model
    venues = Venue.objects.all()
    lines = []
    # Loop
    for venue in venues:
        lines.append(venue.name)
        lines.append(venue.address)
        lines.append(venue.zip_code)
        lines.append(venue.phone)
        lines.append(venue.web)
        lines.append(venue.email_address)
        lines.append("")

    for line in lines:
        textob.textLine(line)
    # Finish Up
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
    
    return FileResponse(buf, as_attachment=True, filename='venues.pdf')

def venue_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=venues.csv'
    # create a csv writer
    writer = csv.writer(response)
    # Designate the model
    venues = Venue.objects.all()
    # Add column headings to the csv file
    writer.writerow(['Venue Name', 'Address', 'Zip Code', 'Phone', 'Web Address', 'Email'])

    for venue in venues:
        textfile_content = [venue.name,venue.address,
        venue.phone,venue.web,venue.email_address]
        writer.writerow(textfile_content)

    return response

def venue_text(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=venues.txt'

    # designate the model
    venues = Venue.objects.all()
    # create blank list
    lines = []
    # loop through and output
    for venue in venues:
        textfile_content = (
            f'{venue.name}\n{venue.address}\n{venue.phone}\n'
            f'{venue.web}\n{venue.email_address}\n\n'
        )
        lines.append(textfile_content)
    # write to textfile
    response.writelines(lines)
    return response


def delete_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue.delete()
    return redirect('list-venues')

def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    event.delete()
    return redirect('list-events')

def update_event(request, event_id):
    up_event = Event.objects.get(pk=event_id)  #this event_id from line above
    form = EventForm(request.POST or None, instance=up_event) #instance pre-fills with existing data
    if form.is_valid():
        form.save()
        return redirect('list-events')
    return render(request, 'search/update_event.html', {
        'up_event': up_event,
        'form': form,
    })

def add_event(request):
    submitted = False  #see if form was submitted, first time at page --> False
    if request.method == "POST":  #method references <form method=POST> determine if submitted or not
        form = EventForm(request.POST)  #if form is filled out, add to VenueForm
        if form.is_valid():    #if the filled out thing is valid
            form.save()      #save it to the database
            return HttpResponseRedirect('/add_event?submitted=True')   #once saved, return to same page, but submitted variable is changed to True
    else:    #if form isnt filled out form, just came to webpage
        form = EventForm    #form is still, VenueForm
        if 'submitted' in request.GET:  #3 lines above submits submitted variable into get request
            submitted = True #if submitted variable is found in the get request, change variable to true

    return render(request, 'search/add_event.html', {
        "form": form,    #pass in form
        "submitted": submitted,    #pass in submitted, html page will decide what to do, if submitted is True or False
    })

def update_venue(request, venue_id):
    up_venue = Venue.objects.get(pk=venue_id)  #this venue_id from line above
    form = VenueForm(request.POST or None, instance=up_venue) #instance pre-fills with existing data
    if form.is_valid():
        form.save()
        return redirect('list-venues')
    return render(request, 'search/update_venue.html', {
        'up_venue': up_venue,
        'form': form,
    })



def search_venues(request):
    #must determine if somebody has gone to the page, or filled out form
    if request.method == "POST":
        searched = request.POST['searched']  #searched is whatever somebody typed into box
        venues_query = Venue.objects.filter(name__contains=searched) #not case sensitive
        return render(request, 'search/search_venues.html', {
        'searched': searched,
        'venues': venues_query,
        })
    else:
        return render(request, 'search/search_venues.html', {
        
        })

def show_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    return render(request, 'search/show_venue.html', {
        'venue': venue
    })


def list_venues(request):
    # venue_list = Venue.objects.all().order_by('name')
    venue_list = Venue.objects.all()
    p = Paginator(Venue.objects.all(), 2)
    page = request.GET.get('page')   #request is 4 lines about in func def
    venues = p.get_page(page)


    return render(request, 'search/venues.html', 
    {
        'venue_list': venue_list,
        'venues': venues
    })

def add_venue(request):
    submitted = False  #see if form was submitted, first time at page --> False
    if request.method == "POST":  #method references <form method=POST> determine if submitted or not
        form = VenueForm(request.POST)  #if form is filled out, add to VenueForm
        if form.is_valid():    #if the filled out thing is valid
            venue = form.save(commit=False) #save, but dont save it yet
            venue.owner = request.user.id #add logged in user id to form
            venue.save()      #save it to the database
            return HttpResponseRedirect('/add_venue?submitted=True')   #once saved, return to same page, but submitted variable is changed to True
    else:    #if form isnt filled out form, just came to webpage
        form = VenueForm    #form is still, VenueForm
        if 'submitted' in request.GET:  #3 lines above submits submitted variable into get request
            submitted = True #if submitted variable is found in the get request, change variable to true

    return render(request, 'search/add_venue.html', {
        "form": form,    #pass in form
        "submitted": submitted,    #pass in submitted, html page will decide what to do, if submitted is True or False
    })

def all_events(request):
    event_list = Event.objects.all().order_by(Lower('name').desc())
    return render(request, 'search/event_list.html', {
        'event_list': event_list
    })


def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
    word = "bios"
    # convert month from name to number
    month = month.capitalize()
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)

    # create calendar
    cal = HTMLCalendar().formatmonth(
        year, 
        month_number)

    # get current year
    now = datetime.now()
    current_year = now.year

    # get current time
    current_time = now.strftime('%I:%M:%S %p')

    return render(request, 'search/home.html', 
    {
    "reference": word,
    "year": year,
    "month": month,
    "month_number": month_number,
    "cal": cal,
    "current_year": current_year,
    "current_time": current_time,
    })