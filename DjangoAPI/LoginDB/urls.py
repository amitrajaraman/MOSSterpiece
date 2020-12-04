from django.conf.urls import url
from . import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
    url(r'signupreq/$',views.userAPI.as_view()),
    # url(r'signupreq/([\w{}.-]+)',views.userApi),

    url(r'^api/files/', views.fileAPI.as_view()),
    url(r'^api/login/', views.loginAPI.as_view()),
    url(r'^api/logout/', views.logoutAPI.as_view()),
    url('^api/files/<str:path>', views.fileAPI.as_view(),
        {'document root': settings.MEDIA_ROOT}),
    url(r'^api/password/', views.changeAPI.as_view()),    
    url(r'^api/process/', views.processAPI.as_view()),
    url(r'^token/', views.tokenAPI.as_view()),
] 
