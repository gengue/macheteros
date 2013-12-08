#encoding: utf-8
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth import login,logout, authenticate
from django.http import HttpResponseRedirect, HttpResponse
from macheteros.apps.gestion_material.forms import subirMaterialForm, comentarioForm, busquedaForm
from macheteros.apps.gestion_material.models import Entrada, Archivo, Perfil, Comentario_entrada, Comentario, Curso, Docente, Asignatura
from django.core.files import File
from django.db.models import Q
import os
from datetime import datetime
from macheteros import settings

def buscar_material_view(request):
	entradas = None
	if request.method == "POST":
		formulario = busquedaForm(request.POST)
		if formulario.is_valid():
			tipo = formulario.cleaned_data['TipoBusqueda']
			query = formulario.cleaned_data['Busqueda'].strip()

			if tipo == "TOD":
				profesor = Docente.objects.filter(Q(Nombre__contains=query) | Q(Apellido__contains=query))
				curso1 = Curso.objects.filter(Docente = profesor)
				entry1 = Entrada.objects.order_by('Titulo').filter(Curso=curso1)
				materia = Asignatura.objects.filter(nombre__contains=query)
				curso2 = Curso.objects.filter(Asignatura=materia)
				entry2 = Entrada.objects.order_by('Titulo').filter(Curso=curso2)
				entry3 = Entrada.objects.order_by('Titulo').filter(Titulo__contains=query)
				entradas = entry1 | entry2 | entry3
			elif tipo == "DOC":
				profesor = Docente.objects.filter(Q(Nombre__contains=query) | Q(Apellido__contains=query))
				curso = Curso.objects.filter(Docente = profesor)
				entradas = Entrada.objects.order_by('Titulo').filter(Curso=curso)
			elif tipo == "ASG":
				materia = Asignatura.objects.filter(nombre__contains=query)
				curso = Curso.objects.filter(Asignatura=materia)
				entradas = Entrada.objects.order_by('Titulo').filter(Curso=curso)
			elif tipo == "TIT":
				entradas = Entrada.objects.order_by('Titulo').filter(Titulo__contains=query)				
	else:
		formulario = busquedaForm()			
	return render_to_response('gestion_material/buscarmaterial.html',{'form':formulario, 'entradas': entradas}, context_instance=RequestContext(request))

def detalle_material_view(request, id_material):
    dato = get_object_or_404(Entrada, pk=id_material)
    comentarios = Comentario_entrada.objects.filter(Entrada=dato)
    doc = dato.Archivo
    ruta = (File(doc.Archivo).name).split("/")
    if request.method == "POST":
    	formulario = comentarioForm(request.POST)
    	if formulario.is_valid() and request.user.is_authenticated():
    		c = Comentario()
    		c.Comentario = formulario.cleaned_data['Comentario']
    		c.Fecha = datetime.now()
    		c.Usuario = Perfil.objects.get(Usuario = request.user)
    		c.save()
    		ce = Comentario_entrada()
    		ce.Comentario = c
    		ce.Entrada = dato
    		ce.save()
    else:
    	formulario = comentarioForm()

    return render_to_response('gestion_material/detallematerial.html',{'entrada':dato,'comentarios':comentarios, 'form':formulario, 'namefile': ruta[len(ruta)-1]}, context_instance=RequestContext(request))

def publicar_comentario_view(request):

	return render_to_response('gestion_material/detallematerial.html',{'entrada':dato,'comentarios':comentarios, 'form':formulario}, context_instance=RequestContext(request))

def descargar_material_view(request, id_entrada):

	""" Descargamos el archivo alojado en el server """

	entrada = Entrada.objects.get(id=id_entrada)
	doc = entrada.Archivo
	if entrada.Archivo.Extension == ".docx":
		response = HttpResponse(mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document') 
	elif entrada.Archivo.Extension == ".doc":
		response = HttpResponse(mimetype='application/msword')
	elif entrada.Archivo.Extension == ".pdf":
		response = HttpResponse(mimetype='application/pdf')	
	elif entrada.Archivo.Extension == ".jpg":
		response = HttpResponse(mimetype="image/jpeg")
	elif entrada.Archivo.Extension == ".png":
		response = HttpResponse(mimetype="image/png")
	elif entrada.Archivo.Extension == ".ppt":
		response = HttpResponse(mimetype="application/vnd.ms-powerpoint")
	elif entrada.Archivo.Extension == ".pptx":
		response = HttpResponse(mimetype="application/vnd.openxmlformats-officedocument.presentationml.presentation")
	elif entrada.Archivo.Extension == ".xls":
		response = HttpResponse(mimetype="application/vnd.ms-excel")
	elif entrada.Archivo.Extension == ".xlsx":
		response = HttpResponse(mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
	elif entrada.Archivo.Extension == ".zip":
		response = HttpResponse(mimetype="application/zip")
	elif entrada.Archivo.Extension == ".rar":
		response = HttpResponse(mimetype="application/x-rar-compressed")
	elif entrada.Archivo.Extension == ".gif":
		response = HttpResponse(mimetype="image/gif")
	else:
		response = HttpResponse(mimetype="text/plain")

	response['Content-Disposition'] = 'attachment; filename=%s'%doc.Nombre

	#fichero= open(os.path.join(doc.Nombre), 'rb')
	fichero= open(File(doc.Archivo).name, 'rb')
	contenido = fichero.read()
	response.write(contenido)
	return response

def _gestion_archivo(docfile):
	f = Archivo()
	doc = File(docfile)
	f.Archivo = docfile
	f.Nombre = os.path.splitext(doc.name)[0]
	f.Extension = os.path.splitext(doc.name)[1]
	f.save()
	return f

def subir_material_view(request):
	if request.method == "POST":
		formulario = subirMaterialForm(request.POST, request.FILES)
		if formulario.is_valid() and request.user.is_authenticated ():			
			curso = formulario.cleaned_data['Curso']
			titulo = formulario.cleaned_data['Titulo']
			descripcion = formulario.cleaned_data['Descripcion']			
			archivo = request.FILES['Archivo']
			#creamos el objeto a guardar en la bd
			entry = Entrada()
			entry.Curso = curso
			entry.Titulo = titulo
			entry.Descripcion = descripcion
			entry.Archivo = _gestion_archivo(archivo)
			entry.Fecha = datetime.now()
			entry.Usuario = Perfil.objects.get(Usuario = request.user)
			entry.save()
			return HttpResponseRedirect('/')
	else:
		formulario = subirMaterialForm()			
	ctx = {'form':formulario}

	return render_to_response('gestion_material/subirmaterial.html', ctx, context_instance=RequestContext(request))