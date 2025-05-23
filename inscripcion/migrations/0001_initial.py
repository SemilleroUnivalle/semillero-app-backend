# Generated by Django 5.1.7 on 2025-05-08 00:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('estudiante', '0001_initial'),
        ('grupo', '0001_initial'),
        ('oferta_academica', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inscripcion',
            fields=[
                ('id_inscripcion', models.AutoField(primary_key=True, serialize=False)),
                ('estado', models.CharField(choices=[('A', 'Activo'), ('I', 'Inactivo'), ('R', 'Rechazado')], default='A', max_length=20)),
                ('fecha_inscripcion', models.DateField(auto_now_add=True)),
                ('tipo_vinculacion', models.CharField(max_length=255)),
                ('terminos', models.BooleanField(default=True)),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('id_estudiante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='estudiante.estudiante')),
                ('id_grupo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grupo.grupo')),
                ('id_oferta_academica', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='oferta_academica.ofertaacademica')),
            ],
            options={
                'verbose_name': 'Inscripción',
                'verbose_name_plural': 'Inscripciones',
                'ordering': ['fecha_inscripcion'],
            },
        ),
    ]
