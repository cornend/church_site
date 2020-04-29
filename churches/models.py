from django.db import models


class Church(models.Model):
    name = models.CharField(max_length=200, unique=True)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    province_state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    class Meta:
        ordering = ('country', 'name')

    def __str__(self):
        return self.name


class Speaker(models.Model):
    church = models.ForeignKey(Church, on_delete=models.PROTECT, related_name='speakers')
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    province_state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name
