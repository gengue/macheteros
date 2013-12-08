#encoding: utf-8
from django import forms
from macheteros.apps.gestion_material.models import Perfil
from django.contrib.auth.models import User

TIPOS_DE_USUARIO = (
		("EST","Estudiante"),
		("DOC", "Docente"),
	)

class ContactForm(forms.Form):
	Email = forms.EmailField(widget=forms.TextInput())
	Titulo = forms.CharField(widget=forms.TextInput())
	Texto = forms.CharField(widget=forms.Textarea())

class loginForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput())
	password = forms.CharField(widget=forms.PasswordInput(render_value=False))

class nuevoPerfilForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput(), label="Usuario")
	password = forms.CharField(widget=forms.PasswordInput(render_value=False), label="Contraseña")
	passwordConfirm = forms.CharField(widget=forms.PasswordInput(render_value=False), label="Confirmar Contraseña")
	email = forms.EmailField()	
	tipoUsuario = forms.ChoiceField(choices=TIPOS_DE_USUARIO)
	 
