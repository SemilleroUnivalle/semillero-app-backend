# Generated by Django 5.1.7 on 2025-05-05 15:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categoria', '0001_initial'),
        ('oferta_academica', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OfertaCategoria',
            fields=[
                ('id_oferta_categoria', models.AutoField(primary_key=True, serialize=False)),
                ('precio_publico', models.DecimalField(decimal_places=2, max_digits=10)),
                ('precio_privado', models.DecimalField(decimal_places=2, max_digits=10)),
                ('precio_univalle', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('fecha_finalizacion', models.DateField()),
                ('id_categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='oferta_categoria', to='categoria.categoria')),
                ('id_oferta_academica', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='oferta_categoria', to='oferta_academica.ofertaacademica')),
            ],
            options={
                'verbose_name': 'Oferta Categoria',
                'verbose_name_plural': 'Ofertas Categoria',
                'ordering': ['id_oferta_categoria'],
            },
        ),
    ]
