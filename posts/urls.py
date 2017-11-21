from django.conf.urls import url
from .views import (
    post_list,
    post_detail,
    post_create,
    post_edit,
    post_delete,
    
)

urlpatterns = [
    url(r'^$', post_list,name='list'),
    url(r'^(?P<slug>[\w-]+)/$', post_detail, name='detail'),
    url(r'^create$', post_create, name='create'),
    url(r'^(?P<slug>[\w-]+)/edit$', post_edit, name='edit'),
    url(r'^(?P<slug>[\w-]+)/delete$', post_delete, name='delete'),

]
