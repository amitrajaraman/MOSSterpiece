from django.conf.urls import url
from LoginDB import views

urlpatterns=[
    url(r'signupreq/$',views.userApi),
    url(r'signupreq/([\w{}.-]+)',views.userApi)
]