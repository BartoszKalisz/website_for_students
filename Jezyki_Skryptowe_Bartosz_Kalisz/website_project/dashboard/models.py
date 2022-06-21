from django.db import models
from django.contrib.auth.models import User


class Notatki(models.Model):
    uzytkownik = models.ForeignKey(User,on_delete=models.CASCADE)
    tytuł = models.CharField(max_length=200)
    opis = models.TextField()

    def __str__(self):
        return self.tytuł

    class Meta:
        verbose_name = "notatki"
        verbose_name_plural = "notatki"


class Lista(models.Model):
    uzytkownik = models.ForeignKey(User,on_delete=models.CASCADE)
    przedmiot = models.CharField(max_length=60)
    tytuł = models.CharField(max_length=100)
    opis = models.TextField()
    termin = models.DateTimeField()
    czy_skonczony = models.BooleanField(default=False)

    def __str__(self):
        return self.tytuł
    
