from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'reservations'

urlpatterns = [
 
 
 
    path('reservation_form/<int:venue_id>/', views.reservation, name='reservation-form'),
    path('reservation/', views.user_reservation, name='reservation'),
    path('reservation_venue/<int:res_id>', views.reservation_venue, name='reservation-venue'),
    path('disapproved_reserv/<int:res_id>', views.disapproved_reservation, name='disapproved-reserv'),
    path('approved_reserv/<int:res_id>', views.approved_reservation, name='approved-reserv'),
    #venune onwer cancel the reservation 
    path('cancel_reserv/<int:res_id>', views.cancel_reservation, name='cancel-reserv'),
    # the one that made the reservation cancel it's resvartion 
    path('reserv-cancel/<int:res_id>', views.reserv_owner_cancel, name='reserv-cancel'),

]



 