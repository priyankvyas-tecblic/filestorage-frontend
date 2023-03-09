from django.urls import path,include
from myapp import views
urlpatterns = [
    path('signin/',views.signIn),
    path('checklogin/',views.checkLogin),
    path('upload/',views.upload),
    path('signup/',views.signUp),
    path('savedata/',views.saveData),
    path('logout/',views.logout)

]