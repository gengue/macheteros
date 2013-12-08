from django import forms
from macheteros.apps.gestion_material.models import Curso, Comentario

TIPOS_DE_BUSQUEDA = (
		("TOD","Todos los Campos"),
		("TIT","Titulo"),
		("DOC", "Docente"),
		("ASG", "Asignatura"),
	)

class subirMaterialForm(forms.Form):
	Titulo = forms.CharField(max_length=150)
	Descripcion = forms.CharField(widget=forms.Textarea)
	Curso = forms.ModelChoiceField(queryset=Curso.objects.all(), label="Curso")
	Archivo = forms.FileField()

class comentarioForm(forms.Form):
	Comentario = forms.CharField(widget=forms.Textarea)

class busquedaForm(forms.Form):
	TipoBusqueda = forms.ChoiceField(choices=TIPOS_DE_BUSQUEDA, label="Tipo de Busqueda")
	Busqueda = forms.CharField(max_length=150, label="", required=False)

