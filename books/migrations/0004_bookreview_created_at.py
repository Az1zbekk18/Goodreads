# Generated by Django 5.1.7 on 2025-03-24 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_alter_bookreview_stars_given'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookreview',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
