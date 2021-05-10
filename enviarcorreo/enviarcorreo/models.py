from django.db import models

class Archivo(models.Model):
    name = models.FileField(upload_to='static/file')
    def __str__(self):
        return str(self.name)
