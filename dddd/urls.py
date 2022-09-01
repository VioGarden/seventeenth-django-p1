from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('search.urls')),
    path('members/', include('django.contrib.auth.urls')),  #django authentication system
    path('members/', include('members.urls')), 
]

# Configure Admin Titles
admin.site.site_header = "Club Administration"
admin.site.site_title = "Browser Title"
admin.site.index_title = "Welcome to the Admin Area"

