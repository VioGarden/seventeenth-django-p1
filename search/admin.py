from django.contrib import admin
from .models import Venue, MyClubUser, Event

# admin.site.register(Venue) #could do admin.site.register(Venue, VenueAdmin), and stuff below class
admin.site.register(MyClubUser) 
# admin.site.register(Event)

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone')   #what to display
    ordering = ('name',)   #orders in admin place ('-name') is opposite order
    search_fields = ('name', 'address')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fields = (('name', 'venue'), 'event_date', 'description', 'manager')
    list_display = ('name', 'event_date', 'venue')
    list_filter = ('event_date', 'venue')
    ordering = ('-event_date',)
