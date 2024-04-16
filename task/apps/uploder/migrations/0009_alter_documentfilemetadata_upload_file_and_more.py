# Generated by Django 5.0.4 on 2024-04-12 09:21

import utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uploder', '0008_remove_wordfilemetadata_user_and_more'),
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
    ]