from django.conf.urls import patterns, include, url
import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^',include('macheteros.apps.principal.urls')),
    url(r'^',include('macheteros.apps.gestion_material.urls')),
    #url(r'^',include('macheteros.apps.gestion_material.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT})
)