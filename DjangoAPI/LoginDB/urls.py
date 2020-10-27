from django.conf.urls import url
from . import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
    url(r'signupreq/$',views.userAPI.as_view()),
    # url(r'signupreq/([\w{}.-]+)',views.userApi),

    url(r'^SaveFile$', views.SaveFile),
    url(r'^api/login/', views.loginAPI.as_view()),
    url(r'^api/logout/', views.logoutAPI.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)