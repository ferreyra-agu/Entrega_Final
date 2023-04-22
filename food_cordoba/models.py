from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):

    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=300)

    publicador = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='puclicador')
    imagen = models.ImageField(upload_to='posts')
    creado_el = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f"{self.id} -- {self.nombre} - {self.descripcion}"


class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name="profile")
    contact = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='profiles')

class Mensaje(models.Model):
    mensaje = models.CharField(max_length=500)
    email = models.EmailField()
    destinatario = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="destinatario")