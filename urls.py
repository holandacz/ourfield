from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from tastypie.api import Api
from places.api import PlaceResource
from boundaries.api import BoundaryResource
from en.api import ENNoteResource
#from tweets.api import TweetResource

v1_api = Api(api_name='v1')
v1_api.register(PlaceResource())
v1_api.register(BoundaryResource())
v1_api.register(ENNoteResource())


from django.contrib import admin
admin.autodiscover()

from pinax.apps.account.openid_consumer import PinaxConsumer

handler500 = "pinax.views.server_error"


urlpatterns = patterns("",
    url(r"^$", direct_to_template, {
        "template": "homepage.html",
    }, name="home"),
    url(r"^admin/invite_user/$", "pinax.apps.signup_codes.views.admin_invite_user", name="admin_invite_user"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^about/", include("about.urls")),
    url(r"^map/", include("map.urls")),
    url(r"^places/", include("places.urls")),
    url(r"^en/", include("en.urls")),
    url(r"^account/", include("pinax.apps.account.urls")),
    url(r"^openid/", include(PinaxConsumer().urls)),
    url(r"^profiles/", include("idios.urls")),
    url(r"^notices/", include("notification.urls")),
    url(r"^announcements/", include("announcements.urls")),    
    (r'^api/', include(v1_api.urls)),
)


if settings.SERVE_MEDIA:
    urlpatterns += patterns("",
        url(r"", include("staticfiles.urls")),
    )