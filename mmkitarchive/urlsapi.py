from django.conf.urls import url, include

from . import views

items_patterns = [
    url('^$', views.ItemListCreateView.as_view(), name='list'),
    url('^(?P<pk>\d+)/$', views.ItemRetrieveUpdateView.as_view(), name='detail')
]

categories_patterns = [
    url('^$', views.CategoryListCreateView.as_view(), name='list'),
    url('^(?P<pk>\d+)/$', views.CategoryRetrieveUpdateView.as_view(), name='detail'),
]

urlpatterns = [
    url(r'^items/', include(items_patterns, namespace='items')),
    url(r'^categories/', include(categories_patterns, namespace='categories'))
]
