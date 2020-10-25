from django.conf.urls import url
from LoginDB import views

urlpatterns=[
    url(r'signup/$',views.userApi),
    url(r'signup/([\w{}.-]+)',views.userApi)
]