from django.urls import path, include 
from django.contrib.auth import views as auth_views
from . import views 


app_name = 'accounts'


urlpatterns = [

    path('login',views.userlogin,name='login'),
    path('',views.userlogin,name='login'),
    path('logout',views.userlogout,name='logout'),
 
    path('signup/',views.register ,name='signup'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('password_reset', views.passwordreset,name='password-reset'),
    path('reset/<uidb64>/<token>', views.passwordnew, name='password-new'),


 
]
