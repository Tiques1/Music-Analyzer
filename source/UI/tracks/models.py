from django.db import models

# Create your models here.


class Track(models.Model):
    name = models.CharField('name', max_length=2566, primary_key=True)
    album = models.CharField('album', max_length=256)
    text = models.TextField('text')
    date = models.DateTimeField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Трек'
        verbose_name_plural = 'Треки'
