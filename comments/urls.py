from django.conf.urls import url
from .views import (
    comment_thread,
    comment_delete,
    comment_delete_from_post
)

urlpatterns = [
    url(r'^(?P<id>\d+)/$', comment_thread, name='thread'),
    url(r'^(?P<id>\d+)/delete$', comment_delete, name='delete'),
    url(r'^(?P<id>\d+)/deleteComment$', comment_delete_from_post, name='delete_from_post'),
]
