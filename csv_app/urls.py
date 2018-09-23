from django.conf.urls import url
from . import views

#from csv_app.views import ToDoView

urlpatterns = [
    #url(r'^api/',ToDoView.as_view()),
    url(r'^$', views.home, name = 'home'),
    url(r'^home/$', views.home, name = 'home'),
    url(r'^help/$', views.help, name = 'help'),
    url(r'^data_search/$', views.data_search, name = 'data_search'),
]
