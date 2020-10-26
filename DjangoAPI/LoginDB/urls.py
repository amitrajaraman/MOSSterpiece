from django.conf.urls import url
from LoginDB import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
    url(r'signupreq/$',views.userApi),
    url(r'signupreq/([\w{}.-]+)',views.userApi),

    url(r'^SaveFile$', views.SaveFile)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)