# Generated by Django 3.2 on 2021-05-04 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_remove_listing_watchers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='bid',
        ),
        migrations.AddField(
            model_name='bid',
            name='listings',
            field=models.ManyToManyField(blank=True, related_name='bids', to='auctions.Listing'),
        ),
    ]