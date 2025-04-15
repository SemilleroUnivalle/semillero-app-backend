# Generated by Django 5.1.7 on 2025-04-15 19:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('modulo', '0001_initial'),
        ('periodo_academico', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OfertaModulo',
            fields=[
                ('id_oferta', models.AutoField(primary_key=True, serialize=False)),
                ('precio_publico', models.DecimalField(decimal_places=2, max_digits=10)),
                ('precio_privado', models.DecimalField(decimal_places=2, max_digits=10)),
                ('precio_relacion_univalente', models.DecimalField(decimal_places=2, max_digits=10)),
                ('id_modulo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo.modulo')),
                ('id_periodo_academico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='periodo_academico.periodoacademico')),
            ],
            options={
                'verbose_name': 'Oferta Modulo',
                'verbose_name_plural': 'Ofertas Modulos',
                'db_table': 'oferta_modulo',
            },
        ),
    ]
