from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^show/(?P<notification_id>\d+)/$', 'show_notification'),
    url(r'^markedasread/(?P<notification_id>\d+)/$', 'mark_notification'),
)