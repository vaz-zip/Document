# Generated by Django 4.2.7 on 2023-11-29 15:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='----', max_length=32, verbose_name='Название')),
                ('slug', models.SlugField(max_length=32, unique_for_date='dateCreate', verbose_name='Метка')),
                ('category', models.CharField(choices=[('СВИД', 'Свидетельство'), ('ДИПЛ', 'Диплом'), ('ПИСЬМО', 'Письмо'), ('ПАСПОРТ', 'Паспорт'), ('СПРАВ', 'Справка'), ('ЗАЯВ', 'Заявление')], default='СПРАВ', max_length=16, verbose_name='Тип документа')),
                ('textDocument', models.TextField(blank=True, verbose_name='Содержание')),
                ('number', models.IntegerField(default=0, verbose_name='Номер')),
                ('dateCreate', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Внесён в базу')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_doc', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'Документы',
                'verbose_name_plural': 'Документы',
                'ordering': ['-dateCreate'],
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.ImageField(null=True, upload_to='media/images/', verbose_name='Изображение')),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images_doc', to='document.document', verbose_name='Файл')),
            ],
            options={
                'verbose_name': 'Изображения',
                'verbose_name_plural': 'Изображения',
            },
        ),
        migrations.AddIndex(
            model_name='document',
            index=models.Index(fields=['-dateCreate'], name='document_do_dateCre_d4e1be_idx'),
        ),
    ]