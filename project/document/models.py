from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from document.resources import POSITIONS, reference
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify


class Document(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', related_name='user_doc')
    title = models.CharField(max_length=32, default="----", verbose_name='Название')
    slug = models.SlugField(max_length=32, unique_for_date='dateCreate', verbose_name='Метка')
    category = models.CharField(max_length=16, choices=POSITIONS, default=reference, verbose_name='Тип документа')
    textDocument = models.TextField(blank=True, verbose_name='Содержание')
    number = models.IntegerField(default=0, verbose_name='Номер')
    dateCreate = models.DateTimeField(default=timezone.now, verbose_name='Внесён в базу')
    class Meta:
        ordering = ['-dateCreate']
        indexes = [
            models.Index(fields=['-dateCreate']), 
            ]
        verbose_name = 'Документы'
        verbose_name_plural = 'Документы'
    def __str__(self):
        return f'{self.dateCreate.strftime("%d. %m. %Y")} {self.title} {self.category} {self.number}'

    def get_absolute_url(self):
        return f'/document/{self.id}'

class Image(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="images_doc", verbose_name='Файл')
    file = models.ImageField(upload_to='media/images/', null=True, verbose_name='Изображение')
    def __str__(self):
        return f'Изображение {self.document_id}'
    def get_absolute_url(self):
        return f'/document/{self.id}'
    class Meta:
        verbose_name = 'Изображения'
        verbose_name_plural = 'Изображения'
