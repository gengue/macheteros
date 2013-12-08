#encoding: utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from macheteros.apps.principal.forms import ContactForm, loginForm, nuevoPerfilForm
from macheteros.apps.gestion_material.models import Entrada, Perfil
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import login,logout, authenticate
from django.http import HttpResponseRedirect
from macheteros import settings


def index_view(request):
	entradas = Entrada.objects.order_by('Fecha').all()
	return render_to_response('principal/index.html', {'entradas':entradas}, context_instance = RequestContext(request))

def about_view(request):
	mensaje = "Esto es un mensaje desde mi vista"
	ctx = {'msg':mensaje}
	return render_to_response('principal/about.html', ctx, context_instance=RequestContext(request))

def perfil_view(request):
	perfil = Perfil.objects.get(Usuario=request.user)
	entradas = Entrada.objects.filter(Usuario=perfil)
	return render_to_response('principal/miperfil.html', {'perfil':perfil, 'entradas':entradas},context_instance=RequestContext(request))

def nuevo_perfil_view(request):
	mensaje = ""
	if request.method == "POST":
		formulario = nuevoPerfilForm(request.POST)
		if formulario.is_valid():
			nombreusuario = formulario.cleaned_data['username']
			password = formulario.cleaned_data['password']
			passwordConfirm = formulario.cleaned_data['passwordConfirm']
			email = formulario.cleaned_data['email']
			tipoUsuario = formulario.cleaned_data['tipoUsuario']
			#creamos el nuevo perfil
			p = Perfil()			
			if(password == passwordConfirm):
				user = User.objects.create_user(nombreusuario, email, password)
				user.save()
				p.Usuario = user
				p.TipoDeUsuario = tipoUsuario
				p.save()
				mensaje = "Usuario registrado con exito"
			else:
				formulario = nuevoPerfilForm()
				mensaje = "las Contraseñas no coinciden"				
			return render_to_response('principal/nuevousuario.html', {'form':formulario, 'msg':mensaje},context_instance=RequestContext(request))
	else:
		formulario = nuevoPerfilForm()
	return render_to_response('principal/nuevousuario.html', {'form':formulario,'msg':mensaje},context_instance=RequestContext(request))

def contact_view(request):
	info_enviado = False #Definir si se envio la informacion o no se envio
	email = ""
	titulo = ""
	texto = ""
	if request.method == "POST":
		formulario = ContactForm(request.POST)
		if formulario.is_valid():
			info_enviado = True
			email = formulario.cleaned_data['Email']
			titulo = formulario.cleaned_data['Titulo']
			texto = formulario.cleaned_data['Texto']
			# Configuracion enviado mensaje via gmail
			to_admin = 'genesisdaft@gmail.com'
			html_content = "Informacion Recibida de [%s]<br><br>**Mensaje**<br>%s"%(email, texto)
			msg = EmailMultiAlternatives('Correo de Contacto',html_content,'from@server.com',[to_admin])
			msg.attach_alternative(html_content, 'text/html')
			msg.send()
	else:   

		formulario = ContactForm()	
	ctx = {'form':formulario,'email':email,'titulo':titulo,'texto':texto, 'info_enviado':info_enviado}
	return render_to_response('principal/contacto.html', ctx,context_instance=RequestContext(request))

def login_view(request):
	mensaje = ""
	if request.user.is_authenticated():
		return HttpResponsRedirect('/')
	else:
		if request.method == "POST":
			form = loginForm(request.POST)
			if form.is_valid():
				username = form.cleaned_data['username']
				password = form.cleaned_data['password']
				usuario = authenticate(username=username,password=password)
				if usuario is not None and usuario.is_active:
					login(request,usuario)
					return HttpResponseRedirect('/')
				else:
					mensaje = "usuario y/o password incorrecto"
		form = loginForm()
		ctx = {'form':form, 'mensaje':mensaje}
		return render_to_response('principal/login.html', ctx, context_instance=RequestContext(request))

def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')
