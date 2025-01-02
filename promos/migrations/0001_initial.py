# Generated by Django 5.1.1 on 2024-12-09 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('image', models.ImageField(upload_to='sliders')),
                ('url', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'slider',
                'verbose_name_plural': 'sliders',
                'db_table': 'promos_sliders',
                'ordering': ['-id'],
            },
        ),
    ]
