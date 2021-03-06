
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelo', '0021_remove_tarea_datetimeofupload_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tarea',
            name='script_comprobacion',
            field=models.FileField(default='', upload_to='media/tareas/'),
        ),
        migrations.AlterField(
            model_name='tarea',
            name='script_inicializacion',
            field=models.FileField(default='', upload_to='media/tareas/'),
        ),
        migrations.AlterField(
            model_name='tarea',
            name='script_parametros',
            field=models.FileField(default='', upload_to='media/tareas/'),
        ),
    ]
