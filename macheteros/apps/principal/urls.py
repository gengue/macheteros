from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('macheteros.apps.principal.views',
	url(r'^$','index_view', name='vista_principal'),
	url(r'^about/$','about_view', name='vista_about'),
	url(r'^contact/$','contact_view',name='vista_contact'),
	url(r'^login/$', 'login_view', name = 'vista_login'),
	url(r'^logout/$', 'logout_view',name = 'vista_logout'),
	url(r'^nuevoUsuario/$', 'nuevo_perfil_view',name = 'vista_nuevo_perfil'),	
	url(r'^Miperfil/$', 'perfil_view',name = 'vista_perfil'),
)