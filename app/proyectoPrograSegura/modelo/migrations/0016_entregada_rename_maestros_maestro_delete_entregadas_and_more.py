# Generated by Django 4.0.1 on 2022-06-29 15:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('modelo', '0015_registro_usuarios_apellidos_registro_usuarios_nombre'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entregada',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calificacion', models.IntegerField()),
            ],
        ),
        migrations.RenameModel(
            old_name='Maestros',
            new_name='Maestro',
        ),
        migrations.DeleteModel(
            name='entregadas',
        ),
        migrations.RenameModel(
            old_name='Alumnos',
            new_name='Alumno',
        ),
        migrations.AddField(
            model_name='entregada',
            name='usuario',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='modelo.alumno'),
        ),
    ]