# Generated by Django 5.1.7 on 2025-05-05 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Grupo',
            fields=[
                ('id_grupo', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_grupo', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Grupo',
                'verbose_name_plural': 'Grupos',
                'ordering': ['id_grupo'],
            },
        ),
    ]
