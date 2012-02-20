from django.conf.urls.defaults import patterns, url, include

from tweets.api import v1

# from api import TweetResource
# tweet_resource = TweetResource()

from .views import IndexView, DetailView

urlpatterns = patterns('',
    url(r'^$',
        IndexView.as_view(),
        name='index'),

    url(r'^(?P<pk>\d+)/$',
        DetailView.as_view(),
        name="detail"),

    (r'^api/', include(v1.urls)),
    #(r'^api/', include(tweet_resource.urls)),
)


