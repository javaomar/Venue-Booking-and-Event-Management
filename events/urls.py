from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'events'

urlpatterns = [


    path('', views.home, name='home' ),
    path('events/', views.all_events, name='list-events'),
    path('add_event/<int:res_id>', views.add_event, name='add-event'),
    path('update_event/<int:event_id>', views.update_event, name='update-event'),
    path('event_detail/<int:event_id>', views.event_detail, name='event-detail'),
    path('delete_event/<int:event_id>', views.delete_event , name='delete-event'),
  
    path('ticket_pdf/<int:ticket_id>',views.download_ticket,name='ticket-pdf'),
 
    path('payment/<int:res_id>/',views.payment,name='payment'),
 
    path('myclub/<int:event_id>',views.myclub, name='myclub'),
    path('byticket/<int:ticket_id>',views.buyticket, name='buyticket')

]



 