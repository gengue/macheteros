from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('macheteros.apps.gestion_material.views',
	url(r'^buscarMaterial/$','buscar_material_view', name='vista_buscar_material'),
	url(r'^subirMaterial/$','subir_material_view', name='vista_subir_material'),	
	url(r'^material/(?P<id_material>\d+)$', 'detalle_material_view', name = 'vista_detalle_material'),
	url(r'^descarga/(?P<id_entrada>\d+)$', 'descargar_material_view', name = 'vista_descargar_material'),
	url(r'^buscarMaterial/$', 'buscar_material_view', name = 'vista_buscar_material'),
)