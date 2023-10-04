from django.urls import path
from venue import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'venues'

urlpatterns = [
    #path Converters
    # int: numbers ex year, date
    # str: strings
    # path: whole urls/   Ex something/something/something
    # slug: hyphen-and_underscores_stuff
    # UUID: universally unique identifier

 
    path('add_venue/', views.add_venue, name='add-venue'),
    path('list_venue/', views.list_venues, name='list-venues'),
    path('show_venue/<int:venue_id>', views.show_venue, name='show-venue'),
    path('search_venue/', views.search_venues, name='search-venues'),
    path('update_venue/<int:venue_id>', views.update_venue, name='update-venue'),
     
 
    path('delete_venue/<int:venue_id>', views.delete_venue, name='delete-venue'),
    path('venue_text',views.venue_text,name='veunue-text'),
    path('venue_csv',views.venue_csv,name='veunue-csv'),
    path('venue_pdf',views.venue_pdf,name='veunue-pdf'), 
    
 
    
 

]



 