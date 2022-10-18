from django.db import models


class Entry(models.Model):
    type = models.IntegerField()
    date = models.DateField()
    value = models.IntegerField()
    cpf = models.CharField(max_length=11)
    card = models.CharField(max_length=12)
    time = models.TimeField()
    owner = models.CharField(max_length=14)
    outlet = models.CharField(max_length=19)

    def __str__(self):
        return f"{self.id} {self.type} {self.date}"
