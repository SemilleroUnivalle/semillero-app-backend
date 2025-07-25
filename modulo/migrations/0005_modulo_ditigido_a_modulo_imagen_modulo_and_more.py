# Generated by Django 5.1.7 on 2025-05-28 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modulo', '0004_alter_modulo_id_oferta_categoria'),
    ]

    operations = [
        migrations.AddField(
            model_name='modulo',
            name='ditigido_a',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='modulo',
            name='imagen_modulo',
            field=models.ImageField(blank=True, null=True, upload_to='modulos/'),
        ),
        migrations.AddField(
            model_name='modulo',
            name='incluye',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='modulo',
            name='intensidad_horaria',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
