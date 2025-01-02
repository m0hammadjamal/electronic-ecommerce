# Generated by Django 5.1.1 on 2024-12-30 04:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0006_alter_customspecification_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ram',
            old_name='name',
            new_name='value',
        ),
        migrations.RenameField(
            model_name='storage',
            old_name='name',
            new_name='value',
        ),
        migrations.RemoveField(
            model_name='option',
            name='images',
        ),
        migrations.RemoveField(
            model_name='product',
            name='images',
        ),
        migrations.RemoveField(
            model_name='productimage',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='productimage',
            name='created_datetime',
        ),
        migrations.RemoveField(
            model_name='productimage',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='productimage',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='productimage',
            name='updated_datetime',
        ),
        migrations.RemoveField(
            model_name='ram',
            name='ram',
        ),
        migrations.RemoveField(
            model_name='storage',
            name='storage',
        ),
        migrations.AddField(
            model_name='productimage',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='items.product'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productimage',
            name='variant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='images', to='items.option'),
        ),
        migrations.AlterField(
            model_name='option',
            name='ram',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='option',
            name='storage',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(upload_to='product_images'),
        ),
    ]
