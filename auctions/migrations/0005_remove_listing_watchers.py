# Generated by Django 3.2 on 2021-05-03 20:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_listing_watchers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='watchers',
        ),
    ]
