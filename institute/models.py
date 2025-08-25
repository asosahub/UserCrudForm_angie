from django.db import models

# 1. python manage.py makemigrations
# 2. python manage.py migrate


#carreras del instituto
class Career(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

#clubes del instituto
class Club(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField(unique=True)
    career = models.ForeignKey(Career, on_delete=models.SET_NULL, null=True, blank=True) #si se elimina una carrera, no elimina el usuario
    clubs = models.ManyToManyField(Club, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    #muestra el nombre completo del usuario
    def __str__(self):
        return f"{self.first_name} {self.last_name}"