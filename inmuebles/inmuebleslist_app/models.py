from django.db import models


# Create your models here.
class Inmueble(models.Model):
    direccion = models.CharField(max_length=250)
    pais = models.CharField(max_length=250)
    descripcion = models.CharField(max_length=250)
    image = models.CharField(max_length=250)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.direccion
