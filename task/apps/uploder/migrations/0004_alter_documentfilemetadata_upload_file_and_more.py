# Generated by Django 5.0.4 on 2024-04-12 03:25

import utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uploder', '0003_alter_imagefilemetadata_height_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentfilemetadata',
            name='upload_file',
            field=models.FileField(upload_to=utils.FileUpload.upload_to),
        ),
        migrations.AlterField(
            model_name='imagefilemetadata',
            name='upload_file',
            field=models.FileField(upload_to=utils.FileUpload.upload_to),
        ),
        migrations.AlterField(
            model_name='textfilemetadata',
            name='upload_file',
            field=models.FileField(upload_to=utils.FileUpload.upload_to),
        ),
        migrations.AlterField(
            model_name='wordfilemetadata',
            name='upload_file',
            field=models.FileField(upload_to=utils.FileUpload.upload_to),
        ),
    ]
