# Generated by Django 4.0.4 on 2022-04-20 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adverts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='advert',
            name='content_type',
            field=models.CharField(help_text='The MIMEType of the file', max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='advert',
            name='picture',
            field=models.BinaryField(editable=True, null=True),
        ),
    ]
