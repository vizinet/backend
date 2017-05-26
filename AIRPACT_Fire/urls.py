"""AIRPACT_Fire URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from user_profile import views as user_view
from convos import views as convos_view
from file_upload import views as file_upload_views
from django_comments.models import Comment
from . import views
from .views import LocationAutocomplete
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
	url(r'^$', views.index, name="home"),
    url(r'^tag-autocomplete/$', LocationAutocomplete.as_view(), name='location-autocomplete'),
    url(r'^admin_page$', views.admin_page, name="adminPage"),
    url(r'^uncertified$', views.uncertified, name="uncertified"),
    url(r'^user/', include('user_profile.urls')),
    #url(r'^user', include('user_profile.urls')),
    url(r'^gallery/$', views.gallery, name="gallery"),
    url(r'^gallery/(?P<page>\d+)/$', views.gallery, name='gallery'),
    url(r'^test$', views.test),
	url(r'^file_upload/', include('file_upload.urls')),
    url(r'^admin/', admin.site.urls), 
    url(r'^picture/view/(?P<picId>\d+)/$', file_upload_views.view_picture, name="view_picture"),
    #url(r'^convos/([0-9]+)/$', convos_view.render_convo),
    #url(r'^comments/post/$', convos_view.comment_post),
    #url( r'^comments/posted/$', convos_view.comment_posted),    
    url(r'^comments/', include('django_comments.urls')),
    url(r'^downloads/', views.downloads, name="downloads"),
    url(r'^about/',views.about,name="about"),
    url(r'^index/',views.main,name="main"),
    url(r'^forum/',include('spirit.urls'), name="forum"),
    url(r'^getPythonScripts/', views.getPythonScripts, name="getPythonScripts"),
]
urlpatterns+=staticfiles_urlpatterns()
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)