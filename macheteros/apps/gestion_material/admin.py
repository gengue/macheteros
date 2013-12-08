from django.contrib import admin
from macheteros.apps.gestion_material.models import Asignatura, Docente, Periodo, Curso, Perfil, Comentario, Archivo, Entrada, Comentario_entrada

admin.site.register(Asignatura)
admin.site.register(Docente)
admin.site.register(Periodo)
admin.site.register(Curso)
admin.site.register(Perfil)
admin.site.register(Comentario)
admin.site.register(Archivo)
admin.site.register(Entrada)
admin.site.register(Comentario_entrada)
