from django.conf.urls import url, include

from . import views

activityrecords_patterns = [
    url(r'^$', views.ActivityRecordView.as_view(), name='list')
]

urlpatterns = [
    url(r'^activityrecords/', include(activityrecords_patterns, namespace='activityrecords'))
]
