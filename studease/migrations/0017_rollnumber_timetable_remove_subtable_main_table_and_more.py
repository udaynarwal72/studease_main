# Generated by Django 4.2.5 on 2024-03-03 09:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('studease', '0016_delete_logindetails_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='RollNumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roll_number', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='TimeTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_name', models.CharField(max_length=100)),
                ('day', models.CharField(max_length=50)),
                ('time', models.TimeField()),
                ('roll_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studease.rollnumber')),
            ],
        ),
        migrations.RemoveField(
            model_name='subtable',
            name='main_table',
        ),
        migrations.RenameField(
            model_name='subsection',
            old_name='main_subsection',
            new_name='sub_section_name',
        ),
        migrations.DeleteModel(
            name='MainTable',
        ),
        migrations.DeleteModel(
            name='SubTable',
        ),
        migrations.AddField(
            model_name='rollnumber',
            name='sub_section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studease.subsection'),
        ),
    ]
