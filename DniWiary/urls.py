from django.conf.urls import patterns, include, url
from django.contrib import admin, staticfiles
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from DniWiary.settings import MEDIA_ROOT, MEDIA_URL, STATIC_URL, STATIC_ROOT
from django.conf.urls.static import static
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'DniWiary.views.home', name='home'),
    # url(r'^DniWiary/', include('DniWiary.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'core.views.homepage' ),
    url(r'^day,(?P<id>\d+),(?P<name>\w+).html$', 'core.views.dayView' ),
    url(r'^page,(?P<name>\w+).html$', 'core.views.newspage' ),
    url(r'^sponsors.html$', 'core.views.sponsors' ),
    #url(r'^about.html$', 'core.views.about' ),
    url(r'^guests.html$', 'core.views.guests' ),
    url(r'^contact.html$', 'core.views.contact' ),
    #url(r'^galleries.html$', 'core.views.galleries' ),
    url(r'^gallery,(?P<id>\d+),(?P<name>\w+).html$', 'core.views.gallery' ),
    url(r'^sentence/(?P<nr>\d+)$', 'core.views.sentence' ),
    url(r'^sentence/$', 'core.views.sentence' ),
    url(r'^sponsor/(?P<nr>\d+)$', 'core.views.sponsor' ),
    url(r'^sponsor/$', 'core.views.sponsor' ),
    url(r'^sponsor/all$', 'core.views.sponsors2' ),
) + static( MEDIA_URL, document_root = MEDIA_ROOT ) + static( STATIC_URL, document_root = STATIC_ROOT )
