# Generated by Django 4.2.5 on 2024-03-03 18:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('studease', '0021_rollnumber_subsection'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rollnumber',
            name='subsection',
        ),
    ]
