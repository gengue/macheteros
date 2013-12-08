#encoding:utf-8
from django.db import models
from django.contrib.auth.models import User
from macheteros import settings

class Asignatura(models.Model):
	nombre = models.CharField(max_length=150, null=False, unique=True)

	def __unicode__(self):
		return self.nombre

class Docente(models.Model):
	Nombre = models.CharField(max_length=150)
	Apellido = models.CharField(max_length=150)

	def __unicode__(self):
		return "%s %s"%(self.Nombre, self.Apellido)

class Periodo(models.Model):
	I='I'
	II='II'
	PERIODOS =(
		('I',"Primer periodo"),
		('II',"Segundo periodo"),
	)
	Anho = models.CharField(max_length=4)
	Periodo = models.CharField(max_length=2, choices=PERIODOS, default='I')

	def __unicode__(self):
		return "%s~%s"%(self.Anho, self.Periodo)

class Curso(models.Model):
	Asignatura = models.ForeignKey(Asignatura)
	Docente = models.ForeignKey(Docente)
	Periodo = models.ForeignKey(Periodo)

	def __unicode__(self):
		return "%s - %s - %s"%(unicode(self.Asignatura), unicode(self.Docente), unicode(self.Periodo))

class Perfil(models.Model):
	ESTUDIANTE = "EST"
	DOCENTE = "DOC"
	TIPOS_DE_USUARIO = (
		(ESTUDIANTE, "Estudiante"),
		(DOCENTE, "Docente"),
	)
	Usuario= models.ForeignKey(User, unique=True)
	TipoDeUsuario =  models.CharField(max_length=3, choices=TIPOS_DE_USUARIO, default=ESTUDIANTE)

	def __unicode__(self):
		return "%s - %s"%(unicode(self.Usuario),unicode(self.TipoDeUsuario in (self.ESTUDIANTE,self.DOCENTE)))

class Comentario(models.Model):
	Usuario = models.ForeignKey(Perfil)
	Comentario = models.TextField()
	Fecha = models.DateTimeField()
	def __unicode__(self):
		return unicode(self.Usuario)

class Archivo(models.Model):
	Nombre = models.CharField(max_length=100)
	Extension = models.CharField(max_length=4)
	Archivo = models.FileField(upload_to=settings.MEDIA_ROOT+'/files/', blank=False)
	def __unicode__(self):
		return self.Nombre

class Entrada(models.Model):
	Curso = models.ForeignKey(Curso)
	Usuario = models.ForeignKey(Perfil)
	Archivo = models.ForeignKey(Archivo)
	Titulo = models.CharField(max_length=150)
	Descripcion = models.TextField()
	Fecha = models.DateTimeField()
	Puntuacion = models.IntegerField(max_length=10, default=0)

	def __unicode__(self):
		return self.Titulo

class Comentario_entrada(models.Model):
	Comentario = models.ForeignKey(Comentario)
	Entrada = models.ForeignKey(Entrada)

	def __unicode__(self):
		return "%s - %s"%(unicode(self.Comentario), unicode(Entrada))
