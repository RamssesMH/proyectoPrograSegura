# Generated by Django 3.2.12 on 2022-06-02 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelo', '0005_alter_registro_usuarios_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='token_login',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=5, unique=True)),
                ('id_usuario', models.BigIntegerField()),
                ('timestamp', models.DateTimeField()),
            ],
        ),
        migrations.AlterField(
            model_name='registro_usuarios',
            name='usuario',
            field=models.CharField(default='', max_length=20, unique=True),
        ),
    ]
