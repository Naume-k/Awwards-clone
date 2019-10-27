from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns=[
    url('^$',views.welcome,name = 'welcome'),
    url(r'^new/upload$', views.upload_image, name='upload'),
    url(r'^new/profile$', views.add_profile, name='edit'),
    url(r'^myprofile$', views.my_profile, name='myprofile'),
    url(r'^comment/(\d+)/$', views.add_comment, name='comment'),
    url(r'^search/',views.search_users, name = 'searchs'),
    # url(r'^likes/(?P<id>\d+)',views.likes, name = 'like'),
    url(r'^rate/(\d+)$',views.rating,name='rating'),
    url(r'^api/profile/$', views.ProfileList.as_view(), name = 'profile'),
    url(r'^api/project/$', views.ProjectList.as_view(), name = 'project')
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    